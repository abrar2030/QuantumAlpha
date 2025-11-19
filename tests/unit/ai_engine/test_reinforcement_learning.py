"""
Unit tests for the AI Engine's Reinforcement Learning module.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

# Add project root to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import module to test
try:
    from backend.ai_engine.reinforcement_learning import (RLAgent,
                                                          RLEnvironment,
                                                          RLTrainer)
    from backend.common.exceptions import (NotFoundError, ServiceError,
                                           ValidationError)
except ImportError:
    # Mock the classes for testing when imports fail
    class RLAgent:
        pass

    class RLEnvironment:
        pass

    class RLTrainer:
        pass

    class NotFoundError(Exception):
        pass

    class ValidationError(Exception):
        pass

    class ServiceError(Exception):
        pass


class TestRLEnvironment(unittest.TestCase):
    """Unit tests for RLEnvironment class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create sample market data
        self.market_data = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=100),
                "open": np.random.normal(100, 2, 100),
                "high": np.random.normal(102, 2, 100),
                "low": np.random.normal(98, 2, 100),
                "close": np.random.normal(100, 2, 100),
                "volume": np.random.normal(1000000, 100000, 100),
                "symbol": "AAPL",
            }
        )

        # Create environment
        self.env = RLEnvironment(
            data=self.market_data,
            initial_balance=10000.0,
            transaction_fee=0.001,
            window_size=10,
        )

    def test_init(self):
        """Test RLEnvironment initialization."""
        env = RLEnvironment(
            data=self.market_data,
            initial_balance=10000.0,
            transaction_fee=0.001,
            window_size=10,
        )

        # Check attributes
        self.assertEqual(env.initial_balance, 10000.0)
        self.assertEqual(env.balance, 10000.0)
        self.assertEqual(env.transaction_fee, 0.001)
        self.assertEqual(env.window_size, 10)
        self.assertEqual(env.current_step, 0)
        self.assertEqual(env.position, 0)
        self.assertEqual(env.position_price, 0.0)
        self.assertEqual(env.total_reward, 0.0)
        self.assertEqual(env.done, False)

    def test_reset(self):
        """Test environment reset."""
        # Make some changes to the environment
        self.env.balance = 9000.0
        self.env.current_step = 50
        self.env.position = 100
        self.env.position_price = 95.0
        self.env.total_reward = 500.0
        self.env.done = True

        # Reset environment
        state = self.env.reset()

        # Check if environment was reset
        self.assertEqual(self.env.balance, 10000.0)
        self.assertEqual(self.env.current_step, 0)
        self.assertEqual(self.env.position, 0)
        self.assertEqual(self.env.position_price, 0.0)
        self.assertEqual(self.env.total_reward, 0.0)
        self.assertEqual(self.env.done, False)

        # Check state
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(state.shape[0], self.env.window_size)

    def test_step_buy(self):
        """Test environment step with buy action."""
        # Reset environment
        self.env.reset()

        # Get initial balance
        initial_balance = self.env.balance

        # Take buy action
        state, reward, done, info = self.env.step(1)  # 1 = buy

        # Check state
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(state.shape[0], self.env.window_size)

        # Check reward
        self.assertIsInstance(reward, float)

        # Check done
        self.assertIsInstance(done, bool)

        # Check info
        self.assertIsInstance(info, dict)
        self.assertIn("balance", info)
        self.assertIn("position", info)
        self.assertIn("position_value", info)
        self.assertIn("total_value", info)

        # Check if position was opened
        self.assertGreater(self.env.position, 0)
        self.assertGreater(self.env.position_price, 0.0)

        # Check if balance was reduced
        self.assertLess(self.env.balance, initial_balance)

    def test_step_sell(self):
        """Test environment step with sell action."""
        # Reset environment
        self.env.reset()

        # Take buy action first
        self.env.step(1)  # 1 = buy

        # Get balance and position after buy
        balance_after_buy = self.env.balance
        self.env.position

        # Take sell action
        state, reward, done, info = self.env.step(2)  # 2 = sell

        # Check state
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(state.shape[0], self.env.window_size)

        # Check reward
        self.assertIsInstance(reward, float)

        # Check done
        self.assertIsInstance(done, bool)

        # Check info
        self.assertIsInstance(info, dict)
        self.assertIn("balance", info)
        self.assertIn("position", info)
        self.assertIn("position_value", info)
        self.assertIn("total_value", info)

        # Check if position was closed
        self.assertEqual(self.env.position, 0)
        self.assertEqual(self.env.position_price, 0.0)

        # Check if balance was increased
        self.assertGreater(self.env.balance, balance_after_buy)

    def test_step_hold(self):
        """Test environment step with hold action."""
        # Reset environment
        self.env.reset()

        # Get initial balance and step
        initial_balance = self.env.balance
        initial_step = self.env.current_step

        # Take hold action
        state, reward, done, info = self.env.step(0)  # 0 = hold

        # Check state
        self.assertIsInstance(state, np.ndarray)
        self.assertEqual(state.shape[0], self.env.window_size)

        # Check reward
        self.assertIsInstance(reward, float)

        # Check done
        self.assertIsInstance(done, bool)

        # Check info
        self.assertIsInstance(info, dict)
        self.assertIn("balance", info)
        self.assertIn("position", info)
        self.assertIn("position_value", info)
        self.assertIn("total_value", info)

        # Check if position remained the same
        self.assertEqual(self.env.position, 0)
        self.assertEqual(self.env.position_price, 0.0)

        # Check if balance remained the same
        self.assertEqual(self.env.balance, initial_balance)

        # Check if step was incremented
        self.assertEqual(self.env.current_step, initial_step + 1)

    def test_step_done(self):
        """Test environment step until done."""
        # Reset environment
        self.env.reset()

        # Run until done
        done = False
        while not done:
            _, _, done, _ = self.env.step(0)  # 0 = hold

        # Check if done
        self.assertTrue(self.env.done)

        # Check if current_step is at the end
        self.assertEqual(self.env.current_step, len(self.env.data) - 1)


