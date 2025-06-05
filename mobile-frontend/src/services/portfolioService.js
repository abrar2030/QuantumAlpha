import api from './api';

class PortfolioService {
  async getPortfolioSummary() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              totalValue: 10400,
              dailyChange: 100,
              percentChange: 0.97,
              assets: [
                { symbol: 'AAPL', value: 3200, change: 1.2 },
                { symbol: 'MSFT', value: 2800, change: 0.8 },
                { symbol: 'GOOGL', value: 2400, change: -0.5 },
                { symbol: 'AMZN', value: 2000, change: 1.5 },
              ],
              cash: 1000,
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio summary:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch portfolio data');
    }
  }

  async getPerformanceHistory(period = '1M') {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          let labels = [];
          let values = [];
          
          switch (period) {
            case '1D':
              labels = ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM'];
              values = [10200, 10250, 10300, 10280, 10320, 10350, 10380, 10400];
              break;
            case '1W':
              labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
              values = [10100, 10150, 10200, 10300, 10400];
              break;
            case '1M':
              labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
              values = [10000, 10100, 10250, 10400];
              break;
            case '3M':
              labels = ['Jan', 'Feb', 'Mar'];
              values = [9800, 10100, 10400];
              break;
            case '1Y':
              labels = ['Q1', 'Q2', 'Q3', 'Q4'];
              values = [9500, 9800, 10200, 10400];
              break;
            case 'ALL':
              labels = ['2020', '2021', '2022', '2023', '2024'];
              values = [8000, 8500, 9200, 9800, 10400];
              break;
            default:
              labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
              values = [10000, 10100, 10250, 10400];
          }
          
          resolve({
            data: {
              labels,
              values,
              period,
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching performance history:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch performance data');
    }
  }

  async getAssetAllocation() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: [
              { name: 'Stocks', percentage: 60, value: 6240 },
              { name: 'Crypto', percentage: 20, value: 2080 },
              { name: 'Bonds', percentage: 10, value: 1040 },
              { name: 'Cash', percentage: 10, value: 1040 },
            ],
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching asset allocation:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch asset allocation data');
    }
  }

  async getHoldings() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: [
              { 
                symbol: 'AAPL', 
                name: 'Apple Inc.', 
                quantity: 10, 
                price: 320, 
                value: 3200, 
                change: 1.2,
                allocation: 30.77
              },
              { 
                symbol: 'MSFT', 
                name: 'Microsoft Corp.', 
                quantity: 8, 
                price: 350, 
                value: 2800, 
                change: 0.8,
                allocation: 26.92
              },
              { 
                symbol: 'GOOGL', 
                name: 'Alphabet Inc.', 
                quantity: 2, 
                price: 1200, 
                value: 2400, 
                change: -0.5,
                allocation: 23.08
              },
              { 
                symbol: 'AMZN', 
                name: 'Amazon.com Inc.', 
                quantity: 1, 
                price: 2000, 
                value: 2000, 
                change: 1.5,
                allocation: 19.23
              },
            ],
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching holdings:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch holdings data');
    }
  }

  async getTransactionHistory(page = 1, limit = 20) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              transactions: [
                { 
                  id: 'tx1', 
                  type: 'BUY', 
                  symbol: 'AAPL', 
                  quantity: 2, 
                  price: 315, 
                  total: 630, 
                  date: '2025-06-01T10:30:00Z',
                  status: 'COMPLETED'
                },
                { 
                  id: 'tx2', 
                  type: 'SELL', 
                  symbol: 'MSFT', 
                  quantity: 1, 
                  price: 340, 
                  total: 340, 
                  date: '2025-05-28T14:15:00Z',
                  status: 'COMPLETED'
                },
                { 
                  id: 'tx3', 
                  type: 'BUY', 
                  symbol: 'GOOGL', 
                  quantity: 1, 
                  price: 1180, 
                  total: 1180, 
                  date: '2025-05-25T09:45:00Z',
                  status: 'COMPLETED'
                },
                { 
                  id: 'tx4', 
                  type: 'DEPOSIT', 
                  symbol: 'USD', 
                  quantity: 2000, 
                  price: 1, 
                  total: 2000, 
                  date: '2025-05-20T11:00:00Z',
                  status: 'COMPLETED'
                },
                { 
                  id: 'tx5', 
                  type: 'BUY', 
                  symbol: 'AMZN', 
                  quantity: 1, 
                  price: 1950, 
                  total: 1950, 
                  date: '2025-05-15T13:20:00Z',
                  status: 'COMPLETED'
                },
              ],
              pagination: {
                page,
                limit,
                total: 5,
                pages: 1
              }
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching transaction history:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch transaction history');
    }
  }
}

export const portfolioService = new PortfolioService();
