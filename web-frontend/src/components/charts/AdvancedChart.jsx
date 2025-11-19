import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  ButtonGroup,
  IconButton,
  Menu,
  MenuItem,
  Chip,
  Grid,
  Card,
  CardContent,
  Fade,
  Tooltip,
  Select,
  FormControl,
  InputLabel
} from '@mui/material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  CandlestickChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Brush
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  BarChart3,
  Activity,
  Settings,
  Download,
  Maximize2,
  MoreVertical,
  Zap,
  Target,
  Eye,
  EyeOff
} from 'lucide-react';

const AdvancedChart = ({ symbol = 'AAPL', title = 'Advanced Trading Chart' }) => {
  const [chartType, setChartType] = useState('candlestick');
  const [timeframe, setTimeframe] = useState('1D');
  const [indicators, setIndicators] = useState({
    sma: true,
    ema: false,
    bollinger: false,
    rsi: false,
    macd: false,
    volume: true
  });
  const [anchorEl, setAnchorEl] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Mock data for demonstration
  const [chartData, setChartData] = useState([
    { time: '09:30', open: 175.20, high: 176.50, low: 174.80, close: 176.20, volume: 1200000, sma: 175.50, ema: 175.80 },
    { time: '10:00', open: 176.20, high: 177.10, low: 175.90, close: 176.80, volume: 980000, sma: 175.70, ema: 176.00 },
    { time: '10:30', open: 176.80, high: 178.20, low: 176.50, close: 177.90, volume: 1100000, sma: 176.00, ema: 176.30 },
    { time: '11:00', open: 177.90, high: 178.50, low: 177.20, close: 178.10, volume: 850000, sma: 176.30, ema: 176.70 },
    { time: '11:30', open: 178.10, high: 179.00, low: 177.80, close: 178.70, volume: 920000, sma: 176.60, ema: 177.10 },
    { time: '12:00', open: 178.70, high: 179.20, low: 178.30, close: 178.90, volume: 760000, sma: 176.90, ema: 177.50 },
    { time: '12:30', open: 178.90, high: 179.80, low: 178.60, close: 179.40, volume: 890000, sma: 177.20, ema: 177.90 },
    { time: '13:00', open: 179.40, high: 180.10, low: 179.00, close: 179.80, volume: 1050000, sma: 177.50, ema: 178.30 },
    { time: '13:30', open: 179.80, high: 180.50, low: 179.30, close: 180.20, volume: 970000, sma: 177.80, ema: 178.70 },
    { time: '14:00', open: 180.20, high: 181.00, low: 179.90, close: 180.60, volume: 1150000, sma: 178.10, ema: 179.10 },
    { time: '14:30', open: 180.60, high: 181.20, low: 180.10, close: 180.90, volume: 820000, sma: 178.40, ema: 179.50 },
    { time: '15:00', open: 180.90, high: 181.50, low: 180.40, close: 181.20, volume: 940000, sma: 178.70, ema: 179.90 },
    { time: '15:30', open: 181.20, high: 182.00, low: 180.80, close: 181.70, volume: 1080000, sma: 179.00, ema: 180.30 },
    { time: '16:00', open: 181.70, high: 182.30, low: 181.40, close: 182.10, volume: 1200000, sma: 179.30, ema: 180.70 }
  ]);

  const toggleIndicator = (indicator) => {
    setIndicators(prev => ({
      ...prev,
      [indicator]: !prev[indicator]
    }));
  };

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const exportChart = () => {
    // Mock export functionality
    console.log('Exporting chart...');
    handleMenuClose();
  };

  const CustomCandlestick = (props) => {
    const { payload, x, y, width, height } = props;
    if (!payload) return null;

    const { open, close, high, low } = payload;
    const isGreen = close > open;
    const color = isGreen ? '#10b981' : '#ef4444';
    const bodyHeight = Math.abs(close - open);
    const bodyY = Math.min(open, close);

    return (
      <g>
        {/* Wick */}
        <line
          x1={x + width / 2}
          y1={y + (high - Math.max(open, close)) * height / (high - low)}
          x2={x + width / 2}
          y2={y + (high - Math.min(open, close)) * height / (high - low)}
          stroke={color}
          strokeWidth={1}
        />
        {/* Body */}
        <rect
          x={x + width * 0.2}
          y={y + (high - Math.max(open, close)) * height / (high - low)}
          width={width * 0.6}
          height={bodyHeight * height / (high - low)}
          fill={color}
          stroke={color}
        />
      </g>
    );
  };

  const renderChart = () => {
    switch (chartType) {
      case 'line':
        return (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="time" stroke="rgba(255,255,255,0.7)" fontSize={12} />
            <YAxis stroke="rgba(255,255,255,0.7)" fontSize={12} domain={['dataMin - 1', 'dataMax + 1']} />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="close"
              stroke="#00d4ff"
              strokeWidth={2}
              dot={false}
              name="Price"
            />
            {indicators.sma && (
              <Line
                type="monotone"
                dataKey="sma"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="SMA"
              />
            )}
            {indicators.ema && (
              <Line
                type="monotone"
                dataKey="ema"
                stroke="#8b5cf6"
                strokeWidth={1}
                strokeDasharray="3 3"
                dot={false}
                name="EMA"
              />
            )}
          </LineChart>
        );

      case 'area':
        return (
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#00d4ff" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="time" stroke="rgba(255,255,255,0.7)" fontSize={12} />
            <YAxis stroke="rgba(255,255,255,0.7)" fontSize={12} domain={['dataMin - 1', 'dataMax + 1']} />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
            />
            <Area
              type="monotone"
              dataKey="close"
              stroke="#00d4ff"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorPrice)"
            />
          </AreaChart>
        );

      case 'bar':
        return (
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="time" stroke="rgba(255,255,255,0.7)" fontSize={12} />
            <YAxis stroke="rgba(255,255,255,0.7)" fontSize={12} />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
            />
            <Bar dataKey="volume" fill="#00d4ff" />
          </BarChart>
        );

      default: // candlestick
        return (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="time" stroke="rgba(255,255,255,0.7)" fontSize={12} />
            <YAxis stroke="rgba(255,255,255,0.7)" fontSize={12} domain={['dataMin - 1', 'dataMax + 1']} />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
              formatter={(value, name) => {
                if (name === 'high') return [`H: $${value}`, 'High'];
                if (name === 'low') return [`L: $${value}`, 'Low'];
                if (name === 'open') return [`O: $${value}`, 'Open'];
                if (name === 'close') return [`C: $${value}`, 'Close'];
                return [value, name];
              }}
            />
            <Line type="monotone" dataKey="high" stroke="transparent" />
            <Line type="monotone" dataKey="low" stroke="transparent" />
            <Line type="monotone" dataKey="open" stroke="transparent" />
            <Line type="monotone" dataKey="close" stroke="#00d4ff" strokeWidth={2} dot={false} />
            {indicators.sma && (
              <Line
                type="monotone"
                dataKey="sma"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="SMA"
              />
            )}
          </LineChart>
        );
    }
  };

  return (
    <Fade in={true} timeout={1000}>
      <Paper
        elevation={0}
        sx={{
          p: 3,
          borderRadius: 4,
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
          height: isFullscreen ? '90vh' : 'auto'
        }}
      >
        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="h6" fontWeight={700} color="white">
              {title} - {symbol}
            </Typography>
            <Chip
              label="Real-time"
              icon={<Zap size={16} />}
              sx={{
                background: 'linear-gradient(45deg, #10b981, #059669)',
                color: 'white',
                fontWeight: 600
              }}
            />
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ButtonGroup size="small" sx={{ mr: 2 }}>
              {['1D', '1W', '1M', '3M', '1Y'].map((tf) => (
                <Button
                  key={tf}
                  variant={timeframe === tf ? 'contained' : 'outlined'}
                  onClick={() => setTimeframe(tf)}
                  sx={{
                    borderColor: '#00d4ff',
                    color: timeframe === tf ? 'white' : '#00d4ff',
                    background: timeframe === tf ? 'linear-gradient(45deg, #00d4ff, #0099cc)' : 'transparent',
                    '&:hover': {
                      borderColor: '#00d4ff',
                      background: timeframe === tf ? 'linear-gradient(45deg, #0099cc, #0066aa)' : 'rgba(0, 212, 255, 0.1)',
                    }
                  }}
                >
                  {tf}
                </Button>
              ))}
            </ButtonGroup>
            <IconButton
              onClick={() => setIsFullscreen(!isFullscreen)}
              sx={{ color: '#00d4ff' }}
            >
              <Maximize2 size={20} />
            </IconButton>
            <IconButton
              onClick={handleMenuClick}
              sx={{ color: '#00d4ff' }}
            >
              <MoreVertical size={20} />
            </IconButton>
          </Box>
        </Box>

        {/* Chart Type Selector */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
          <ButtonGroup size="small">
            {[
              { type: 'candlestick', label: 'Candlestick', icon: BarChart3 },
              { type: 'line', label: 'Line', icon: TrendingUp },
              { type: 'area', label: 'Area', icon: Activity },
              { type: 'bar', label: 'Volume', icon: BarChart3 }
            ].map(({ type, label, icon: Icon }) => (
              <Button
                key={type}
                variant={chartType === type ? 'contained' : 'outlined'}
                startIcon={<Icon size={16} />}
                onClick={() => setChartType(type)}
                sx={{
                  borderColor: '#00d4ff',
                  color: chartType === type ? 'white' : '#00d4ff',
                  background: chartType === type ? 'linear-gradient(45deg, #00d4ff, #0099cc)' : 'transparent',
                  '&:hover': {
                    borderColor: '#00d4ff',
                    background: chartType === type ? 'linear-gradient(45deg, #0099cc, #0066aa)' : 'rgba(0, 212, 255, 0.1)',
                  }
                }}
              >
                {label}
              </Button>
            ))}
          </ButtonGroup>
        </Box>

        {/* Indicators */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3, flexWrap: 'wrap' }}>
          <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
            Indicators:
          </Typography>
          {Object.entries(indicators).map(([key, enabled]) => (
            <Chip
              key={key}
              label={key.toUpperCase()}
              onClick={() => toggleIndicator(key)}
              icon={enabled ? <Eye size={14} /> : <EyeOff size={14} />}
              sx={{
                background: enabled ? 'linear-gradient(45deg, #00d4ff, #0099cc)' : 'rgba(255, 255, 255, 0.1)',
                color: 'white',
                fontWeight: 500,
                '&:hover': {
                  background: enabled ? 'linear-gradient(45deg, #0099cc, #0066aa)' : 'rgba(255, 255, 255, 0.2)',
                }
              }}
            />
          ))}
        </Box>

        {/* Chart */}
        <Box sx={{ height: isFullscreen ? 600 : 400, width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </Box>

        {/* Volume Chart (if enabled) */}
        {indicators.volume && chartType !== 'bar' && (
          <Box sx={{ height: 100, width: '100%', mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Volume
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <XAxis dataKey="time" hide />
                <YAxis hide />
                <Bar dataKey="volume" fill="#00d4ff" opacity={0.6} />
              </BarChart>
            </ResponsiveContainer>
          </Box>
        )}

        {/* Stats */}
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={6} sm={3}>
            <Card sx={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
              <CardContent sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">Open</Typography>
                <Typography variant="h6" color="#10b981" fontWeight={700}>
                  ${chartData[0]?.open.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Card sx={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
              <CardContent sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">High</Typography>
                <Typography variant="h6" color="#ef4444" fontWeight={700}>
                  ${Math.max(...chartData.map(d => d.high)).toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Card sx={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
              <CardContent sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">Low</Typography>
                <Typography variant="h6" color="#3b82f6" fontWeight={700}>
                  ${Math.min(...chartData.map(d => d.low)).toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Card sx={{ background: 'rgba(0, 212, 255, 0.1)', border: '1px solid rgba(0, 212, 255, 0.3)' }}>
              <CardContent sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">Close</Typography>
                <Typography variant="h6" color="#00d4ff" fontWeight={700}>
                  ${chartData[chartData.length - 1]?.close.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: {
              background: 'rgba(0, 0, 0, 0.9)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 2
            }
          }}
        >
          <MenuItem onClick={exportChart} sx={{ color: 'white' }}>
            <Download size={16} style={{ marginRight: 8 }} />
            Export Chart
          </MenuItem>
          <MenuItem onClick={handleMenuClose} sx={{ color: 'white' }}>
            <Settings size={16} style={{ marginRight: 8 }} />
            Chart Settings
          </MenuItem>
          <MenuItem onClick={handleMenuClose} sx={{ color: 'white' }}>
            <Target size={16} style={{ marginRight: 8 }} />
            Add Alert
          </MenuItem>
        </Menu>
      </Paper>
    </Fade>
  );
};

export default AdvancedChart;
