import React, { useState } from 'react';
import { 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Button, 
  Card,
  CardContent,
  useTheme,
  useMediaQuery,
  Skeleton,
  Alert,
  Fade
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useGetPortfolioQuery, useGetStrategiesQuery, useGetTradesQuery } from '../services/api';
import PortfolioSummary from '../components/dashboard/PortfolioSummary';
import PerformanceChart from '../components/dashboard/PerformanceChart';
import StrategyTable from '../components/dashboard/StrategyTable';
import RecentTradesList from '../components/dashboard/RecentTradesList';
import ErrorBoundary from '../components/common/ErrorBoundary';
import { toggleModal } from '../store/slices/uiSlice';

const Dashboard = () => {
  const theme = useTheme();
  const dispatch = useDispatch();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Get data from Redux store and API
  const { portfolioValue, dailyChange, percentChange, historicalData } = useSelector((state) => state.portfolio);
  const { strategies, recentTrades } = useSelector((state) => state.strategy);
  
  // RTK Query hooks with automatic loading and error states
  const { 
    data: portfolioData, 
    isLoading: portfolioLoading, 
    error: portfolioError 
  } = useGetPortfolioQuery();
  
  const { 
    data: strategiesData, 
    isLoading: strategiesLoading, 
    error: strategiesError 
  } = useGetStrategiesQuery();
  
  const { 
    data: tradesData, 
    isLoading: tradesLoading, 
    error: tradesError 
  } = useGetTradesQuery({ limit: 5 });

  // Handle deposit/withdraw modals
  const handleOpenDepositModal = () => {
    dispatch(toggleModal({ modal: 'deposit', value: true }));
  };

  const handleOpenWithdrawModal = () => {
    dispatch(toggleModal({ modal: 'withdraw', value: true }));
  };

  return (
    <ErrorBoundary>
      <Container maxWidth="xl" sx={{ animation: 'fadeIn 0.5s ease-in-out' }}>
        {/* Portfolio Summary */}
        <Fade in={true} timeout={800}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: { xs: 2, md: 3 }, 
              mb: 3, 
              borderRadius: 2,
              background: 'linear-gradient(to right, rgba(30,30,30,0.95), rgba(40,40,40,0.9))',
              backdropFilter: 'blur(10px)',
              boxShadow: '0 4px 20px rgba(0,0,0,0.25)'
            }}
          >
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                {portfolioLoading ? (
                  <>
                    <Skeleton variant="text" width="60%" height={40} />
                    <Skeleton variant="text" width="40%" height={60} />
                    <Skeleton variant="text" width="30%" height={30} />
                  </>
                ) : portfolioError ? (
                  <Alert severity="error">Error loading portfolio data</Alert>
                ) : (
                  <PortfolioSummary 
                    portfolioValue={portfolioData?.portfolioValue || portfolioValue}
                    dailyChange={portfolioData?.dailyChange || dailyChange}
                    percentChange={portfolioData?.percentChange || percentChange}
                  />
                )}
              </Grid>
              <Grid item xs={12} md={6}>
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: { xs: 'center', md: 'flex-end' }, 
                  gap: 2,
                  mt: { xs: 2, md: 0 }
                }}>
                  <Button 
                    variant="contained" 
                    color="primary"
                    size={isMobile ? "medium" : "large"}
                    onClick={handleOpenDepositModal}
                    sx={{ 
                      px: 3,
                      py: 1,
                      fontWeight: 600,
                      boxShadow: '0 4px 10px rgba(26, 255, 146, 0.3)',
                      '&:hover': {
                        boxShadow: '0 6px 14px rgba(26, 255, 146, 0.4)',
                      }
                    }}
                  >
                    Deposit Funds
                  </Button>
                  <Button 
                    variant="outlined" 
                    color="primary"
                    size={isMobile ? "medium" : "large"}
                    onClick={handleOpenWithdrawModal}
                    sx={{ 
                      px: 3,
                      py: 1,
                      fontWeight: 600,
                      borderWidth: 2,
                      '&:hover': {
                        borderWidth: 2,
                      }
                    }}
                  >
                    Withdraw
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Fade>

        {/* Performance Chart */}
        <Fade in={true} timeout={1000}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: { xs: 2, md: 3 }, 
              mb: 3, 
              borderRadius: 2,
              boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
            }}
          >
            <Typography variant="h5" gutterBottom fontWeight="600">
              Portfolio Performance
            </Typography>
            {portfolioLoading ? (
              <Skeleton variant="rectangular" width="100%" height={300} />
            ) : portfolioError ? (
              <Alert severity="error">Error loading performance data</Alert>
            ) : (
              <PerformanceChart 
                data={portfolioData?.historicalData || historicalData} 
                height={300}
              />
            )}
          </Paper>
        </Fade>

        {/* Strategy Performance and Recent Trades */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={7}>
            <Fade in={true} timeout={1200}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: { xs: 2, md: 3 }, 
                  height: '100%', 
                  borderRadius: 2,
                  boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
                }}
              >
                <Typography variant="h5" gutterBottom fontWeight="600">
                  Strategy Performance
                </Typography>
                {strategiesLoading ? (
                  <>
                    <Skeleton variant="rectangular" width="100%" height={50} />
                    <Skeleton variant="rectangular" width="100%" height={50} sx={{ mt: 1 }} />
                    <Skeleton variant="rectangular" width="100%" height={50} sx={{ mt: 1 }} />
                    <Skeleton variant="rectangular" width="100%" height={50} sx={{ mt: 1 }} />
                  </>
                ) : strategiesError ? (
                  <Alert severity="error">Error loading strategy data</Alert>
                ) : (
                  <StrategyTable strategies={strategiesData || strategies} />
                )}
              </Paper>
            </Fade>
          </Grid>
          <Grid item xs={12} md={5}>
            <Fade in={true} timeout={1400}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: { xs: 2, md: 3 }, 
                  height: '100%', 
                  borderRadius: 2,
                  boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
                }}
              >
                <Typography variant="h5" gutterBottom fontWeight="600">
                  Recent Trades
                </Typography>
                {tradesLoading ? (
                  <>
                    <Skeleton variant="rectangular" width="100%" height={80} sx={{ mb: 2, borderRadius: 1 }} />
                    <Skeleton variant="rectangular" width="100%" height={80} sx={{ mb: 2, borderRadius: 1 }} />
                    <Skeleton variant="rectangular" width="100%" height={80} sx={{ borderRadius: 1 }} />
                  </>
                ) : tradesError ? (
                  <Alert severity="error">Error loading trade data</Alert>
                ) : (
                  <RecentTradesList trades={tradesData || recentTrades} />
                )}
              </Paper>
            </Fade>
          </Grid>
        </Grid>
      </Container>
    </ErrorBoundary>
  );
};

export default Dashboard;
