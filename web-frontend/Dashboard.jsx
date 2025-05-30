import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Button, 
  AppBar, 
  Toolbar, 
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Card,
  CardContent,
  CardHeader
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
  ExitToApp as ExitToAppIcon
} from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Create a dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1aff92',
    },
    secondary: {
      main: '#7986cb',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

// Sample data for charts
const performanceData = [
  { name: 'Jan', value: 10000 },
  { name: 'Feb', value: 10200 },
  { name: 'Mar', value: 10150 },
  { name: 'Apr', value: 10400 },
  { name: 'May', value: 10800 },
  { name: 'Jun', value: 11200 },
  { name: 'Jul', value: 11500 },
];

const strategyPerformance = [
  { name: 'Momentum Alpha', return: 8.2, sharpe: 1.8, drawdown: -3.5 },
  { name: 'Sentiment Trader', return: 5.7, sharpe: 1.5, drawdown: -2.8 },
  { name: 'ML Predictor', return: 12.3, sharpe: 2.1, drawdown: -5.2 },
  { name: 'Mean Reversion', return: 6.9, sharpe: 1.6, drawdown: -4.1 },
];

const recentTrades = [
  { id: 1, symbol: 'AAPL', type: 'BUY', quantity: 100, price: 182.63, timestamp: '2023-06-15 10:32:45' },
  { id: 2, symbol: 'MSFT', type: 'SELL', quantity: 50, price: 337.42, timestamp: '2023-06-15 11:15:22' },
  { id: 3, symbol: 'GOOGL', type: 'BUY', quantity: 25, price: 125.23, timestamp: '2023-06-15 13:45:10' },
];

function Dashboard() {
  const [open, setOpen] = useState(false);
  const [portfolioValue, setPortfolioValue] = useState(11500);
  const [dailyChange, setDailyChange] = useState(300);
  const [percentChange, setPercentChange] = useState(2.68);

  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        {/* App Bar */}
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={toggleDrawer}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
              QuantumAlpha Dashboard
            </Typography>
            <IconButton color="inherit">
              <NotificationsIcon />
            </IconButton>
            <IconButton color="inherit">
              <AccountCircleIcon />
            </IconButton>
          </Toolbar>
        </AppBar>

        {/* Side Drawer */}
        <Drawer
          variant="persistent"
          anchor="left"
          open={open}
          sx={{
            width: 240,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: 240,
              boxSizing: 'border-box',
              backgroundColor: 'background.paper',
            },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto', mt: 2 }}>
            <List>
              <ListItem button selected>
                <ListItemIcon>
                  <DashboardIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItem>
              <ListItem button>
                <ListItemIcon>
                  <TrendingUpIcon />
                </ListItemIcon>
                <ListItemText primary="Strategies" />
              </ListItem>
              <ListItem button>
                <ListItemIcon>
                  <AssessmentIcon />
                </ListItemIcon>
                <ListItemText primary="Analytics" />
              </ListItem>
            </List>
            <Divider />
            <List>
              <ListItem button>
                <ListItemIcon>
                  <SettingsIcon />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItem>
              <ListItem button>
                <ListItemIcon>
                  <ExitToAppIcon />
                </ListItemIcon>
                <ListItemText primary="Logout" />
              </ListItem>
            </List>
          </Box>
        </Drawer>

        {/* Main Content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            backgroundColor: 'background.default',
            marginLeft: open ? '240px' : 0,
            transition: (theme) => theme.transitions.create('margin', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.leavingScreen,
            }),
          }}
        >
          <Toolbar />
          
          {/* Portfolio Summary */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h4" gutterBottom>
                  Portfolio Value
                </Typography>
                <Typography variant="h3" color="primary">
                  ${portfolioValue.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <Typography 
                    variant="h6" 
                    color={dailyChange >= 0 ? 'primary' : 'error'}
                  >
                    {dailyChange >= 0 ? '+' : ''}{dailyChange.toLocaleString()} ({percentChange}%)
                  </Typography>
                  <Typography variant="body2" sx={{ ml: 1 }}>
                    Today
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                  <Button variant="contained" color="primary">
                    Deposit Funds
                  </Button>
                  <Button variant="outlined" color="primary">
                    Withdraw
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Paper>

          {/* Performance Chart */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Portfolio Performance
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={performanceData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#1aff92"
                  activeDot={{ r: 8 }}
                  name="Portfolio Value"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>

          {/* Strategy Performance and Recent Trades */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={7}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Typography variant="h5" gutterBottom>
                  Strategy Performance
                </Typography>
                <Box sx={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr>
                        <th style={{ textAlign: 'left', padding: '8px' }}>Strategy</th>
                        <th style={{ textAlign: 'right', padding: '8px' }}>Return (%)</th>
                        <th style={{ textAlign: 'right', padding: '8px' }}>Sharpe</th>
                        <th style={{ textAlign: 'right', padding: '8px' }}>Max DD (%)</th>
                        <th style={{ textAlign: 'center', padding: '8px' }}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {strategyPerformance.map((strategy, index) => (
                        <tr key={index} style={{ borderTop: '1px solid rgba(255, 255, 255, 0.12)' }}>
                          <td style={{ padding: '12px 8px' }}>{strategy.name}</td>
                          <td style={{ textAlign: 'right', padding: '12px 8px', color: strategy.return > 0 ? '#1aff92' : '#ff4d4d' }}>
                            {strategy.return > 0 ? '+' : ''}{strategy.return}%
                          </td>
                          <td style={{ textAlign: 'right', padding: '12px 8px' }}>{strategy.sharpe}</td>
                          <td style={{ textAlign: 'right', padding: '12px 8px', color: '#ff4d4d' }}>
                            {strategy.drawdown}%
                          </td>
                          <td style={{ textAlign: 'center', padding: '12px 8px' }}>
                            <Button size="small" variant="outlined" color="primary">
                              Details
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={5}>
              <Paper sx={{ p: 3, height: '100%' }}>
                <Typography variant="h5" gutterBottom>
                  Recent Trades
                </Typography>
                <Box sx={{ overflowY: 'auto', maxHeight: 300 }}>
                  {recentTrades.map((trade) => (
                    <Card key={trade.id} sx={{ mb: 2, backgroundColor: 'background.paper' }}>
                      <CardContent sx={{ py: 1 }}>
                        <Grid container alignItems="center">
                          <Grid item xs={8}>
                            <Typography variant="h6">
                              {trade.symbol}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {trade.timestamp}
                            </Typography>
                          </Grid>
                          <Grid item xs={4} sx={{ textAlign: 'right' }}>
                            <Typography 
                              variant="body1" 
                              color={trade.type === 'BUY' ? 'primary' : 'error'}
                              fontWeight="bold"
                            >
                              {trade.type}
                            </Typography>
                            <Typography variant="body2">
                              {trade.quantity} @ ${trade.price}
                            </Typography>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default Dashboard;
