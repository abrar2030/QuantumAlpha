import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  portfolioValue: 11500,
  dailyChange: 300,
  percentChange: 2.68,
  historicalData: [
    { name: 'Jan', value: 10000 },
    { name: 'Feb', value: 10200 },
    { name: 'Mar', value: 10150 },
    { name: 'Apr', value: 10400 },
    { name: 'May', value: 10800 },
    { name: 'Jun', value: 11200 },
    { name: 'Jul', value: 11500 },
  ],
  assets: [],
  loading: false,
  error: null,
};

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    fetchPortfolioStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchPortfolioSuccess: (state, action) => {
      state.portfolioValue = action.payload.portfolioValue;
      state.dailyChange = action.payload.dailyChange;
      state.percentChange = action.payload.percentChange;
      state.historicalData = action.payload.historicalData;
      state.assets = action.payload.assets;
      state.loading = false;
    },
    fetchPortfolioFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    updatePortfolioValue: (state, action) => {
      state.portfolioValue = action.payload.value;
      state.dailyChange = action.payload.dailyChange;
      state.percentChange = action.payload.percentChange;
    },
    addHistoricalDataPoint: (state, action) => {
      state.historicalData.push(action.payload);
    },
  },
});

export const {
  fetchPortfolioStart,
  fetchPortfolioSuccess,
  fetchPortfolioFailure,
  updatePortfolioValue,
  addHistoricalDataPoint,
} = portfolioSlice.actions;

export default portfolioSlice.reducer;
