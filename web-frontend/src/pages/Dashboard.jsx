import React, { useState, useEffect, useRef } from 'react';
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
  Fade,
  Chip,
  LinearProgress,
  Avatar,
  IconButton,
  Tooltip,
  Divider,
  Slide,
  Zoom,
  Grow,
  Collapse,
  Badge,
  Stack
} from '@mui/material';
import { 
  TrendingUp, 
  TrendingDown, 
  AccountBalance, 
  ShowChart, 
  Speed,
  Timeline,
  Analytics,
  AutoGraph,
  Insights,
  MonetizationOn,
  Assessment,
  Refresh,
  Fullscreen,
  Settings,
  NotificationsActive,
  Bolt,
  Psychology,
  Rocket,
  Star,
  FlashOn,
  TrendingFlat,
  AttachMoney,
  BarChart as BarChartIcon,
  CandlestickChart,
  DataUsage,
  ElectricBolt,
  Equalizer
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, RadialBarChart, RadialBar, ComposedChart } from 'recharts';
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
  const [animationKey, setAnimationKey] = useState(0);
  const [realTimeData, setRealTimeData] = useState({});
  const [particlePositions, setParticlePositions] = useState([]);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [marketPulse, setMarketPulse] = useState(0);
  const canvasRef = useRef(null);
  
  // Get data from Redux store and API
  const { portfolioValue, dailyChange, percentChange, historicalData } = useSelector((state) => state.portfolio);
  const { strategies, recentTrades } = useSelector((state) => state.strategy);
  
  // RTK Query hooks with automatic loading and error states
  const { 
    data: portfolioData, 
    isLoading: portfolioLoading, 
    error: portfolioError,
    refetch: refetchPortfolio
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

  // Initialize floating particles
  useEffect(() => {
    const particles = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 3 + 1,
      opacity: Math.random() * 0.5 + 0.1
    }));
    setParticlePositions(particles);
  }, []);

  // Animate particles
  useEffect(() => {
    const animateParticles = () => {
      setParticlePositions(prev => prev.map(particle => ({
        ...particle,
        x: (particle.x + particle.vx + window.innerWidth) % window.innerWidth,
        y: (particle.y + particle.vy + window.innerHeight) % window.innerHeight,
        opacity: 0.1 + Math.sin(Date.now() * 0.001 + particle.id) * 0.2
      })));
    };

    const interval = setInterval(animateParticles, 50);
    return () => clearInterval(interval);
  }, []);

  // Real-time updates and market pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
      setRealTimeData({
        timestamp: new Date().toLocaleTimeString(),
        change: (Math.random() - 0.5) * 2,
        volume: Math.floor(Math.random() * 1000000),
        price: 1250000 + (Math.random() - 0.5) * 50000
      });
      setMarketPulse(prev => (prev + 1) % 100);
      setAnimationKey(prev => prev + 1);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Handle deposit/withdraw modals
  const handleOpenDepositModal = () => {
    dispatch(toggleModal({ modal: 'deposit', value: true }));
  };

  const handleOpenWithdrawModal = () => {
    dispatch(toggleModal({ modal: 'withdraw', value: true }));
  };

  const handleRefresh = () => {
    refetchPortfolio();
    setAnimationKey(prev => prev + 1);
  };

  // Extract strategies array from API response
  const strategiesArray = strategiesData?.success ? strategiesData.data : (strategies || []);

  // Advanced mock data
  const marketOverviewData = [
    { name: 'AI/Tech', value: 35, color: '#00f5ff', growth: '+12.5%' },
    { name: 'DeFi', value: 25, color: '#1de9b6', growth: '+8.3%' },
    { name: 'Quantum', value: 20, color: '#ff6d00', growth: '+15.7%' },
    { name: 'Biotech', value: 12, color: '#e91e63', growth: '+6.2%' },
    { name: 'Space', value: 8, color: '#9c27b0', growth: '+22.1%' }
  ];

  const performanceMetrics = [
    { 
      label: 'AI Score', 
      value: '98.5', 
      trend: 'up', 
      color: 'success',
      icon: Psychology,
      description: 'Neural Network Confidence',
      change: '+2.3%'
    },
    { 
      label: 'Quantum Edge', 
      value: '87.2%', 
      trend: 'up', 
      color: 'info',
      icon: Bolt,
      description: 'Quantum Algorithm Performance',
      change: '+5.1%'
    },
    { 
      label: 'Risk Shield', 
      value: '99.1%', 
      trend: 'up', 
      color: 'success',
      icon: Star,
      description: 'Advanced Risk Protection',
      change: '+0.8%'
    },
    { 
      label: 'Alpha Gen', 
      value: '156%', 
      trend: 'up', 
      color: 'warning',
      icon: Rocket,
      description: 'Alpha Generation Rate',
      change: '+12.4%'
    }
  ];

  const advancedChartData = [
    { time: '09:00', portfolio: 1200000, benchmark: 1180000, ai_prediction: 1220000 },
    { time: '10:00', portfolio: 1215000, benchmark: 1185000, ai_prediction: 1235000 },
    { time: '11:00', portfolio: 1230000, benchmark: 1190000, ai_prediction: 1250000 },
    { time: '12:00', portfolio: 1245000, benchmark: 1195000, ai_prediction: 1265000 },
    { time: '13:00', portfolio: 1250000, benchmark: 1200000, ai_prediction: 1270000 }
  ];

  return (
    <ErrorBoundary>
      {/* Animated Background */}
      <Box sx={{ 
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: `
          radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
          radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%),
          linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0a0a0a 100%)
        `,
        zIndex: -2
      }}>
        {/* Floating Particles */}
        {particlePositions.map(particle => (
          <Box
            key={particle.id}
            sx={{
              position: 'absolute',
              left: particle.x,
              top: particle.y,
              width: particle.size,
              height: particle.size,
              borderRadius: '50%',
              background: `linear-gradient(45deg, #00f5ff, #1de9b6)`,
              opacity: particle.opacity,
              boxShadow: `0 0 ${particle.size * 2}px rgba(0, 245, 255, 0.5)`,
              animation: 'twinkle 2s ease-in-out infinite alternate'
            }}
          />
        ))}
      </Box>

      {/* Neural Network Grid Overlay */}
      <Box sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundImage: `
          linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px)
        `,
        backgroundSize: '50px 50px',
        zIndex: -1,
        animation: 'gridPulse 4s ease-in-out infinite'
      }} />

      <Box sx={{ 
        minHeight: '100vh',
        pb: 4,
        position: 'relative',
        zIndex: 1
      }}>
        <Container maxWidth="xl" sx={{ pt: 3 }}>
          {/* Futuristic Header */}
          <Fade in={true} timeout={800}>
            <Box sx={{ mb: 4, position: 'relative' }}>
              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                mb: 3,
                p: 3,
                borderRadius: 4,
                background: 'linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(29, 233, 182, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(0, 245, 255, 0.3)',
                boxShadow: '0 8px 32px rgba(0, 245, 255, 0.2)'
              }}>
                <Box>
                  <Typography variant="h2" sx={{ 
                    fontWeight: 900, 
                    background: 'linear-gradient(45deg, #00f5ff, #1de9b6, #ff6d00)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    mb: 1,
                    textShadow: '0 0 30px rgba(0, 245, 255, 0.5)',
                    animation: 'glow 2s ease-in-out infinite alternate'
                  }}>
                    QuantumAlpha
                  </Typography>
                  <Typography variant="h5" sx={{ 
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontWeight: 300,
                    letterSpacing: '2px'
                  }}>
                    Next-Generation AI Trading Intelligence
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Chip 
                      icon={<Psychology />} 
                      label="AI POWERED" 
                      sx={{ 
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        color: 'black',
                        fontWeight: 700,
                        animation: 'pulse 2s infinite'
                      }}
                    />
                    <Chip 
                      icon={<Bolt />} 
                      label="QUANTUM ENHANCED" 
                      sx={{ 
                        background: 'linear-gradient(45deg, #ff6d00, #e91e63)',
                        color: 'white',
                        fontWeight: 700
                      }}
                    />
                    <Chip 
                      icon={<Rocket />} 
                      label="REAL-TIME" 
                      sx={{ 
                        background: 'linear-gradient(45deg, #9c27b0, #673ab7)',
                        color: 'white',
                        fontWeight: 700
                      }}
                    />
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="Neural Refresh">
                      <IconButton onClick={handleRefresh} sx={{ 
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        color: 'black',
                        width: 56,
                        height: 56,
                        '&:hover': { 
                          transform: 'scale(1.1) rotate(180deg)',
                          boxShadow: '0 0 20px rgba(0, 245, 255, 0.8)'
                        },
                        transition: 'all 0.3s ease'
                      }}>
                        <Refresh />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Quantum Alerts">
                      <Badge badgeContent={3} color="error">
                        <IconButton sx={{ 
                          color: '#00f5ff',
                          width: 56,
                          height: 56,
                          border: '2px solid #00f5ff',
                          '&:hover': { 
                            background: 'rgba(0, 245, 255, 0.1)',
                            transform: 'scale(1.1)'
                          }
                        }}>
                          <NotificationsActive />
                        </IconButton>
                      </Badge>
                    </Tooltip>
                  </Box>
                  <Typography variant="caption" sx={{ 
                    color: 'rgba(255, 255, 255, 0.6)',
                    textAlign: 'center'
                  }}>
                    {currentTime.toLocaleTimeString()}
                  </Typography>
                </Box>
              </Box>
              
              {/* Advanced Status Bar */}
              <Paper sx={{ 
                p: 3, 
                background: 'linear-gradient(90deg, rgba(0, 245, 255, 0.1) 0%, rgba(29, 233, 182, 0.1) 50%, rgba(255, 109, 0, 0.1) 100%)',
                border: '1px solid rgba(0, 245, 255, 0.3)',
                borderRadius: 3,
                backdropFilter: 'blur(20px)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
              }}>
                <Grid container spacing={3} alignItems="center">
                  <Grid item xs={12} md={3}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Box sx={{ 
                        width: 12, 
                        height: 12, 
                        borderRadius: '50%',
                        background: '#1de9b6',
                        boxShadow: '0 0 10px #1de9b6',
                        animation: 'pulse 1s infinite'
                      }} />
                      <Typography variant="h6" fontWeight={700} color="#1de9b6">
                        NEURAL NETWORK ACTIVE
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <ElectricBolt sx={{ color: '#00f5ff' }} />
                      <Typography variant="body1" color="white">
                        Quantum Processing: {marketPulse}%
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <DataUsage sx={{ color: '#ff6d00' }} />
                      <Typography variant="body1" color="white">
                        Market Volume: {realTimeData.volume?.toLocaleString() || '0'}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <LinearProgress 
                      variant="determinate" 
                      value={marketPulse} 
                      sx={{ 
                        height: 8, 
                        borderRadius: 4,
                        background: 'rgba(255, 255, 255, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #00f5ff, #1de9b6, #ff6d00)',
                          borderRadius: 4
                        }
                      }} 
                    />
                  </Grid>
                </Grid>
              </Paper>
            </Box>
          </Fade>

          {/* Advanced Metrics Grid */}
          <Fade in={true} timeout={1000}>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              {performanceMetrics.map((metric, index) => (
                <Grid item xs={12} sm={6} lg={3} key={index}>
                  <Zoom in={true} timeout={1000 + index * 200}>
                    <Card sx={{ 
                      background: `linear-gradient(135deg, 
                        rgba(0, 245, 255, 0.1) 0%, 
                        rgba(29, 233, 182, 0.1) 50%, 
                        rgba(255, 109, 0, 0.1) 100%
                      )`,
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(0, 245, 255, 0.3)',
                      borderRadius: 4,
                      transition: 'all 0.3s ease',
                      position: 'relative',
                      overflow: 'hidden',
                      '&:hover': { 
                        transform: 'translateY(-10px) scale(1.02)',
                        boxShadow: '0 20px 40px rgba(0, 245, 255, 0.3)',
                        border: '1px solid rgba(0, 245, 255, 0.6)'
                      }
                    }}>
                      {/* Animated Background */}
                      <Box sx={{
                        position: 'absolute',
                        top: -50,
                        right: -50,
                        width: 100,
                        height: 100,
                        borderRadius: '50%',
                        background: `linear-gradient(45deg, ${metric.color === 'success' ? '#1de9b6' : metric.color === 'info' ? '#00f5ff' : '#ff6d00'}, transparent)`,
                        opacity: 0.1,
                        animation: 'rotate 10s linear infinite'
                      }} />
                      
                      <CardContent sx={{ p: 3 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                          <Box>
                            <Typography variant="body2" sx={{ 
                              color: 'rgba(255, 255, 255, 0.7)',
                              fontWeight: 600,
                              letterSpacing: '1px'
                            }}>
                              {metric.label}
                            </Typography>
                            <Typography variant="h4" fontWeight={900} sx={{ 
                              background: `linear-gradient(45deg, ${
                                metric.color === 'success' ? '#1de9b6, #00f5ff' : 
                                metric.color === 'info' ? '#00f5ff, #1de9b6' : 
                                '#ff6d00, #e91e63'
                              })`,
                              backgroundClip: 'text',
                              WebkitBackgroundClip: 'text',
                              WebkitTextFillColor: 'transparent'
                            }}>
                              {metric.value}
                            </Typography>
                            <Typography variant="caption" color="rgba(255, 255, 255, 0.6)">
                              {metric.description}
                            </Typography>
                          </Box>
                          <Avatar sx={{ 
                            bgcolor: 'transparent',
                            border: `2px solid ${
                              metric.color === 'success' ? '#1de9b6' : 
                              metric.color === 'info' ? '#00f5ff' : 
                              '#ff6d00'
                            }`,
                            width: 56,
                            height: 56,
                            color: metric.color === 'success' ? '#1de9b6' : 
                                   metric.color === 'info' ? '#00f5ff' : 
                                   '#ff6d00'
                          }}>
                            <metric.icon fontSize="large" />
                          </Avatar>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Chip 
                            label={metric.change}
                            size="small"
                            sx={{ 
                              background: metric.color === 'success' ? 'rgba(29, 233, 182, 0.2)' : 
                                         metric.color === 'info' ? 'rgba(0, 245, 255, 0.2)' : 
                                         'rgba(255, 109, 0, 0.2)',
                              color: metric.color === 'success' ? '#1de9b6' : 
                                     metric.color === 'info' ? '#00f5ff' : 
                                     '#ff6d00',
                              fontWeight: 700
                            }}
                          />
                          <TrendingUp sx={{ 
                            color: '#1de9b6',
                            animation: 'bounce 2s infinite'
                          }} />
                        </Box>
                      </CardContent>
                    </Card>
                  </Zoom>
                </Grid>
              ))}
            </Grid>
          </Fade>

          {/* Quantum Portfolio Overview */}
          <Fade in={true} timeout={1200}>
            <Paper 
              elevation={0}
              sx={{ 
                p: 4, 
                mb: 4, 
                borderRadius: 6,
                background: `
                  linear-gradient(135deg, 
                    rgba(0, 245, 255, 0.15) 0%, 
                    rgba(29, 233, 182, 0.15) 25%,
                    rgba(255, 109, 0, 0.15) 50%,
                    rgba(233, 30, 99, 0.15) 75%,
                    rgba(156, 39, 176, 0.15) 100%
                  )
                `,
                border: '2px solid rgba(0, 245, 255, 0.3)',
                position: 'relative',
                overflow: 'hidden',
                backdropFilter: 'blur(30px)',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
              }}
            >
              {/* Animated Quantum Particles */}
              <Box sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: `
                  radial-gradient(circle at 25% 25%, rgba(0, 245, 255, 0.1) 0%, transparent 50%),
                  radial-gradient(circle at 75% 75%, rgba(29, 233, 182, 0.1) 0%, transparent 50%)
                `,
                animation: 'quantumPulse 3s ease-in-out infinite'
              }} />
              
              <Grid container spacing={4} alignItems="center">
                <Grid item xs={12} md={8}>
                  {portfolioLoading ? (
                    <Box>
                      <Skeleton variant="text" width="60%" height={80} />
                      <Skeleton variant="text" width="40%" height={100} />
                      <Skeleton variant="text" width="30%" height={60} />
                    </Box>
                  ) : portfolioError ? (
                    <Alert severity="error" sx={{ borderRadius: 3 }}>
                      Quantum connection error - Reconnecting...
                    </Alert>
                  ) : (
                    <Box sx={{ position: 'relative', zIndex: 2 }}>
                      <Typography variant="h3" fontWeight={900} gutterBottom sx={{
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        textShadow: '0 0 30px rgba(0, 245, 255, 0.5)'
                      }}>
                        Quantum Portfolio
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 3, mb: 3 }}>
                        <Typography variant="h1" fontWeight={900} sx={{ 
                          background: 'linear-gradient(45deg, #ffffff, #00f5ff)',
                          backgroundClip: 'text',
                          WebkitBackgroundClip: 'text',
                          WebkitTextFillColor: 'transparent',
                          fontSize: { xs: '2.5rem', md: '4rem' },
                          textShadow: '0 0 50px rgba(255, 255, 255, 0.3)'
                        }}>
                          ${(portfolioData?.data?.total_value || 1250000).toLocaleString()}
                        </Typography>
                        <Chip 
                          label={`+${(portfolioData?.data?.daily_change_percent || 1.28).toFixed(2)}%`}
                          icon={<TrendingUp />}
                          sx={{ 
                            fontSize: '1.2rem', 
                            fontWeight: 700,
                            px: 2,
                            py: 1,
                            background: 'linear-gradient(45deg, #1de9b6, #00f5ff)',
                            color: 'black',
                            boxShadow: '0 0 20px rgba(29, 233, 182, 0.5)',
                            animation: 'glow 2s ease-in-out infinite alternate'
                          }}
                        />
                      </Box>
                      <Typography variant="h5" sx={{ 
                        color: '#1de9b6',
                        fontWeight: 700,
                        textShadow: '0 0 20px rgba(29, 233, 182, 0.5)'
                      }}>
                        +${(portfolioData?.data?.daily_change || 15750).toLocaleString()} Neural Gains Today
                      </Typography>
                      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                        <Chip 
                          icon={<Psychology />}
                          label="AI Optimized"
                          sx={{ 
                            background: 'rgba(0, 245, 255, 0.2)',
                            color: '#00f5ff',
                            border: '1px solid #00f5ff'
                          }}
                        />
                        <Chip 
                          icon={<Bolt />}
                          label="Quantum Enhanced"
                          sx={{ 
                            background: 'rgba(29, 233, 182, 0.2)',
                            color: '#1de9b6',
                            border: '1px solid #1de9b6'
                          }}
                        />
                      </Box>
                    </Box>
                  )}
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ 
                    display: 'flex', 
                    flexDirection: 'column',
                    gap: 3,
                    position: 'relative',
                    zIndex: 2
                  }}>
                    <Button 
                      variant="contained" 
                      size="large"
                      startIcon={<Rocket />}
                      onClick={handleOpenDepositModal}
                      sx={{ 
                        px: 4,
                        py: 3,
                        fontWeight: 900,
                        fontSize: '1.1rem',
                        borderRadius: 4,
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        color: 'black',
                        boxShadow: '0 10px 30px rgba(0, 245, 255, 0.4)',
                        '&:hover': {
                          transform: 'translateY(-3px) scale(1.05)',
                          boxShadow: '0 15px 40px rgba(0, 245, 255, 0.6)',
                          background: 'linear-gradient(45deg, #1de9b6, #00f5ff)',
                        },
                        transition: 'all 0.3s ease'
                      }}
                    >
                      Quantum Invest
                    </Button>
                    <Button 
                      variant="outlined" 
                      size="large"
                      startIcon={<AttachMoney />}
                      onClick={handleOpenWithdrawModal}
                      sx={{ 
                        px: 4,
                        py: 3,
                        fontWeight: 900,
                        fontSize: '1.1rem',
                        borderRadius: 4,
                        borderWidth: 2,
                        borderColor: '#ff6d00',
                        color: '#ff6d00',
                        '&:hover': {
                          borderWidth: 2,
                          borderColor: '#ff6d00',
                          background: 'rgba(255, 109, 0, 0.1)',
                          transform: 'translateY(-3px) scale(1.05)',
                          boxShadow: '0 10px 30px rgba(255, 109, 0, 0.3)'
                        },
                        transition: 'all 0.3s ease'
                      }}
                    >
                      Neural Withdraw
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Fade>

          {/* Advanced Charts Section */}
          <Grid container spacing={4} sx={{ mb: 4 }}>
            {/* Quantum Performance Chart */}
            <Grid item xs={12} lg={8}>
              <Fade in={true} timeout={1400}>
                <Paper 
                  elevation={0}
                  sx={{ 
                    p: 4, 
                    borderRadius: 6,
                    background: `
                      linear-gradient(135deg, 
                        rgba(0, 245, 255, 0.08) 0%, 
                        rgba(29, 233, 182, 0.08) 50%,
                        rgba(255, 109, 0, 0.08) 100%
                      )
                    `,
                    backdropFilter: 'blur(30px)',
                    border: '1px solid rgba(0, 245, 255, 0.2)',
                    height: 500,
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Box>
                      <Typography variant="h4" fontWeight={900} sx={{
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent'
                      }}>
                        Quantum Performance Matrix
                      </Typography>
                      <Typography variant="body1" color="rgba(255, 255, 255, 0.7)">
                        AI-Powered Predictive Analytics
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      {['1D', '1W', '1M', '1Y'].map((period, index) => (
                        <Chip 
                          key={period}
                          label={period} 
                          size="small" 
                          variant={index === 2 ? "filled" : "outlined"}
                          color={index === 2 ? "primary" : "default"}
                          sx={{ 
                            fontWeight: 700,
                            ...(index === 2 && {
                              background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                              color: 'black'
                            })
                          }}
                        />
                      ))}
                    </Box>
                  </Box>
                  {portfolioLoading ? (
                    <Skeleton variant="rectangular" width="100%" height={350} sx={{ borderRadius: 3 }} />
                  ) : portfolioError ? (
                    <Alert severity="error">Quantum matrix offline - Reconnecting...</Alert>
                  ) : (
                    <ResponsiveContainer width="100%" height={350}>
                      <ComposedChart data={advancedChartData}>
                        <defs>
                          <linearGradient id="portfolioGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#00f5ff" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#00f5ff" stopOpacity={0.1}/>
                          </linearGradient>
                          <linearGradient id="aiGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#1de9b6" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#1de9b6" stopOpacity={0.1}/>
                          </linearGradient>
                        </defs>
                        <XAxis dataKey="time" stroke="#666" />
                        <YAxis stroke="#666" />
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <RechartsTooltip 
                          contentStyle={{ 
                            backgroundColor: 'rgba(0,0,0,0.9)', 
                            border: '1px solid #00f5ff',
                            borderRadius: '12px',
                            backdropFilter: 'blur(20px)'
                          }} 
                        />
                        <Legend />
                        <Area 
                          type="monotone" 
                          dataKey="portfolio" 
                          stroke="#00f5ff" 
                          strokeWidth={3}
                          fillOpacity={1} 
                          fill="url(#portfolioGradient)"
                          name="Portfolio Value"
                        />
                        <Line 
                          type="monotone" 
                          dataKey="ai_prediction" 
                          stroke="#1de9b6" 
                          strokeWidth={2}
                          strokeDasharray="5 5"
                          name="AI Prediction"
                        />
                        <Line 
                          type="monotone" 
                          dataKey="benchmark" 
                          stroke="#ff6d00" 
                          strokeWidth={2}
                          name="Market Benchmark"
                        />
                      </ComposedChart>
                    </ResponsiveContainer>
                  )}
                </Paper>
              </Fade>
            </Grid>

            {/* Neural Market Allocation */}
            <Grid item xs={12} lg={4}>
              <Fade in={true} timeout={1600}>
                <Paper 
                  elevation={0}
                  sx={{ 
                    p: 4, 
                    borderRadius: 6,
                    background: `
                      linear-gradient(135deg, 
                        rgba(255, 109, 0, 0.08) 0%, 
                        rgba(233, 30, 99, 0.08) 50%,
                        rgba(156, 39, 176, 0.08) 100%
                      )
                    `,
                    backdropFilter: 'blur(30px)',
                    border: '1px solid rgba(255, 109, 0, 0.2)',
                    height: 500
                  }}
                >
                  <Typography variant="h5" fontWeight={900} gutterBottom sx={{
                    background: 'linear-gradient(45deg, #ff6d00, #e91e63)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                  }}>
                    Neural Allocation Matrix
                  </Typography>
                  <ResponsiveContainer width="100%" height={280}>
                    <PieChart>
                      <Pie
                        data={marketOverviewData}
                        cx="50%"
                        cy="50%"
                        innerRadius={70}
                        outerRadius={120}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {marketOverviewData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={entry.color}
                            stroke={entry.color}
                            strokeWidth={2}
                          />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <Box sx={{ mt: 3 }}>
                    {marketOverviewData.map((item, index) => (
                      <Box key={index} sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        mb: 2,
                        p: 2,
                        borderRadius: 2,
                        background: `rgba(${item.color === '#00f5ff' ? '0, 245, 255' : 
                                           item.color === '#1de9b6' ? '29, 233, 182' :
                                           item.color === '#ff6d00' ? '255, 109, 0' :
                                           item.color === '#e91e63' ? '233, 30, 99' :
                                           '156, 39, 176'}, 0.1)`,
                        border: `1px solid ${item.color}`,
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateX(10px)',
                          background: `rgba(${item.color === '#00f5ff' ? '0, 245, 255' : 
                                             item.color === '#1de9b6' ? '29, 233, 182' :
                                             item.color === '#ff6d00' ? '255, 109, 0' :
                                             item.color === '#e91e63' ? '233, 30, 99' :
                                             '156, 39, 176'}, 0.2)`
                        }
                      }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Box sx={{ 
                            width: 16, 
                            height: 16, 
                            bgcolor: item.color, 
                            borderRadius: 1,
                            boxShadow: `0 0 10px ${item.color}`
                          }} />
                          <Typography variant="body1" fontWeight={600}>{item.name}</Typography>
                        </Box>
                        <Box sx={{ textAlign: 'right' }}>
                          <Typography variant="h6" fontWeight={700}>{item.value}%</Typography>
                          <Typography variant="caption" sx={{ color: '#1de9b6' }}>
                            {item.growth}
                          </Typography>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                </Paper>
              </Fade>
            </Grid>
          </Grid>

          {/* AI Strategy Performance and Neural Trading */}
          <Grid container spacing={4}>
            <Grid item xs={12} lg={7}>
              <Fade in={true} timeout={1800}>
                <Paper 
                  elevation={0}
                  sx={{ 
                    p: 4, 
                    borderRadius: 6,
                    background: `
                      linear-gradient(135deg, 
                        rgba(0, 245, 255, 0.08) 0%, 
                        rgba(29, 233, 182, 0.08) 50%,
                        rgba(156, 39, 176, 0.08) 100%
                      )
                    `,
                    backdropFilter: 'blur(30px)',
                    border: '1px solid rgba(0, 245, 255, 0.2)',
                    minHeight: 500
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                    <Box>
                      <Typography variant="h4" fontWeight={900} sx={{
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent'
                      }}>
                        Neural Strategy Matrix
                      </Typography>
                      <Typography variant="body1" color="rgba(255, 255, 255, 0.7)">
                        Quantum-Enhanced AI Performance
                      </Typography>
                    </Box>
                    <Chip 
                      icon={<Psychology />} 
                      label="NEURAL ACTIVE" 
                      sx={{ 
                        background: 'linear-gradient(45deg, #00f5ff, #1de9b6)',
                        color: 'black',
                        fontWeight: 700,
                        px: 2,
                        py: 1,
                        animation: 'pulse 2s infinite'
                      }}
                    />
                  </Box>
                  {strategiesLoading ? (
                    <Stack spacing={2}>
                      {[1, 2, 3].map((i) => (
                        <Skeleton key={i} variant="rectangular" width="100%" height={80} sx={{ borderRadius: 3 }} />
                      ))}
                    </Stack>
                  ) : strategiesError ? (
                    <Alert severity="error">Neural network offline - Reconnecting...</Alert>
                  ) : (
                    <StrategyTable strategies={strategiesArray} />
                  )}
                </Paper>
              </Fade>
            </Grid>
            
            <Grid item xs={12} lg={5}>
              <Fade in={true} timeout={2000}>
                <Paper 
                  elevation={0}
                  sx={{ 
                    p: 4, 
                    borderRadius: 6,
                    background: `
                      linear-gradient(135deg, 
                        rgba(255, 109, 0, 0.08) 0%, 
                        rgba(233, 30, 99, 0.08) 50%,
                        rgba(156, 39, 176, 0.08) 100%
                      )
                    `,
                    backdropFilter: 'blur(30px)',
                    border: '1px solid rgba(255, 109, 0, 0.2)',
                    minHeight: 500
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                    <Box>
                      <Typography variant="h4" fontWeight={900} sx={{
                        background: 'linear-gradient(45deg, #ff6d00, #e91e63)',
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent'
                      }}>
                        Quantum Trading Feed
                      </Typography>
                      <Typography variant="body1" color="rgba(255, 255, 255, 0.7)">
                        Real-time Neural Execution
                      </Typography>
                    </Box>
                    <Chip 
                      icon={<FlashOn />} 
                      label="LIVE FEED" 
                      sx={{ 
                        background: 'linear-gradient(45deg, #ff6d00, #e91e63)',
                        color: 'white',
                        fontWeight: 700,
                        animation: 'glow 2s ease-in-out infinite alternate'
                      }}
                    />
                  </Box>
                  {tradesLoading ? (
                    <Stack spacing={2}>
                      {[1, 2, 3].map((i) => (
                        <Skeleton key={i} variant="rectangular" width="100%" height={100} sx={{ borderRadius: 3 }} />
                      ))}
                    </Stack>
                  ) : tradesError ? (
                    <Alert severity="error">Trading feed offline - Reconnecting...</Alert>
                  ) : (
                    <RecentTradesList trades={tradesData || recentTrades} />
                  )}
                </Paper>
              </Fade>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Advanced CSS Animations */}
      <style jsx>{`
        @keyframes glow {
          0%, 100% { text-shadow: 0 0 20px rgba(0, 245, 255, 0.5); }
          50% { text-shadow: 0 0 30px rgba(0, 245, 255, 0.8), 0 0 40px rgba(29, 233, 182, 0.5); }
        }
        
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.05); opacity: 0.8; }
        }
        
        @keyframes twinkle {
          0%, 100% { opacity: 0.1; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.2); }
        }
        
        @keyframes gridPulse {
          0%, 100% { opacity: 0.03; }
          50% { opacity: 0.08; }
        }
        
        @keyframes quantumPulse {
          0%, 100% { opacity: 0.1; transform: scale(1); }
          50% { opacity: 0.3; transform: scale(1.02); }
        }
        
        @keyframes rotate {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-5px); }
          60% { transform: translateY(-3px); }
        }
      `}</style>
    </ErrorBoundary>
  );
};

export default Dashboard;

