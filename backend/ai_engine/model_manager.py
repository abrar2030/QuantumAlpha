"""
Model manager for QuantumAlpha AI Engine.
Handles model training, evaluation, and management.
"""
import os
import logging
import uuid
import json
import pickle
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Dense, LSTM, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Add parent directory to path to import common modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    setup_logger,
    ServiceError,
    ValidationError,
    NotFoundError
)

# Configure logging
logger = setup_logger('model_manager', logging.INFO)

class ModelManager:
    """Model manager"""
    
    def __init__(self, config_manager, db_manager):
        """Initialize model manager
        
        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        
        # Initialize data service URL
        self.data_service_url = f"http://{config_manager.get('services.data_service.host')}:{config_manager.get('services.data_service.port')}"
        
        # Initialize model directory
        self.model_dir = config_manager.get('ai_engine.model_dir', '/home/ubuntu/quantumalpha_backend/models')
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize model registry
        self.registry_file = os.path.join(self.model_dir, 'registry.json')
        self.model_registry = self._load_registry()
        
        logger.info("Model manager initialized")
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load model registry
        
        Returns:
            Model registry
        """
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading model registry: {e}")
                return {'models': {}}
        else:
            return {'models': {}}
    
    def _save_registry(self) -> None:
        """Save model registry"""
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self.model_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving model registry: {e}")
    
    def get_models(self) -> List[Dict[str, Any]]:
        """Get all models
        
        Returns:
            List of models
        """
        models = []
        
        for model_id, model_info in self.model_registry['models'].items():
            models.append({
                'id': model_id,
                'name': model_info['name'],
                'description': model_info['description'],
                'type': model_info['type'],
                'status': model_info['status'],
                'created_at': model_info['created_at'],
                'updated_at': model_info['updated_at'],
                'metrics': model_info.get('metrics', {})
            })
        
        return models
    
    def get_model(self, model_id: str) -> Dict[str, Any]:
        """Get a specific model
        
        Args:
            model_id: Model ID
            
        Returns:
            Model details
            
        Raises:
            NotFoundError: If model is not found
        """
        if model_id not in self.model_registry['models']:
            raise NotFoundError(f"Model not found: {model_id}")
        
        model_info = self.model_registry['models'][model_id]
        
        return {
            'id': model_id,
            'name': model_info['name'],
            'description': model_info['description'],
            'type': model_info['type'],
            'status': model_info['status'],
            'created_at': model_info['created_at'],
            'updated_at': model_info['updated_at'],
            'metrics': model_info.get('metrics', {}),
            'parameters': model_info.get('parameters', {}),
            'features': model_info.get('features', [])
        }
    
    def create_model(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new model
        
        Args:
            data: Model data
            
        Returns:
            Created model
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Validate required fields
            if 'name' not in data:
                raise ValidationError("Model name is required")
            
            if 'type' not in data:
                raise ValidationError("Model type is required")
            
            # Generate model ID
            model_id = f"model_{uuid.uuid4().hex}"
            
            # Create model info
            model_info = {
                'name': data['name'],
                'description': data.get('description', ''),
                'type': data['type'],
                'status': 'created',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'parameters': data.get('parameters', {}),
                'features': data.get('features', [])
            }
            
            # Add to registry
            self.model_registry['models'][model_id] = model_info
            
            # Save registry
            self._save_registry()
            
            return {
                'id': model_id,
                'name': model_info['name'],
                'description': model_info['description'],
                'type': model_info['type'],
                'status': model_info['status'],
                'created_at': model_info['created_at'],
                'updated_at': model_info['updated_at'],
                'parameters': model_info['parameters'],
                'features': model_info['features']
            }
        
        except ValidationError:
            raise
        
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise ServiceError(f"Error creating model: {str(e)}")
    
    def train_model(
        self,
        model_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Train a model
        
        Args:
            model_id: Model ID
            data: Training data
            
        Returns:
            Training result
            
        Raises:
            NotFoundError: If model is not found
            ValidationError: If data is invalid
            ServiceError: If there is an error training the model
        """
        try:
            # Check if model exists
            if model_id not in self.model_registry['models']:
                raise NotFoundError(f"Model not found: {model_id}")
            
            # Get model info
            model_info = self.model_registry['models'][model_id]
            
            # Validate required fields
            if 'symbol' not in data:
                raise ValidationError("Symbol is required")
            
            if 'timeframe' not in data:
                raise ValidationError("Timeframe is required")
            
            if 'period' not in data:
                raise ValidationError("Period is required")
            
            # Update model status
            model_info['status'] = 'training'
            self._save_registry()
            
            # Get market data
            market_data = self._get_market_data(
                symbol=data['symbol'],
                timeframe=data['timeframe'],
                period=data['period']
            )
            
            # Process data
            processed_data = self._process_data(
                market_data=market_data,
                features=model_info.get('features', [])
            )
            
            # Train model based on type
            if model_info['type'] == 'lstm':
                result = self._train_lstm_model(model_id, model_info, processed_data, data)
            elif model_info['type'] == 'cnn':
                result = self._train_cnn_model(model_id, model_info, processed_data, data)
            elif model_info['type'] == 'transformer':
                result = self._train_transformer_model(model_id, model_info, processed_data, data)
            else:
                raise ValidationError(f"Unsupported model type: {model_info['type']}")
            
            # Update model info
            model_info['status'] = 'trained'
            model_info['updated_at'] = datetime.utcnow().isoformat()
            model_info['metrics'] = result['metrics']
            model_info['training_data'] = {
                'symbol': data['symbol'],
                'timeframe': data['timeframe'],
                'period': data['period']
            }
            
            # Save registry
            self._save_registry()
            
            return {
                'id': model_id,
                'name': model_info['name'],
                'status': model_info['status'],
                'metrics': result['metrics']
            }
        
        except (NotFoundError, ValidationError):
            raise
        
        except Exception as e:
            # Update model status to error
            if model_id in self.model_registry['models']:
                self.model_registry['models'][model_id]['status'] = 'error'
                self._save_registry()
            
            logger.error(f"Error training model: {e}")
            raise ServiceError(f"Error training model: {str(e)}")
    
    def _get_market_data(
        self,
        symbol: str,
        timeframe: str,
        period: str
    ) -> List[Dict[str, Any]]:
        """Get market data from data service
        
        Args:
            symbol: Symbol
            timeframe: Timeframe
            period: Period
            
        Returns:
            Market data
            
        Raises:
            ServiceError: If there is an error getting market data
        """
        try:
            # Get market data from data service
            response = requests.get(
                f"{self.data_service_url}/api/market-data/{symbol}",
                params={
                    'timeframe': timeframe,
                    'period': period
                }
            )
            
            if response.status_code != 200:
                raise ServiceError(f"Error getting market data: {response.text}")
            
            # Parse response
            data = response.json()
            
            return data['data']
        
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            raise ServiceError(f"Error getting market data: {str(e)}")
    
    def _process_data(
        self,
        market_data: List[Dict[str, Any]],
        features: List[str]
    ) -> pd.DataFrame:
        """Process market data
        
        Args:
            market_data: Market data
            features: Features to calculate
            
        Returns:
            Processed data
            
        Raises:
            ServiceError: If there is an error processing data
        """
        try:
            # Get data processor from data service
            from data_service.data_processor import DataProcessor
            
            # Initialize data processor
            data_processor = DataProcessor(self.config_manager, self.db_manager)
            
            # Process data
            processed_data = data_processor.process_market_data(market_data, features)
            
            return processed_data
        
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise ServiceError(f"Error processing data: {str(e)}")
    
    def _train_lstm_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Train LSTM model
        
        Args:
            model_id: Model ID
            model_info: Model info
            data: Processed data
            training_params: Training parameters
            
        Returns:
            Training result
            
        Raises:
            ServiceError: If there is an error training the model
        """
        try:
            # Get parameters
            target_column = training_params.get('target_column', 'close')
            sequence_length = training_params.get('sequence_length', 60)
            target_shift = training_params.get('target_shift', 1)
            test_size = training_params.get('test_size', 0.2)
            epochs = training_params.get('epochs', 100)
            batch_size = training_params.get('batch_size', 32)
            
            # Get data processor from data service
            from data_service.data_processor import DataProcessor
            
            # Initialize data processor
            data_processor = DataProcessor(self.config_manager, self.db_manager)
            
            # Prepare data for ML
            X_train, X_test, y_train, y_test, scaler = data_processor.prepare_data_for_ml(
                df=data,
                target_column=target_column,
                sequence_length=sequence_length,
                target_shift=target_shift,
                test_size=test_size
            )
            
            # Build model
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
            model.add(Dropout(0.2))
            model.add(LSTM(units=50, return_sequences=False))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))
            
            # Compile model
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
            
            # Define callbacks
            callbacks = [
                EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
                ModelCheckpoint(
                    filepath=os.path.join(self.model_dir, f"{model_id}.h5"),
                    monitor='val_loss',
                    save_best_only=True
                )
            ]
            
            # Train model
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test, y_test),
                callbacks=callbacks,
                verbose=1
            )
            
            # Evaluate model
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Save scaler
            with open(os.path.join(self.model_dir, f"{model_id}_scaler.pkl"), 'wb') as f:
                pickle.dump(scaler, f)
            
            # Save model parameters
            model_params = {
                'target_column': target_column,
                'sequence_length': sequence_length,
                'target_shift': target_shift,
                'test_size': test_size,
                'epochs': epochs,
                'batch_size': batch_size,
                'input_shape': X_train.shape[1:]
            }
            
            with open(os.path.join(self.model_dir, f"{model_id}_params.json"), 'w') as f:
                json.dump(model_params, f, indent=2)
            
            # Return result
            return {
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2)
                }
            }
        
        except Exception as e:
            logger.error(f"Error training LSTM model: {e}")
            raise ServiceError(f"Error training LSTM model: {str(e)}")
    
    def _train_cnn_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Train CNN model
        
        Args:
            model_id: Model ID
            model_info: Model info
            data: Processed data
            training_params: Training parameters
            
        Returns:
            Training result
            
        Raises:
            ServiceError: If there is an error training the model
        """
        try:
            # Get parameters
            target_column = training_params.get('target_column', 'close')
            sequence_length = training_params.get('sequence_length', 60)
            target_shift = training_params.get('target_shift', 1)
            test_size = training_params.get('test_size', 0.2)
            epochs = training_params.get('epochs', 100)
            batch_size = training_params.get('batch_size', 32)
            
            # Get data processor from data service
            from data_service.data_processor import DataProcessor
            
            # Initialize data processor
            data_processor = DataProcessor(self.config_manager, self.db_manager)
            
            # Prepare data for ML
            X_train, X_test, y_train, y_test, scaler = data_processor.prepare_data_for_ml(
                df=data,
                target_column=target_column,
                sequence_length=sequence_length,
                target_shift=target_shift,
                test_size=test_size
            )
            
            # Reshape data for CNN
            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)
            
            # Build model
            model = Sequential()
            model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)))
            model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
            model.add(tf.keras.layers.Flatten())
            model.add(Dense(units=50, activation='relu'))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))
            
            # Compile model
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
            
            # Define callbacks
            callbacks = [
                EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
                ModelCheckpoint(
                    filepath=os.path.join(self.model_dir, f"{model_id}.h5"),
                    monitor='val_loss',
                    save_best_only=True
                )
            ]
            
            # Train model
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test, y_test),
                callbacks=callbacks,
                verbose=1
            )
            
            # Evaluate model
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Save scaler
            with open(os.path.join(self.model_dir, f"{model_id}_scaler.pkl"), 'wb') as f:
                pickle.dump(scaler, f)
            
            # Save model parameters
            model_params = {
                'target_column': target_column,
                'sequence_length': sequence_length,
                'target_shift': target_shift,
                'test_size': test_size,
                'epochs': epochs,
                'batch_size': batch_size,
                'input_shape': X_train.shape[1:]
            }
            
            with open(os.path.join(self.model_dir, f"{model_id}_params.json"), 'w') as f:
                json.dump(model_params, f, indent=2)
            
            # Return result
            return {
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2)
                }
            }
        
        except Exception as e:
            logger.error(f"Error training CNN model: {e}")
            raise ServiceError(f"Error training CNN model: {str(e)}")
    
    def _train_transformer_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Train Transformer model
        
        Args:
            model_id: Model ID
            model_info: Model info
            data: Processed data
            training_params: Training parameters
            
        Returns:
            Training result
            
        Raises:
            ServiceError: If there is an error training the model
        """
        try:
            # Get parameters
            target_column = training_params.get('target_column', 'close')
            sequence_length = training_params.get('sequence_length', 60)
            target_shift = training_params.get('target_shift', 1)
            test_size = training_params.get('test_size', 0.2)
            epochs = training_params.get('epochs', 100)
            batch_size = training_params.get('batch_size', 32)
            
            # Get data processor from data service
            from data_service.data_processor import DataProcessor
            
            # Initialize data processor
            data_processor = DataProcessor(self.config_manager, self.db_manager)
            
            # Prepare data for ML
            X_train, X_test, y_train, y_test, scaler = data_processor.prepare_data_for_ml(
                df=data,
                target_column=target_column,
                sequence_length=sequence_length,
                target_shift=target_shift,
                test_size=test_size
            )
            
            # Build model
            def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
                # Attention and Normalization
                x = tf.keras.layers.MultiHeadAttention(
                    key_dim=head_size, num_heads=num_heads, dropout=dropout
                )(inputs, inputs)
                x = tf.keras.layers.Dropout(dropout)(x)
                x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
                res = x + inputs

                # Feed Forward Part
                x = tf.keras.layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(res)
                x = tf.keras.layers.Dropout(dropout)(x)
                x = tf.keras.layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
                x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
                return x + res

            # Build model
            inputs = Input(shape=(X_train.shape[1], X_train.shape[2]))
            x = inputs
            for _ in range(2):
                x = transformer_encoder(x, head_size=256, num_heads=4, ff_dim=512, dropout=0.2)
            x = tf.keras.layers.GlobalAveragePooling1D()(x)
            x = tf.keras.layers.Dense(128, activation="relu")(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            outputs = tf.keras.layers.Dense(1)(x)
            model = Model(inputs=inputs, outputs=outputs)
            
            # Compile model
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
            
            # Define callbacks
            callbacks = [
                EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
                ModelCheckpoint(
                    filepath=os.path.join(self.model_dir, f"{model_id}.h5"),
                    monitor='val_loss',
                    save_best_only=True
                )
            ]
            
            # Train model
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test, y_test),
                callbacks=callbacks,
                verbose=1
            )
            
            # Evaluate model
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Save scaler
            with open(os.path.join(self.model_dir, f"{model_id}_scaler.pkl"), 'wb') as f:
                pickle.dump(scaler, f)
            
            # Save model parameters
            model_params = {
                'target_column': target_column,
                'sequence_length': sequence_length,
                'target_shift': target_shift,
                'test_size': test_size,
                'epochs': epochs,
                'batch_size': batch_size,
                'input_shape': X_train.shape[1:]
            }
            
            with open(os.path.join(self.model_dir, f"{model_id}_params.json"), 'w') as f:
                json.dump(model_params, f, indent=2)
            
            # Return result
            return {
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2)
                }
            }
        
        except Exception as e:
            logger.error(f"Error training Transformer model: {e}")
            raise ServiceError(f"Error training Transformer model: {str(e)}")
    
    def predict(
        self,
        model_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make predictions with a model
        
        Args:
            model_id: Model ID
            data: Prediction data
            
        Returns:
            Prediction result
            
        Raises:
            NotFoundError: If model is not found
            ValidationError: If data is invalid
            ServiceError: If there is an error making predictions
        """
        try:
            # Check if model exists
            if model_id not in self.model_registry['models']:
                raise NotFoundError(f"Model not found: {model_id}")
            
            # Get model info
            model_info = self.model_registry['models'][model_id]
            
            # Check if model is trained
            if model_info['status'] != 'trained':
                raise ValidationError(f"Model is not trained: {model_id}")
            
            # Validate required fields
            if 'symbol' not in data:
                raise ValidationError("Symbol is required")
            
            if 'timeframe' not in data:
                raise ValidationError("Timeframe is required")
            
            if 'period' not in data:
                raise ValidationError("Period is required")
            
            # Get market data
            market_data = self._get_market_data(
                symbol=data['symbol'],
                timeframe=data['timeframe'],
                period=data['period']
            )
            
            # Process data
            processed_data = self._process_data(
                market_data=market_data,
                features=model_info.get('features', [])
            )
            
            # Load model
            model_path = os.path.join(self.model_dir, f"{model_id}.h5")
            
            if not os.path.exists(model_path):
                raise NotFoundError(f"Model file not found: {model_path}")
            
            model = load_model(model_path)
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, f"{model_id}_scaler.pkl")
            
            if not os.path.exists(scaler_path):
                raise NotFoundError(f"Scaler file not found: {scaler_path}")
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            
            # Load parameters
            params_path = os.path.join(self.model_dir, f"{model_id}_params.json")
            
            if not os.path.exists(params_path):
                raise NotFoundError(f"Parameters file not found: {params_path}")
            
            with open(params_path, 'r') as f:
                params = json.load(f)
            
            # Prepare data for prediction
            target_column = params['target_column']
            sequence_length = params['sequence_length']
            
            # Select numeric columns
            numeric_columns = processed_data.select_dtypes(include=[np.number]).columns.tolist()
            
            # Scale data
            scaled_data = scaler.transform(processed_data[numeric_columns])
            
            # Create sequences
            X = []
            
            for i in range(len(scaled_data) - sequence_length):
                X.append(scaled_data[i:i+sequence_length])
            
            X = np.array(X)
            
            # Reshape data for CNN if needed
            if model_info['type'] == 'cnn':
                X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)
            
            # Make predictions
            predictions = model.predict(X)
            
            # Inverse transform predictions
            target_idx = numeric_columns.index(target_column)
            dummy = np.zeros((len(predictions), len(numeric_columns)))
            dummy[:, target_idx] = predictions.flatten()
            predictions_inv = scaler.inverse_transform(dummy)[:, target_idx]
            
            # Create result
            result = {
                'symbol': data['symbol'],
                'timeframe': data['timeframe'],
                'predictions': []
            }
            
            # Add predictions to result
            for i, pred in enumerate(predictions_inv):
                idx = i + sequence_length
                timestamp = processed_data.index[idx].isoformat() if hasattr(processed_data.index[idx], 'isoformat') else str(processed_data.index[idx])
                
                result['predictions'].append({
                    'timestamp': timestamp,
                    'value': float(pred)
                })
            
            return result
        
        except (NotFoundError, ValidationError):
            raise
        
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise ServiceError(f"Error making predictions: {str(e)}")
    
    def delete_model(self, model_id: str) -> Dict[str, Any]:
        """Delete a model
        
        Args:
            model_id: Model ID
            
        Returns:
            Deletion result
            
        Raises:
            NotFoundError: If model is not found
        """
        try:
            # Check if model exists
            if model_id not in self.model_registry['models']:
                raise NotFoundError(f"Model not found: {model_id}")
            
            # Get model info
            model_info = self.model_registry['models'][model_id]
            
            # Delete model files
            model_path = os.path.join(self.model_dir, f"{model_id}.h5")
            scaler_path = os.path.join(self.model_dir, f"{model_id}_scaler.pkl")
            params_path = os.path.join(self.model_dir, f"{model_id}_params.json")
            
            if os.path.exists(model_path):
                os.remove(model_path)
            
            if os.path.exists(scaler_path):
                os.remove(scaler_path)
            
            if os.path.exists(params_path):
                os.remove(params_path)
            
            # Remove from registry
            del self.model_registry['models'][model_id]
            
            # Save registry
            self._save_registry()
            
            return {
                'id': model_id,
                'name': model_info['name'],
                'deleted': True
            }
        
        except NotFoundError:
            raise
        
        except Exception as e:
            logger.error(f"Error deleting model: {e}")
            raise ServiceError(f"Error deleting model: {str(e)}")
    
    def evaluate_model(
        self,
        model_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a model
        
        Args:
            model_id: Model ID
            data: Evaluation data
            
        Returns:
            Evaluation result
            
        Raises:
            NotFoundError: If model is not found
            ValidationError: If data is invalid
            ServiceError: If there is an error evaluating the model
        """
        try:
            # Check if model exists
            if model_id not in self.model_registry['models']:
                raise NotFoundError(f"Model not found: {model_id}")
            
            # Get model info
            model_info = self.model_registry['models'][model_id]
            
            # Check if model is trained
            if model_info['status'] != 'trained':
                raise ValidationError(f"Model is not trained: {model_id}")
            
            # Validate required fields
            if 'symbol' not in data:
                raise ValidationError("Symbol is required")
            
            if 'timeframe' not in data:
                raise ValidationError("Timeframe is required")
            
            if 'period' not in data:
                raise ValidationError("Period is required")
            
            # Get market data
            market_data = self._get_market_data(
                symbol=data['symbol'],
                timeframe=data['timeframe'],
                period=data['period']
            )
            
            # Process data
            processed_data = self._process_data(
                market_data=market_data,
                features=model_info.get('features', [])
            )
            
            # Load model
            model_path = os.path.join(self.model_dir, f"{model_id}.h5")
            
            if not os.path.exists(model_path):
                raise NotFoundError(f"Model file not found: {model_path}")
            
            model = load_model(model_path)
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, f"{model_id}_scaler.pkl")
            
            if not os.path.exists(scaler_path):
                raise NotFoundError(f"Scaler file not found: {scaler_path}")
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            
            # Load parameters
            params_path = os.path.join(self.model_dir, f"{model_id}_params.json")
            
            if not os.path.exists(params_path):
                raise NotFoundError(f"Parameters file not found: {params_path}")
            
            with open(params_path, 'r') as f:
                params = json.load(f)
            
            # Prepare data for evaluation
            target_column = params['target_column']
            sequence_length = params['sequence_length']
            target_shift = params['target_shift']
            
            # Get data processor from data service
            from data_service.data_processor import DataProcessor
            
            # Initialize data processor
            data_processor = DataProcessor(self.config_manager, self.db_manager)
            
            # Prepare data for ML
            X_train, X_test, y_train, y_test, _ = data_processor.prepare_data_for_ml(
                df=processed_data,
                target_column=target_column,
                sequence_length=sequence_length,
                target_shift=target_shift,
                test_size=1.0  # Use all data for testing
            )
            
            # Reshape data for CNN if needed
            if model_info['type'] == 'cnn':
                X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Create result
            result = {
                'symbol': data['symbol'],
                'timeframe': data['timeframe'],
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'mae': float(mae),
                    'r2': float(r2)
                }
            }
            
            return result
        
        except (NotFoundError, ValidationError):
            raise
        
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise ServiceError(f"Error evaluating model: {str(e)}")
    
    def update_model(
        self,
        model_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a model
        
        Args:
            model_id: Model ID
            data: Model data
            
        Returns:
            Updated model
            
        Raises:
            NotFoundError: If model is not found
        """
        try:
            # Check if model exists
            if model_id not in self.model_registry['models']:
                raise NotFoundError(f"Model not found: {model_id}")
            
            # Get model info
            model_info = self.model_registry['models'][model_id]
            
            # Update model info
            if 'name' in data:
                model_info['name'] = data['name']
            
            if 'description' in data:
                model_info['description'] = data['description']
            
            if 'parameters' in data:
                model_info['parameters'] = data['parameters']
            
            if 'features' in data:
                model_info['features'] = data['features']
            
            # Update timestamp
            model_info['updated_at'] = datetime.utcnow().isoformat()
            
            # Save registry
            self._save_registry()
            
            return {
                'id': model_id,
                'name': model_info['name'],
                'description': model_info['description'],
                'type': model_info['type'],
                'status': model_info['status'],
                'created_at': model_info['created_at'],
                'updated_at': model_info['updated_at'],
                'parameters': model_info.get('parameters', {}),
                'features': model_info.get('features', [])
            }
        
        except NotFoundError:
            raise
        
        except Exception as e:
            logger.error(f"Error updating model: {e}")
            raise ServiceError(f"Error updating model: {str(e)}")

