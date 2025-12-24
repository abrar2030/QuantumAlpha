"""
Reinforcement learning service for QuantumAlpha AI Engine.
Handles reinforcement learning models for trading.
"""

import json
import logging
import os
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List
import gym
import numpy as np
import pandas as pd
import requests
from gym import spaces
from stable_baselines3 import A2C, DQN, PPO, SAC
from stable_baselines3.common.vec_env import DummyVecEnv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import NotFoundError, ServiceError, ValidationError, setup_logger
from core.logging import get_logger

logger = get_logger(__name__)
logger = setup_logger("reinforcement_learning", logging.INFO)


class TradingEnvironment(gym.Env):
    """Trading environment for reinforcement learning"""

    def __init__(
        self, df: Any, initial_balance: Any = 10000, transaction_fee: Any = 0.001
    ) -> None:
        """Initialize trading environment

        Args:
            df: DataFrame with market data
            initial_balance: Initial balance
            transaction_fee: Transaction fee
        """
        super(TradingEnvironment, self).__init__()
        self.df = df
        self.initial_balance = initial_balance
        self.transaction_fee = transaction_fee
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(df.shape[1] + 3,), dtype=np.float32
        )
        self.reset()

    def reset(self) -> Any:
        """Reset environment

        Returns:
            Initial observation
        """
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.position_value = 0
        self.done = False
        self.history = []
        return self._get_observation()

    def step(self, action: Any) -> Any:
        """Take a step in the environment

        Args:
            action: Action to take (0: hold, 1: buy, 2: sell)

        Returns:
            Tuple of (observation, reward, done, info)
        """
        current_price = self.df.iloc[self.current_step]["close"]
        reward = 0
        if action == 1:
            if self.balance > 0:
                position_size = self.balance
                fee = position_size * self.transaction_fee
                shares = (position_size - fee) / current_price
                self.position = shares
                self.position_value = self.position * current_price
                self.balance = 0
        elif action == 2:
            if self.position > 0:
                position_value = self.position * current_price
                fee = position_value * self.transaction_fee
                self.balance = position_value - fee
                self.position = 0
                self.position_value = 0
        self.current_step += 1
        if self.current_step >= len(self.df) - 1:
            self.done = True
        if self.done:
            portfolio_value = self.balance + self.position * current_price
            returns = (portfolio_value - self.initial_balance) / self.initial_balance
            reward = returns * 100
        else:
            portfolio_value = self.balance + self.position * current_price
            returns = (portfolio_value - self.initial_balance) / self.initial_balance
            reward = returns * 10
        self.history.append(
            {
                "step": self.current_step,
                "action": action,
                "price": current_price,
                "balance": self.balance,
                "position": self.position,
                "position_value": self.position_value,
                "portfolio_value": self.balance + self.position * current_price,
                "reward": reward,
            }
        )
        observation = self._get_observation()
        return (observation, reward, self.done, {})

    def _get_observation(self) -> Any:
        """Get observation

        Returns:
            Observation
        """
        market_data = self.df.iloc[self.current_step].values
        observation = np.append(
            market_data, [self.balance, self.position, self.position_value]
        )
        return observation

    def render(self, mode: Any = "human") -> Any:
        """Render environment

        Args:
            mode: Rendering mode
        """
        if mode == "human":
            step = (
                self.history[-1]
                if self.history
                else {
                    "step": self.current_step,
                    "action": 0,
                    "price": self.df.iloc[self.current_step]["close"],
                    "balance": self.balance,
                    "position": self.position,
                    "position_value": self.position_value,
                    "portfolio_value": self.balance
                    + self.position * self.df.iloc[self.current_step]["close"],
                    "reward": 0,
                }
            )
            logger.info(f"Step: {step['step']}")
            logger.info(f"Action: {step['action']}")
            logger.info(f"Price: {step['price']}")
            logger.info(f"Balance: {step['balance']}")
            logger.info(f"Position: {step['position']}")
            logger.info(f"Position Value: {step['position_value']}")
            logger.info(f"Portfolio Value: {step['portfolio_value']}")
            logger.info(f"Reward: {step['reward']}")
            logger.info("---")