class TestRLAgent(unittest.TestCase):
    """Unit tests for RLAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "ai_engine": {
                "model_dir": "/tmp/models",
                "registry_file": "/tmp/models/registry.json",
            }
        }

        # Create mock database manager
        self.db_manager = MagicMock()

        # Create agent
        self.agent = RLAgent(
            state_size=10,
            action_size=3,
            model_id="rl_model1",
            config_manager=self.config_manager,
            db_manager=self.db_manager,
        )

    def test_init(self):
        """Test RLAgent initialization."""
        agent = RLAgent(
            state_size=10,
            action_size=3,
            model_id="rl_model1",
            config_manager=self.config_manager,
            db_manager=self.db_manager,
        )

        # Check attributes
        self.assertEqual(agent.state_size, 10)
        self.assertEqual(agent.action_size, 3)
        self.assertEqual(agent.model_id, "rl_model1")
        self.assertEqual(agent.config_manager, self.config_manager)
        self.assertEqual(agent.db_manager, self.db_manager)
        self.assertIsNotNone(agent.model)
        self.assertIsNotNone(agent.target_model)
        self.assertIsNotNone(agent.memory)

    @patch("numpy.random.rand")
    def test_act_explore(self, mock_rand):
        """Test agent act method with exploration."""
        # Set up mock to return a value less than epsilon
        mock_rand.return_value = 0.01  # Less than default epsilon (0.1)

        # Create state
        state = np.random.random((1, 10))

        # Get action
        action = self.agent.act(state)

        # Check action
        self.assertIsInstance(action, int)
        self.assertGreaterEqual(action, 0)
        self.assertLess(action, 3)

    @patch("numpy.random.rand")
    def test_act_exploit(self, mock_rand):
        """Test agent act method with exploitation."""
        # Set up mock to return a value greater than epsilon
        mock_rand.return_value = 0.9  # Greater than default epsilon (0.1)

        # Mock model predict
        self.agent.model.predict = MagicMock(return_value=np.array([[0.1, 0.8, 0.1]]))

        # Create state
        state = np.random.random((1, 10))

        # Get action
        action = self.agent.act(state)

        # Check action
        self.assertEqual(action, 1)  # Should choose action with highest Q-value

    def test_remember(self):
        """Test agent remember method."""
        # Create experience
        state = np.random.random(10)
        action = 1
        reward = 0.5
        next_state = np.random.random(10)
        done = False

        # Remember experience
        self.agent.remember(state, action, reward, next_state, done)

        # Check if experience was added to memory
        self.assertEqual(len(self.agent.memory), 1)

    @patch("numpy.random.choice")
    def test_replay(self, mock_choice):
        """Test agent replay method."""
        # Create experiences
        batch_size = 32
        experiences = []

        for _ in range(batch_size):
            state = np.random.random(10)
            action = np.random.randint(0, 3)
            reward = np.random.random()
            next_state = np.random.random(10)
            done = np.random.choice([True, False])
            experiences.append((state, action, reward, next_state, done))

        # Add experiences to memory
        for exp in experiences:
            self.agent.memory.append(exp)

        # Set up mock to return all experiences
        mock_choice.return_value = np.arange(batch_size)

        # Mock model predict
        self.agent.model.predict = MagicMock(
            return_value=np.random.random((batch_size, 3))
        )
        self.agent.target_model.predict = MagicMock(
            return_value=np.random.random((batch_size, 3))
        )

        # Replay experiences
        self.agent.replay(batch_size)

        # Check if model was trained
        self.agent.model.fit.assert_called_once()

    def test_load_model(self):
        """Test agent load_model method."""
        # Mock os.path.exists
        with patch("os.path.exists", return_value=True):
            # Mock load_model
            with patch("tensorflow.keras.models.load_model") as mock_load_model:
                # Load model
                self.agent.load_model()

                # Check if load_model was called
                mock_load_model.assert_called()

    def test_save_model(self):
        """Test agent save_model method."""
        # Mock os.path.exists
        with patch("os.path.exists", return_value=True):
            # Mock model save
            self.agent.model.save = MagicMock()

            # Save model
            self.agent.save_model()

            # Check if model.save was called
            self.agent.model.save.assert_called_once()


class TestRLTrainer(unittest.TestCase):
    """Unit tests for RLTrainer class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "ai_engine": {
                "model_dir": "/tmp/models",
                "registry_file": "/tmp/models/registry.json",
            }
        }

        # Create mock database manager
        self.db_manager = MagicMock()

        # Create sample market data
        self.market_data = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=100),
                "open": np.random.normal(100, 2, 100),
                "high": np.random.normal(102, 2, 100),
                "low": np.random.normal(98, 2, 100),
                "close": np.random.normal(100, 2, 100),
                "volume": np.random.normal(1000000, 100000, 100),
                "symbol": "AAPL",
            }
        )

        # Create trainer
        self.trainer = RLTrainer(
            config_manager=self.config_manager, db_manager=self.db_manager
        )

    def test_init(self):
        """Test RLTrainer initialization."""
        trainer = RLTrainer(
            config_manager=self.config_manager, db_manager=self.db_manager
        )

        # Check attributes
        self.assertEqual(trainer.config_manager, self.config_manager)
        self.assertEqual(trainer.db_manager, self.db_manager)

    @patch("backend.ai_engine.reinforcement_learning.RLEnvironment")
    @patch("backend.ai_engine.reinforcement_learning.RLAgent")
    def test_train(self, mock_agent_class, mock_env_class):
        """Test trainer train method."""
        # Set up mock environment
        mock_env = MagicMock()
        mock_env.reset.return_value = np.random.random(10)
        mock_env.step.return_value = (np.random.random(10), 0.5, False, {})
        mock_env_class.return_value = mock_env

        # Set up mock agent
        mock_agent = MagicMock()
        mock_agent.act.return_value = 1
        mock_agent_class.return_value = mock_agent

        # Train agent
        result = self.trainer.train(
            model_id="rl_model1",
            data=self.market_data,
            episodes=2,
            batch_size=32,
            window_size=10,
            initial_balance=10000.0,
            transaction_fee=0.001,
        )

        # Check result
        self.assertIsInstance(result, dict)
        self.assertIn("model_id", result)
        self.assertIn("episodes", result)
        self.assertIn("final_reward", result)
        self.assertIn("training_time", result)

        # Check if agent methods were called
        mock_agent.act.assert_called()
        mock_agent.remember.assert_called()
        mock_agent.replay.assert_called()
        mock_agent.save_model.assert_called_once()

    @patch("backend.ai_engine.reinforcement_learning.RLEnvironment")
    @patch("backend.ai_engine.reinforcement_learning.RLAgent")
    def test_evaluate(self, mock_agent_class, mock_env_class):
        """Test trainer evaluate method."""
        # Set up mock environment
        mock_env = MagicMock()
        mock_env.reset.return_value = np.random.random(10)
        mock_env.step.return_value = (
            np.random.random(10),
            0.5,
            False,
            {
                "balance": 10000.0,
                "position": 0,
                "position_value": 0.0,
                "total_value": 10000.0,
            },
        )
        mock_env_class.return_value = mock_env

        # Set up mock agent
        mock_agent = MagicMock()
        mock_agent.act.return_value = 1
        mock_agent_class.return_value = mock_agent

        # Evaluate agent
        result = self.trainer.evaluate(
            model_id="rl_model1",
            data=self.market_data,
            window_size=10,
            initial_balance=10000.0,
            transaction_fee=0.001,
        )

        # Check result
        self.assertIsInstance(result, dict)
        self.assertIn("model_id", result)
        self.assertIn("initial_balance", result)
        self.assertIn("final_balance", result)
        self.assertIn("total_reward", result)
        self.assertIn("profit", result)
        self.assertIn("profit_percent", result)
        self.assertIn("trades", result)

        # Check if agent methods were called
        mock_agent.act.assert_called()
        mock_agent.load_model.assert_called_once()


if __name__ == "__main__":
    unittest.main()
