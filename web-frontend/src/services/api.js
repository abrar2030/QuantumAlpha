import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Get the backend URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';

// Define our single API slice
export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: API_BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      // Get the token from auth state
      const token = getState().auth.token;
      
      // If we have a token, add it to the headers
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      
      return headers;
    },
  }),
  tagTypes: ['Portfolio', 'Strategy', 'Trade', 'User'],
  endpoints: (builder) => ({
    // Auth endpoints
    login: builder.mutation({
      query: (credentials) => ({
        url: '/auth/login',
        method: 'POST',
        body: credentials,
      }),
    }),
    register: builder.mutation({
      query: (userData) => ({
        url: '/auth/register',
        method: 'POST',
        body: userData,
      }),
    }),
    getUser: builder.query({
      query: () => '/auth/user',
      providesTags: ['User'],
    }),
    
    // Portfolio endpoints
    getPortfolio: builder.query({
      query: () => '/portfolio',
      providesTags: ['Portfolio'],
    }),
    getPortfolioHistory: builder.query({
      query: (timeframe) => `/portfolio/history?timeframe=${timeframe}`,
      providesTags: ['Portfolio'],
    }),
    
    // Strategy endpoints
    getStrategies: builder.query({
      query: () => '/strategies',
      providesTags: ['Strategy'],
    }),
    getStrategy: builder.query({
      query: (id) => `/strategies/${id}`,
      providesTags: (result, error, id) => [{ type: 'Strategy', id }],
    }),
    createStrategy: builder.mutation({
      query: (strategy) => ({
        url: '/strategies',
        method: 'POST',
        body: strategy,
      }),
      invalidatesTags: ['Strategy'],
    }),
    updateStrategy: builder.mutation({
      query: ({ id, ...patch }) => ({
        url: `/strategies/${id}`,
        method: 'PATCH',
        body: patch,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Strategy', id }],
    }),
    deleteStrategy: builder.mutation({
      query: (id) => ({
        url: `/strategies/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Strategy'],
    }),
    
    // Trade endpoints
    getTrades: builder.query({
      query: (params) => ({
        url: '/trades',
        params,
      }),
      providesTags: ['Trade'],
    }),
    
    // Market data endpoints
    getMarketData: builder.query({
      query: (symbol) => `/market-data/${symbol}`,
    }),
    
    // Risk metrics endpoints
    getRiskMetrics: builder.query({
      query: (strategyId) => `/risk/metrics/${strategyId}`,
    }),
  }),
});

// Export hooks for usage in components
export const {
  useLoginMutation,
  useRegisterMutation,
  useGetUserQuery,
  useGetPortfolioQuery,
  useGetPortfolioHistoryQuery,
  useGetStrategiesQuery,
  useGetStrategyQuery,
  useCreateStrategyMutation,
  useUpdateStrategyMutation,
  useDeleteStrategyMutation,
  useGetTradesQuery,
  useGetMarketDataQuery,
  useGetRiskMetricsQuery,
} = api;

