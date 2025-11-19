// This file would contain the Redux Toolkit store setup.
// Example: configureStore from @reduxjs/toolkit

import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../store/slices/authSlice';
import portfolioReducer from '../store/slices/portfolioSlice';
import strategyReducer from '../store/slices/strategySlice';
import themeReducer from '../store/slices/themeSlice';
import uiReducer from '../store/slices/uiSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    portfolio: portfolioReducer,
    strategy: strategyReducer,
    theme: themeReducer,
    ui: uiReducer,
  },
});

export default store;