class ReinforcementLearning:
    """Reinforcement learning service"""

    def __init__(self, config_manager: Any, db_manager: Any) -> None:
        """Initialize reinforcement learning service

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.data_service_url = f"http://{config_manager.get('services.data_service.host')}:{config_manager.get('services.data_service.port')}"
        self.model_dir = config_manager.get(
            "ai_engine.rl_model_dir", "/home/ubuntu/quantumalpha_backend/rl_models"
        )
        os.makedirs(self.model_dir, exist_ok=True)
        self.registry_file = os.path.join(self.model_dir, "registry.json")
        self.model_registry = self._load_registry()
        logger.info("Reinforcement learning service initialized")

    def _load_registry(self) -> Dict[str, Any]:
        """Load model registry

        Returns:
            Model registry
        """
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading model registry: {e}")
                return {"models": {}}
        else:
            return {"models": {}}

    def _save_registry(self) -> None:
        """Save model registry"""
        try:
            with open(self.registry_file, "w") as f:
                json.dump(self.model_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving model registry: {e}")

    def get_models(self) -> List[Dict[str, Any]]:
        """Get all models

        Returns:
            List of models
        """
        models = []
        for model_id, model_info in self.model_registry["models"].items():
            models.append(
                {
                    "id": model_id,
                    "name": model_info["name"],
                    "description": model_info["description"],
                    "algorithm": model_info["algorithm"],
                    "status": model_info["status"],
                    "created_at": model_info["created_at"],
                    "updated_at": model_info["updated_at"],
                    "metrics": model_info.get("metrics", {}),
                }
            )
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
        if model_id not in self.model_registry["models"]:
            raise NotFoundError(f"Model not found: {model_id}")
        model_info = self.model_registry["models"][model_id]
        return {
            "id": model_id,
            "name": model_info["name"],
            "description": model_info["description"],
            "algorithm": model_info["algorithm"],
            "status": model_info["status"],
            "created_at": model_info["created_at"],
            "updated_at": model_info["updated_at"],
            "metrics": model_info.get("metrics", {}),
            "parameters": model_info.get("parameters", {}),
            "features": model_info.get("features", []),
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
            if "name" not in data:
                raise ValidationError("Model name is required")
            if "algorithm" not in data:
                raise ValidationError("Algorithm is required")
            valid_algorithms = ["ppo", "a2c", "dqn", "sac"]
            if data["algorithm"] not in valid_algorithms:
                raise ValidationError(f"Invalid algorithm: {data['algorithm']}")
            model_id = f"rl_model_{uuid.uuid4().hex}"
            model_info = {
                "name": data["name"],
                "description": data.get("description", ""),
                "algorithm": data["algorithm"],
                "status": "created",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "parameters": data.get("parameters", {}),
                "features": data.get("features", []),
            }
            self.model_registry["models"][model_id] = model_info
            self._save_registry()
            return {
                "id": model_id,
                "name": model_info["name"],
                "description": model_info["description"],
                "algorithm": model_info["algorithm"],
                "status": model_info["status"],
                "created_at": model_info["created_at"],
                "updated_at": model_info["updated_at"],
                "parameters": model_info["parameters"],
                "features": model_info["features"],
            }
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise ServiceError(f"Error creating model: {str(e)}")

    def train_model(self, model_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
            if model_id not in self.model_registry["models"]:
                raise NotFoundError(f"Model not found: {model_id}")
            model_info = self.model_registry["models"][model_id]
            if "symbol" not in data:
                raise ValidationError("Symbol is required")
            if "timeframe" not in data:
                raise ValidationError("Timeframe is required")
            if "period" not in data:
                raise ValidationError("Period is required")
            model_info["status"] = "training"
            self._save_registry()
            market_data = self._get_market_data(
                symbol=data["symbol"],
                timeframe=data["timeframe"],
                period=data["period"],
            )
            processed_data = self._process_data(
                market_data=market_data, features=model_info.get("features", [])
            )
            if model_info["algorithm"] == "ppo":
                result = self._train_ppo_model(
                    model_id, model_info, processed_data, data
                )
            elif model_info["algorithm"] == "a2c":
                result = self._train_a2c_model(
                    model_id, model_info, processed_data, data
                )
            elif model_info["algorithm"] == "dqn":
                result = self._train_dqn_model(
                    model_id, model_info, processed_data, data
                )
            elif model_info["algorithm"] == "sac":
                result = self._train_sac_model(
                    model_id, model_info, processed_data, data
                )
            else:
                raise ValidationError(
                    f"Unsupported algorithm: {model_info['algorithm']}"
                )
            model_info["status"] = "trained"
            model_info["updated_at"] = datetime.utcnow().isoformat()
            model_info["metrics"] = result["metrics"]
            model_info["training_data"] = {
                "symbol": data["symbol"],
                "timeframe": data["timeframe"],
                "period": data["period"],
            }
            self._save_registry()
            return {
                "id": model_id,
                "name": model_info["name"],
                "status": model_info["status"],
                "metrics": result["metrics"],
            }
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            if model_id in self.model_registry["models"]:
                self.model_registry["models"][model_id]["status"] = "error"
                self._save_registry()
            logger.error(f"Error training model: {e}")
            raise ServiceError(f"Error training model: {str(e)}")

    def _get_market_data(
        self, symbol: str, timeframe: str, period: str
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
            response = requests.get(
                f"{self.data_service_url}/api/market-data/{symbol}",
                params={"timeframe": timeframe, "period": period},
            )
            if response.status_code != 200:
                raise ServiceError(f"Error getting market data: {response.text}")
            data = response.json()
            return data["data"]
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            raise ServiceError(f"Error getting market data: {str(e)}")

    def _process_data(
        self, market_data: List[Dict[str, Any]], features: List[str]
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
            from data_service.data_processor import DataProcessor

            data_processor = DataProcessor(self.config_manager, self.db_manager)
            processed_data = data_processor.process_market_data(market_data, features)
            return processed_data
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise ServiceError(f"Error processing data: {str(e)}")

    def _train_ppo_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Train PPO model

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
            total_timesteps = training_params.get("total_timesteps", 100000)
            initial_balance = training_params.get("initial_balance", 10000)
            transaction_fee = training_params.get("transaction_fee", 0.001)
            data = data.dropna()
            env = TradingEnvironment(data, initial_balance, transaction_fee)
            env = DummyVecEnv([lambda: env])
            model = PPO(
                "MlpPolicy",
                env,
                verbose=1,
                tensorboard_log=os.path.join(self.model_dir, f"{model_id}_logs"),
            )
            model.learn(total_timesteps=total_timesteps)
            model.save(os.path.join(self.model_dir, f"{model_id}.zip"))
            mean_reward, std_reward = self._evaluate_rl_model(
                model, env, n_eval_episodes=10
            )
            model_params = {
                "total_timesteps": total_timesteps,
                "initial_balance": initial_balance,
                "transaction_fee": transaction_fee,
            }
            with open(
                os.path.join(self.model_dir, f"{model_id}_params.json"), "w"
            ) as f:
                json.dump(model_params, f, indent=2)
            return {
                "metrics": {
                    "mean_reward": float(mean_reward),
                    "std_reward": float(std_reward),
                }
            }
        except Exception as e:
            logger.error(f"Error training PPO model: {e}")
            raise ServiceError(f"Error training PPO model: {str(e)}")

    def _train_a2c_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Train A2C model

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
            total_timesteps = training_params.get("total_timesteps", 100000)
            initial_balance = training_params.get("initial_balance", 10000)
            transaction_fee = training_params.get("transaction_fee", 0.001)
            data = data.dropna()
            env = TradingEnvironment(data, initial_balance, transaction_fee)
            env = DummyVecEnv([lambda: env])
            model = A2C(
                "MlpPolicy",
                env,
                verbose=1,
                tensorboard_log=os.path.join(self.model_dir, f"{model_id}_logs"),
            )
            model.learn(total_timesteps=total_timesteps)
            model.save(os.path.join(self.model_dir, f"{model_id}.zip"))
            mean_reward, std_reward = self._evaluate_rl_model(
                model, env, n_eval_episodes=10
            )
            model_params = {
                "total_timesteps": total_timesteps,
                "initial_balance": initial_balance,
                "transaction_fee": transaction_fee,
            }
            with open(
                os.path.join(self.model_dir, f"{model_id}_params.json"), "w"
            ) as f:
                json.dump(model_params, f, indent=2)
            return {
                "metrics": {
                    "mean_reward": float(mean_reward),
                    "std_reward": float(std_reward),
                }
            }
        except Exception as e:
            logger.error(f"Error training A2C model: {e}")
            raise ServiceError(f"Error training A2C model: {str(e)}")

    def _train_dqn_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Train DQN model

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
            total_timesteps = training_params.get("total_timesteps", 100000)
            initial_balance = training_params.get("initial_balance", 10000)
            transaction_fee = training_params.get("transaction_fee", 0.001)
            data = data.dropna()
            env = TradingEnvironment(data, initial_balance, transaction_fee)
            model = DQN(
                "MlpPolicy",
                env,
                verbose=1,
                tensorboard_log=os.path.join(self.model_dir, f"{model_id}_logs"),
            )
            model.learn(total_timesteps=total_timesteps)
            model.save(os.path.join(self.model_dir, f"{model_id}.zip"))
            mean_reward, std_reward = self._evaluate_rl_model(
                model, env, n_eval_episodes=10
            )
            model_params = {
                "total_timesteps": total_timesteps,
                "initial_balance": initial_balance,
                "transaction_fee": transaction_fee,
            }
            with open(
                os.path.join(self.model_dir, f"{model_id}_params.json"), "w"
            ) as f:
                json.dump(model_params, f, indent=2)
            return {
                "metrics": {
                    "mean_reward": float(mean_reward),
                    "std_reward": float(std_reward),
                }
            }
        except Exception as e:
            logger.error(f"Error training DQN model: {e}")
            raise ServiceError(f"Error training DQN model: {str(e)}")

    def _train_sac_model(
        self,
        model_id: str,
        model_info: Dict[str, Any],
        data: pd.DataFrame,
        training_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Train SAC model

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
            total_timesteps = training_params.get("total_timesteps", 100000)
            initial_balance = training_params.get("initial_balance", 10000)
            transaction_fee = training_params.get("transaction_fee", 0.001)
            data = data.dropna()
            env = TradingEnvironment(data, initial_balance, transaction_fee)
            model = SAC(
                "MlpPolicy",
                env,
                verbose=1,
                tensorboard_log=os.path.join(self.model_dir, f"{model_id}_logs"),
            )
            model.learn(total_timesteps=total_timesteps)
            model.save(os.path.join(self.model_dir, f"{model_id}.zip"))
            mean_reward, std_reward = self._evaluate_rl_model(
                model, env, n_eval_episodes=10
            )
            model_params = {
                "total_timesteps": total_timesteps,
                "initial_balance": initial_balance,
                "transaction_fee": transaction_fee,
            }
            with open(
                os.path.join(self.model_dir, f"{model_id}_params.json"), "w"
            ) as f:
                json.dump(model_params, f, indent=2)
            return {
                "metrics": {
                    "mean_reward": float(mean_reward),
                    "std_reward": float(std_reward),
                }
            }
        except Exception as e:
            logger.error(f"Error training SAC model: {e}")
            raise ServiceError(f"Error training SAC model: {str(e)}")

    def _evaluate_rl_model(
        self, model: Any, env: Any, n_eval_episodes: int = 10
    ) -> tuple:
        """Evaluate reinforcement learning model

        Args:
            model: Model
            env: Environment
            n_eval_episodes: Number of evaluation episodes

        Returns:
            Tuple of (mean_reward, std_reward)
        """
        obs = env.reset()
        rewards = []
        for _ in range(n_eval_episodes):
            obs = env.reset()
            done = False
            episode_reward = 0
            while not done:
                action, _ = model.predict(obs)
                obs, reward, done, _ = env.step(action)
                episode_reward += reward
            rewards.append(episode_reward)
        mean_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        return (mean_reward, std_reward)

    def predict(self, model_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
            if model_id not in self.model_registry["models"]:
                raise NotFoundError(f"Model not found: {model_id}")
            model_info = self.model_registry["models"][model_id]
            if model_info["status"] != "trained":
                raise ValidationError(f"Model is not trained: {model_id}")
            if "symbol" not in data:
                raise ValidationError("Symbol is required")
            if "timeframe" not in data:
                raise ValidationError("Timeframe is required")
            if "period" not in data:
                raise ValidationError("Period is required")
            market_data = self._get_market_data(
                symbol=data["symbol"],
                timeframe=data["timeframe"],
                period=data["period"],
            )
            processed_data = self._process_data(
                market_data=market_data, features=model_info.get("features", [])
            )
            processed_data = processed_data.dropna()
            params_path = os.path.join(self.model_dir, f"{model_id}_params.json")
            if not os.path.exists(params_path):
                raise NotFoundError(f"Parameters file not found: {params_path}")
            with open(params_path, "r") as f:
                params = json.load(f)
            env = TradingEnvironment(
                processed_data,
                params.get("initial_balance", 10000),
                params.get("transaction_fee", 0.001),
            )
            model_path = os.path.join(self.model_dir, f"{model_id}.zip")
            if not os.path.exists(model_path):
                raise NotFoundError(f"Model file not found: {model_path}")
            if model_info["algorithm"] == "ppo":
                model = PPO.load(model_path)
            elif model_info["algorithm"] == "a2c":
                model = A2C.load(model_path)
            elif model_info["algorithm"] == "dqn":
                model = DQN.load(model_path)
            elif model_info["algorithm"] == "sac":
                model = SAC.load(model_path)
            else:
                raise ValidationError(
                    f"Unsupported algorithm: {model_info['algorithm']}"
                )
            obs = env.reset()
            done = False
            actions = []
            while not done:
                action, _ = model.predict(obs)
                obs, reward, done, _ = env.step(action)
                actions.append(int(action))
            history = env.history
            result = {
                "symbol": data["symbol"],
                "timeframe": data["timeframe"],
                "initial_balance": params.get("initial_balance", 10000),
                "final_balance": history[-1]["portfolio_value"],
                "return": (
                    history[-1]["portfolio_value"]
                    - params.get("initial_balance", 10000)
                )
                / params.get("initial_balance", 10000),
                "actions": actions,
                "history": history,
            }
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
            if model_id not in self.model_registry["models"]:
                raise NotFoundError(f"Model not found: {model_id}")
            model_info = self.model_registry["models"][model_id]
            model_path = os.path.join(self.model_dir, f"{model_id}.zip")
            params_path = os.path.join(self.model_dir, f"{model_id}_params.json")
            if os.path.exists(model_path):
                os.remove(model_path)
            if os.path.exists(params_path):
                os.remove(params_path)
            del self.model_registry["models"][model_id]
            self._save_registry()
            return {"id": model_id, "name": model_info["name"], "deleted": True}
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting model: {e}")
            raise ServiceError(f"Error deleting model: {str(e)}")

    def update_model(self, model_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
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
            if model_id not in self.model_registry["models"]:
                raise NotFoundError(f"Model not found: {model_id}")
            model_info = self.model_registry["models"][model_id]
            if "name" in data:
                model_info["name"] = data["name"]
            if "description" in data:
                model_info["description"] = data["description"]
            if "parameters" in data:
                model_info["parameters"] = data["parameters"]
            if "features" in data:
                model_info["features"] = data["features"]
            model_info["updated_at"] = datetime.utcnow().isoformat()
            self._save_registry()
            return {
                "id": model_id,
                "name": model_info["name"],
                "description": model_info["description"],
                "algorithm": model_info["algorithm"],
                "status": model_info["status"],
                "created_at": model_info["created_at"],
                "updated_at": model_info["updated_at"],
                "parameters": model_info.get("parameters", {}),
                "features": model_info.get("features", []),
            }
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating model: {e}")
            raise ServiceError(f"Error updating model: {str(e)}")
