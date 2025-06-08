import React from 'react';
import { Box, Typography, List, ListItem, ListItemText, Chip, Avatar, Divider, Paper } from '@mui/material';
import { TrendingUp, TrendingDown, SwapHoriz } from '@mui/icons-material';

const RecentTradesList = ({ trades }) => {
  if (!trades || !Array.isArray(trades)) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="body1" color="text.secondary">
          No recent trades available
        </Typography>
      </Box>
    );
  }

  const getTradeIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'buy': return <TrendingUp />;
      case 'sell': return <TrendingDown />;
      default: return <SwapHoriz />;
    }
  };

  const getTradeColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'buy': return 'success';
      case 'sell': return 'error';
      default: return 'primary';
    }
  };

  return (
    <Box>
      <List sx={{ p: 0 }}>
        {trades.map((trade, index) => (
          <React.Fragment key={trade.id || index}>
            <ListItem 
              sx={{ 
                px: 0,
                py: 2,
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.05)',
                  borderRadius: 2
                }
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', gap: 2 }}>
                <Avatar sx={{ 
                  bgcolor: `${getTradeColor(trade.type)}.main`,
                  width: 48,
                  height: 48,
                  background: trade.type?.toLowerCase() === 'buy' 
                    ? 'linear-gradient(45deg, #4caf50, #81c784)'
                    : 'linear-gradient(45deg, #f44336, #ef5350)'
                }}>
                  {getTradeIcon(trade.type)}
                </Avatar>
                
                <Box sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="h6" fontWeight={700}>
                      {trade.symbol}
                    </Typography>
                    <Chip 
                      label={trade.type?.toUpperCase() || 'TRADE'}
                      color={getTradeColor(trade.type)}
                      size="small"
                      variant="filled"
                      sx={{ fontWeight: 600 }}
                    />
                  </Box>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Qty: {trade.quantity} @ ${trade.price}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {trade.timestamp}
                      </Typography>
                    </Box>
                    <Typography variant="h6" fontWeight={700} color="primary.main">
                      ${(trade.quantity * trade.price).toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </ListItem>
            {index < trades.length - 1 && (
              <Divider sx={{ backgroundColor: 'rgba(255,255,255,0.1)' }} />
            )}
          </React.Fragment>
        ))}
      </List>
      
      <Paper sx={{ 
        mt: 2, 
        p: 2, 
        background: 'linear-gradient(45deg, rgba(25,118,210,0.1), rgba(66,165,245,0.1))',
        border: '1px solid rgba(25,118,210,0.2)',
        borderRadius: 2
      }}>
        <Typography variant="body2" color="primary.main" fontWeight={600} textAlign="center">
          View All Trading Activity →
        </Typography>
      </Paper>
    </Box>
  );
};

export default RecentTradesList;

