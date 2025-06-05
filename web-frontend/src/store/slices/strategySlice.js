import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  strategies: [
    { name: 'Momentum Alpha', return: 8.2, sharpe: 1.8, drawdown: -3.5 },
    { name: 'Sentiment Trader', return: 5.7, sharpe: 1.5, drawdown: -2.8 },
    { name: 'ML Predictor', return: 12.3, sharpe: 2.1, drawdown: -5.2 },
    { name: 'Mean Reversion', return: 6.9, sharpe: 1.6, drawdown: -4.1 },
  ],
  activeStrategy: null,
  recentTrades: [
    { id: 1, symbol: 'AAPL', type: 'BUY', quantity: 100, price: 182.63, timestamp: '2023-06-15 10:32:45' },
    { id: 2, symbol: 'MSFT', type: 'SELL', quantity: 50, price: 337.42, timestamp: '2023-06-15 11:15:22' },
    { id: 3, symbol: 'GOOGL', type: 'BUY', quantity: 25, price: 125.23, timestamp: '2023-06-15 13:45:10' },
  ],
  loading: false,
  error: null,
};

const strategySlice = createSlice({
  name: 'strategy',
  initialState,
  reducers: {
    fetchStrategiesStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchStrategiesSuccess: (state, action) => {
      state.strategies = action.payload;
      state.loading = false;
    },
    fetchStrategiesFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    setActiveStrategy: (state, action) => {
      state.activeStrategy = action.payload;
    },
    updateStrategyPerformance: (state, action) => {
      const { name, performance } = action.payload;
      const strategyIndex = state.strategies.findIndex(strategy => strategy.name === name);
      if (strategyIndex !== -1) {
        state.strategies[strategyIndex] = { ...state.strategies[strategyIndex], ...performance };
      }
    },
    addTrade: (state, action) => {
      state.recentTrades.unshift(action.payload);
      // Keep only the most recent trades
      if (state.recentTrades.length > 10) {
        state.recentTrades.pop();
      }
    },
  },
});

export const {
  fetchStrategiesStart,
  fetchStrategiesSuccess,
  fetchStrategiesFailure,
  setActiveStrategy,
  updateStrategyPerformance,
  addTrade,
} = strategySlice.actions;

export default strategySlice.reducer;
