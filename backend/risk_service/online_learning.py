"""
Online learning module for QuantumAlpha Risk Service.
Handles real-time model updates and adaptive risk modeling.
"""
import os
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDRegressor, PassiveAggressiveRegressor
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle
import json

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
logger = setup_logger('online_learning', logging.INFO)

class OnlineLearningEngine:
    """Online learning engine for adaptive risk modeling"""
    
    def __init__(self, config_manager, db_manager):
        """Initialize online learning engine
        
        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        
        # Initialize models
        self.models = {
            'volatility_predictor': SGDRegressor(
                learning_rate='adaptive',
                eta0=0.01,
                max_iter=1000,
                random_state=42
            ),
            'return_predictor': SGDRegressor(
                learning_rate='adaptive',
                eta0=0.01,
                max_iter=1000,
                random_state=42
            ),
            'correlation_predictor': SGDRegressor(
                learning_rate='adaptive',
                eta0=0.01,
                max_iter=1000,
                random_state=42
            ),
            'anomaly_detector': IsolationForest(
                contamination=0.1,
                random_state=42
            )
        }
        
        # Initialize scalers
        self.scalers = {
            'volatility': StandardScaler(),
            'return': StandardScaler(),
            'correlation': StandardScaler(),
            'anomaly': StandardScaler()
        }
        
        # Model performance tracking
        self.model_performance = {
            'volatility_predictor': {'mse': [], 'mae': [], 'last_updated': None},
            'return_predictor': {'mse': [], 'mae': [], 'last_updated': None},
            'correlation_predictor': {'mse': [], 'mae': [], 'last_updated': None},
            'anomaly_detector': {'accuracy': [], 'last_updated': None}
        }
        
        # Feature engineering parameters
        self.feature_windows = [5, 10, 20, 50]  # Different lookback windows
        self.decay_factor = 0.94  # For exponential weighting
        
        # Model persistence
        self.model_save_path = "/tmp/quantum_alpha_models"
        os.makedirs(self.model_save_path, exist_ok=True)
        
        logger.info("Online learning engine initialized")
    
    def update_models(
        self,
        market_data: Dict[str, List[Dict[str, Any]]],
        portfolio_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Update models with new market data
        
        Args:
            market_data: Dictionary of symbol -> historical data
            portfolio_data: Optional portfolio positions for context
            
        Returns:
            Update results
        """
        try:
            logger.info("Updating online learning models")
            
            # Prepare features and targets
            features, targets = self._prepare_training_data(market_data)
            
            if len(features) == 0:
                logger.warning("No features prepared for model update")
                return {'status': 'no_update', 'reason': 'insufficient_data'}
            
            # Update each model
            update_results = {}
            
            # Update volatility predictor
            if 'volatility' in targets and len(targets['volatility']) > 0:
                vol_result = self._update_volatility_model(
                    features['volatility'], 
                    targets['volatility']
                )
                update_results['volatility_predictor'] = vol_result
            
            # Update return predictor
            if 'returns' in targets and len(targets['returns']) > 0:
                ret_result = self._update_return_model(
                    features['returns'], 
                    targets['returns']
                )
                update_results['return_predictor'] = ret_result
            
            # Update correlation predictor
            if 'correlation' in targets and len(targets['correlation']) > 0:
                corr_result = self._update_correlation_model(
                    features['correlation'], 
                    targets['correlation']
                )
                update_results['correlation_predictor'] = corr_result
            
            # Update anomaly detector
            if 'anomaly' in features and len(features['anomaly']) > 0:
                anom_result = self._update_anomaly_model(features['anomaly'])
                update_results['anomaly_detector'] = anom_result
            
            # Save updated models
            self._save_models()
            
            # Create response
            response = {
                'status': 'success',
                'models_updated': list(update_results.keys()),
                'update_results': update_results,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            return response
        
        except Exception as e:
            logger.error(f"Error updating models: {e}")
            raise ServiceError(f"Error updating models: {str(e)}")
    
    def predict_volatility(
        self,
        symbol: str,
        features: np.ndarray,
        horizon: int = 1
    ) -> Dict[str, Any]:
        """Predict volatility using online learning model
        
        Args:
            symbol: Symbol to predict for
            features: Feature vector
            horizon: Prediction horizon in days
            
        Returns:
            Volatility prediction
        """
        try:
            # Scale features
            scaled_features = self.scalers['volatility'].transform(features.reshape(1, -1))
            
            # Make prediction
            prediction = self.models['volatility_predictor'].predict(scaled_features)[0]
            
            # Adjust for horizon (simple scaling, could be more sophisticated)
            adjusted_prediction = prediction * np.sqrt(horizon)
            
            # Calculate confidence interval (simplified)
            model_performance = self.model_performance['volatility_predictor']
            recent_mse = np.mean(model_performance['mse'][-10:]) if model_performance['mse'] else 0.01
            confidence_interval = 1.96 * np.sqrt(recent_mse)  # 95% CI
            
            return {
                'symbol': symbol,
                'predicted_volatility': float(adjusted_prediction),
                'horizon_days': horizon,
                'confidence_interval': {
                    'lower': float(adjusted_prediction - confidence_interval),
                    'upper': float(adjusted_prediction + confidence_interval)
                },
                'model_performance': {
                    'recent_mse': float(recent_mse),
                    'last_updated': model_performance['last_updated']
                },
                'predicted_at': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error predicting volatility: {e}")
            raise ServiceError(f"Error predicting volatility: {str(e)}")
    
    def detect_market_anomalies(
        self,
        market_data: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Detect market anomalies using online learning
        
        Args:
            market_data: Current market data
            
        Returns:
            Anomaly detection results
        """
        try:
            logger.info("Detecting market anomalies")
            
            # Prepare features for anomaly detection
            features = self._prepare_anomaly_features(market_data)
            
            if len(features) == 0:
                return {'anomalies_detected': False, 'reason': 'insufficient_data'}
            
            # Scale features
            scaled_features = self.scalers['anomaly'].transform(features)
            
            # Detect anomalies
            anomaly_scores = self.models['anomaly_detector'].decision_function(scaled_features)
            anomaly_predictions = self.models['anomaly_detector'].predict(scaled_features)
            
            # Identify anomalous symbols
            anomalous_symbols = []
            symbols = list(market_data.keys())
            
            for i, (symbol, score, prediction) in enumerate(zip(symbols, anomaly_scores, anomaly_predictions)):
                if prediction == -1:  # Anomaly detected
                    anomalous_symbols.append({
                        'symbol': symbol,
                        'anomaly_score': float(score),
                        'severity': 'high' if score < -0.5 else 'medium' if score < -0.2 else 'low'
                    })
            
            return {
                'anomalies_detected': len(anomalous_symbols) > 0,
                'anomalous_symbols': anomalous_symbols,
                'total_symbols_analyzed': len(symbols),
                'detection_threshold': -0.1,
                'detected_at': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            raise ServiceError(f"Error detecting anomalies: {str(e)}")
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Get performance metrics for all models
        
        Returns:
            Model performance metrics
        """
        performance_summary = {}
        
        for model_name, performance in self.model_performance.items():
            if model_name == 'anomaly_detector':
                recent_accuracy = np.mean(performance['accuracy'][-10:]) if performance['accuracy'] else 0.0
                performance_summary[model_name] = {
                    'recent_accuracy': float(recent_accuracy),
                    'total_updates': len(performance['accuracy']),
                    'last_updated': performance['last_updated']
                }
            else:
                recent_mse = np.mean(performance['mse'][-10:]) if performance['mse'] else 0.0
                recent_mae = np.mean(performance['mae'][-10:]) if performance['mae'] else 0.0
                performance_summary[model_name] = {
                    'recent_mse': float(recent_mse),
                    'recent_mae': float(recent_mae),
                    'total_updates': len(performance['mse']),
                    'last_updated': performance['last_updated']
                }
        
        return {
            'model_performance': performance_summary,
            'retrieved_at': datetime.utcnow().isoformat()
        }
    
    def _prepare_training_data(
        self,
        market_data: Dict[str, List[Dict[str, Any]]]
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
        """Prepare training data from market data
        
        Args:
            market_data: Raw market data
            
        Returns:
            Tuple of (features, targets)
        """
        features = {}
        targets = {}
        
        # Process each symbol
        for symbol, data in market_data.items():
            if len(data) < max(self.feature_windows) + 1:
                continue
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Calculate returns
            df['returns'] = df['close'].pct_change()
            
            # Calculate rolling volatility
            for window in self.feature_windows:
                df[f'volatility_{window}'] = df['returns'].rolling(window).std()
                df[f'mean_return_{window}'] = df['returns'].rolling(window).mean()
                df[f'volume_ma_{window}'] = df['volume'].rolling(window).mean()
            
            # Prepare volatility features and targets
            vol_features = []
            vol_targets = []
            
            for i in range(max(self.feature_windows), len(df) - 1):
                # Features: lagged volatilities, returns, volume
                feature_vector = []
                for window in self.feature_windows:
                    feature_vector.extend([
                        df.iloc[i][f'volatility_{window}'],
                        df.iloc[i][f'mean_return_{window}'],
                        df.iloc[i][f'volume_ma_{window}']
                    ])
                
                # Add recent price changes
                feature_vector.extend([
                    df.iloc[i]['returns'],
                    df.iloc[i-1]['returns'],
                    df.iloc[i-2]['returns'] if i >= 2 else 0
                ])
                
                vol_features.append(feature_vector)
                
                # Target: next period volatility
                next_vol = abs(df.iloc[i+1]['returns'])
                vol_targets.append(next_vol)
            
            # Store features and targets
            if vol_features:
                if 'volatility' not in features:
                    features['volatility'] = []
                    targets['volatility'] = []
                
                features['volatility'].extend(vol_features)
                targets['volatility'].extend(vol_targets)
        
        # Convert to numpy arrays
        for key in features:
            features[key] = np.array(features[key])
            targets[key] = np.array(targets[key])
        
        # Prepare return prediction features (similar structure)
        features['returns'] = features.get('volatility', np.array([]))
        targets['returns'] = targets.get('volatility', np.array([]))  # Simplified
        
        # Prepare correlation features (simplified)
        features['correlation'] = features.get('volatility', np.array([]))
        targets['correlation'] = targets.get('volatility', np.array([]))  # Simplified
        
        # Prepare anomaly detection features
        features['anomaly'] = features.get('volatility', np.array([]))
        
        return features, targets
    
    def _prepare_anomaly_features(
        self,
        market_data: Dict[str, List[Dict[str, Any]]]
    ) -> np.ndarray:
        """Prepare features for anomaly detection
        
        Args:
            market_data: Current market data
            
        Returns:
            Feature matrix for anomaly detection
        """
        features = []
        
        for symbol, data in market_data.items():
            if len(data) < 5:  # Need minimum data
                continue
            
            # Get recent data
            recent_data = data[-5:]  # Last 5 periods
            
            # Calculate features
            prices = [d['close'] for d in recent_data]
            volumes = [d['volume'] for d in recent_data]
            
            # Price-based features
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns)
            mean_return = np.mean(returns)
            
            # Volume-based features
            volume_ratio = volumes[-1] / np.mean(volumes[:-1]) if len(volumes) > 1 else 1.0
            
            # Technical indicators
            price_change = (prices[-1] - prices[0]) / prices[0]
            
            feature_vector = [
                volatility,
                mean_return,
                volume_ratio,
                price_change,
                prices[-1]  # Current price level
            ]
            
            features.append(feature_vector)
        
        return np.array(features) if features else np.array([])
    
    def _update_volatility_model(
        self,
        features: np.ndarray,
        targets: np.ndarray
    ) -> Dict[str, Any]:
        """Update volatility prediction model
        
        Args:
            features: Training features
            targets: Training targets
            
        Returns:
            Update results
        """
        try:
            # Remove any NaN or infinite values
            valid_indices = np.isfinite(features).all(axis=1) & np.isfinite(targets)
            features = features[valid_indices]
            targets = targets[valid_indices]
            
            if len(features) == 0:
                return {'status': 'no_update', 'reason': 'no_valid_data'}
            
            # Fit scaler if not already fitted
            if not hasattr(self.scalers['volatility'], 'scale_'):
                self.scalers['volatility'].fit(features)
            
            # Scale features
            scaled_features = self.scalers['volatility'].transform(features)
            
            # Partial fit (online learning)
            self.models['volatility_predictor'].partial_fit(scaled_features, targets)
            
            # Evaluate performance
            predictions = self.models['volatility_predictor'].predict(scaled_features)
            mse = mean_squared_error(targets, predictions)
            mae = mean_absolute_error(targets, predictions)
            
            # Update performance tracking
            self.model_performance['volatility_predictor']['mse'].append(mse)
            self.model_performance['volatility_predictor']['mae'].append(mae)
            self.model_performance['volatility_predictor']['last_updated'] = datetime.utcnow().isoformat()
            
            return {
                'status': 'updated',
                'samples_processed': len(features),
                'mse': float(mse),
                'mae': float(mae)
            }
        
        except Exception as e:
            logger.error(f"Error updating volatility model: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _update_return_model(
        self,
        features: np.ndarray,
        targets: np.ndarray
    ) -> Dict[str, Any]:
        """Update return prediction model
        
        Args:
            features: Training features
            targets: Training targets
            
        Returns:
            Update results
        """
        try:
            # Similar to volatility model update
            valid_indices = np.isfinite(features).all(axis=1) & np.isfinite(targets)
            features = features[valid_indices]
            targets = targets[valid_indices]
            
            if len(features) == 0:
                return {'status': 'no_update', 'reason': 'no_valid_data'}
            
            if not hasattr(self.scalers['return'], 'scale_'):
                self.scalers['return'].fit(features)
            
            scaled_features = self.scalers['return'].transform(features)
            self.models['return_predictor'].partial_fit(scaled_features, targets)
            
            predictions = self.models['return_predictor'].predict(scaled_features)
            mse = mean_squared_error(targets, predictions)
            mae = mean_absolute_error(targets, predictions)
            
            self.model_performance['return_predictor']['mse'].append(mse)
            self.model_performance['return_predictor']['mae'].append(mae)
            self.model_performance['return_predictor']['last_updated'] = datetime.utcnow().isoformat()
            
            return {
                'status': 'updated',
                'samples_processed': len(features),
                'mse': float(mse),
                'mae': float(mae)
            }
        
        except Exception as e:
            logger.error(f"Error updating return model: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _update_correlation_model(
        self,
        features: np.ndarray,
        targets: np.ndarray
    ) -> Dict[str, Any]:
        """Update correlation prediction model
        
        Args:
            features: Training features
            targets: Training targets
            
        Returns:
            Update results
        """
        try:
            # Similar to other model updates
            valid_indices = np.isfinite(features).all(axis=1) & np.isfinite(targets)
            features = features[valid_indices]
            targets = targets[valid_indices]
            
            if len(features) == 0:
                return {'status': 'no_update', 'reason': 'no_valid_data'}
            
            if not hasattr(self.scalers['correlation'], 'scale_'):
                self.scalers['correlation'].fit(features)
            
            scaled_features = self.scalers['correlation'].transform(features)
            self.models['correlation_predictor'].partial_fit(scaled_features, targets)
            
            predictions = self.models['correlation_predictor'].predict(scaled_features)
            mse = mean_squared_error(targets, predictions)
            mae = mean_absolute_error(targets, predictions)
            
            self.model_performance['correlation_predictor']['mse'].append(mse)
            self.model_performance['correlation_predictor']['mae'].append(mae)
            self.model_performance['correlation_predictor']['last_updated'] = datetime.utcnow().isoformat()
            
            return {
                'status': 'updated',
                'samples_processed': len(features),
                'mse': float(mse),
                'mae': float(mae)
            }
        
        except Exception as e:
            logger.error(f"Error updating correlation model: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _update_anomaly_model(self, features: np.ndarray) -> Dict[str, Any]:
        """Update anomaly detection model
        
        Args:
            features: Training features
            
        Returns:
            Update results
        """
        try:
            # Remove any NaN or infinite values
            valid_indices = np.isfinite(features).all(axis=1)
            features = features[valid_indices]
            
            if len(features) == 0:
                return {'status': 'no_update', 'reason': 'no_valid_data'}
            
            # Fit scaler if not already fitted
            if not hasattr(self.scalers['anomaly'], 'scale_'):
                self.scalers['anomaly'].fit(features)
            
            # Scale features
            scaled_features = self.scalers['anomaly'].transform(features)
            
            # Fit anomaly detector (IsolationForest doesn't support partial_fit)
            # In a real system, you might use a streaming anomaly detection algorithm
            self.models['anomaly_detector'].fit(scaled_features)
            
            # Evaluate (simplified - in practice you'd need labeled anomaly data)
            predictions = self.models['anomaly_detector'].predict(scaled_features)
            anomaly_rate = np.sum(predictions == -1) / len(predictions)
            
            # Update performance tracking (simplified)
            self.model_performance['anomaly_detector']['accuracy'].append(1.0 - anomaly_rate)
            self.model_performance['anomaly_detector']['last_updated'] = datetime.utcnow().isoformat()
            
            return {
                'status': 'updated',
                'samples_processed': len(features),
                'anomaly_rate': float(anomaly_rate)
            }
        
        except Exception as e:
            logger.error(f"Error updating anomaly model: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _save_models(self) -> None:
        """Save models and scalers to disk"""
        try:
            # Save models
            for model_name, model in self.models.items():
                model_path = os.path.join(self.model_save_path, f"{model_name}.pkl")
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
            
            # Save scalers
            for scaler_name, scaler in self.scalers.items():
                scaler_path = os.path.join(self.model_save_path, f"scaler_{scaler_name}.pkl")
                with open(scaler_path, 'wb') as f:
                    pickle.dump(scaler, f)
            
            # Save performance metrics
            performance_path = os.path.join(self.model_save_path, "performance.json")
            with open(performance_path, 'w') as f:
                json.dump(self.model_performance, f, indent=2)
            
            logger.debug("Models saved successfully")
        
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self) -> bool:
        """Load models and scalers from disk
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load models
            for model_name in self.models.keys():
                model_path = os.path.join(self.model_save_path, f"{model_name}.pkl")
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
            
            # Load scalers
            for scaler_name in self.scalers.keys():
                scaler_path = os.path.join(self.model_save_path, f"scaler_{scaler_name}.pkl")
                if os.path.exists(scaler_path):
                    with open(scaler_path, 'rb') as f:
                        self.scalers[scaler_name] = pickle.load(f)
            
            # Load performance metrics
            performance_path = os.path.join(self.model_save_path, "performance.json")
            if os.path.exists(performance_path):
                with open(performance_path, 'r') as f:
                    self.model_performance = json.load(f)
            
            logger.info("Models loaded successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

