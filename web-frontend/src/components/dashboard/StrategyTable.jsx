import React from 'react';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, useTheme, Typography, Chip, Avatar, LinearProgress } from '@mui/material';
import { TrendingUp, TrendingDown, Pause, PlayArrow, AutoGraph } from '@mui/icons-material';

const StrategyTable = ({ strategies }) => {
  const theme = useTheme();

  // Handle case where strategies might not be an array or might be undefined
  if (!strategies || !Array.isArray(strategies)) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="body1" color="text.secondary">
          No strategy data available
        </Typography>
      </Box>
    );
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'success';
      case 'paused': return 'warning';
      case 'stopped': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return <PlayArrow fontSize="small" />;
      case 'paused': return <Pause fontSize="small" />;
      default: return <AutoGraph fontSize="small" />;
    }
  };

  return (
    <Box sx={{ overflowX: 'auto' }}>
      <TableContainer>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 700, color: 'primary.main' }}>Strategy</TableCell>
              <TableCell align="right" sx={{ fontWeight: 700, color: 'primary.main' }}>Return (%)</TableCell>
              <TableCell align="right" sx={{ fontWeight: 700, color: 'primary.main' }}>Sharpe</TableCell>
              <TableCell align="right" sx={{ fontWeight: 700, color: 'primary.main' }}>Max DD (%)</TableCell>
              <TableCell align="center" sx={{ fontWeight: 700, color: 'primary.main' }}>Status</TableCell>
              <TableCell align="center" sx={{ fontWeight: 700, color: 'primary.main' }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {strategies.map((strategy, index) => {
              const returnValue = strategy.return_ytd || strategy.return || 0;
              const sharpeValue = strategy.sharpe_ratio || strategy.sharpe || 'N/A';
              const drawdownValue = strategy.max_drawdown || strategy.drawdown || 'N/A';
              
              return (
                <TableRow 
                  key={strategy.id || index} 
                  sx={{ 
                    '&:hover': { 
                      backgroundColor: 'rgba(25, 118, 210, 0.08)',
                      transform: 'scale(1.01)',
                    },
                    transition: 'all 0.2s ease',
                    borderRadius: 2
                  }}
                >
                  <TableCell component="th" scope="row">
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Avatar sx={{ 
                        bgcolor: 'primary.main', 
                        width: 40, 
                        height: 40,
                        background: 'linear-gradient(45deg, #1976d2, #42a5f5)'
                      }}>
                        <AutoGraph />
                      </Avatar>
                      <Box>
                        <Typography variant="subtitle1" fontWeight={600}>
                          {strategy.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {strategy.description || 'AI-powered strategy'}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell align="right">
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 1 }}>
                      {returnValue > 0 ? <TrendingUp color="success" fontSize="small" /> : <TrendingDown color="error" fontSize="small" />}
                      <Typography 
                        variant="h6"
                        fontWeight={700}
                        sx={{ 
                          color: returnValue > 0 ? 'success.main' : 'error.main'
                        }}
                      >
                        {returnValue > 0 ? '+' : ''}{returnValue}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.abs(returnValue) * 2} 
                      sx={{ 
                        mt: 1, 
                        height: 4, 
                        borderRadius: 2,
                        backgroundColor: 'rgba(255,255,255,0.1)',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: returnValue > 0 ? theme.palette.success.main : theme.palette.error.main
                        }
                      }} 
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="h6" fontWeight={600}>
                      {sharpeValue}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography 
                      variant="h6" 
                      fontWeight={600}
                      sx={{ color: 'error.main' }}
                    >
                      {drawdownValue}%
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Chip 
                      icon={getStatusIcon(strategy.status)}
                      label={strategy.status?.toUpperCase() || 'ACTIVE'}
                      color={getStatusColor(strategy.status)}
                      variant="filled"
                      sx={{ 
                        fontWeight: 600,
                        minWidth: 80
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Button 
                      size="small" 
                      variant="contained" 
                      color="primary"
                      sx={{ 
                        minWidth: '100px',
                        fontWeight: 600,
                        borderRadius: 2,
                        background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
                        '&:hover': {
                          transform: 'translateY(-1px)',
                          boxShadow: '0 4px 12px rgba(25,118,210,0.4)'
                        }
                      }}
                    >
                      Optimize
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default StrategyTable;

