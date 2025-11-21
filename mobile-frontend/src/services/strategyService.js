import api from "./api";

class StrategyService {
  async getActiveStrategies() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: "strat1",
                name: "Momentum Alpha",
                description:
                  "Captures price momentum across multiple timeframes",
                performance: 2.3,
                risk: "Medium",
                status: "Active",
                allocation: 30,
                lastUpdated: "2025-06-04T15:30:00Z",
              },
              {
                id: "strat2",
                name: "Sentiment Trader",
                description:
                  "Analyzes market sentiment from news and social media",
                performance: 1.5,
                risk: "Medium-High",
                status: "Active",
                allocation: 25,
                lastUpdated: "2025-06-04T14:45:00Z",
              },
              {
                id: "strat3",
                name: "ML Predictor",
                description:
                  "Uses machine learning to predict short-term price movements",
                performance: -0.8,
                risk: "High",
                status: "Active",
                allocation: 20,
                lastUpdated: "2025-06-04T16:15:00Z",
              },
              {
                id: "strat4",
                name: "Value Investor",
                description:
                  "Identifies undervalued assets based on fundamentals",
                performance: 0.9,
                risk: "Low",
                status: "Active",
                allocation: 15,
                lastUpdated: "2025-06-04T13:20:00Z",
              },
              {
                id: "strat5",
                name: "Trend Follower",
                description:
                  "Follows established market trends with adaptive entry/exit",
                performance: 1.2,
                risk: "Medium",
                status: "Active",
                allocation: 10,
                lastUpdated: "2025-06-04T12:10:00Z",
              },
            ],
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching active strategies:", error);
      throw new Error(
        error.response?.data?.message || "Failed to fetch strategy data",
      );
    }
  }

  async getStrategyDetails(strategyId) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          const strategies = {
            strat1: {
              id: "strat1",
              name: "Momentum Alpha",
              description:
                "Captures price momentum across multiple timeframes with adaptive position sizing based on volatility. Uses a combination of technical indicators to identify strong trends.",
              performance: 2.3,
              risk: "Medium",
              status: "Active",
              allocation: 30,
              lastUpdated: "2025-06-04T15:30:00Z",
              inception: "2025-01-15T00:00:00Z",
              totalReturn: 12.5,
              sharpeRatio: 1.8,
              maxDrawdown: -5.2,
              winRate: 68,
              parameters: [
                { name: "Lookback Period", value: "20 days" },
                { name: "Momentum Threshold", value: "0.05" },
                { name: "Position Sizing", value: "Adaptive" },
                { name: "Stop Loss", value: "2%" },
              ],
              holdings: [
                { symbol: "AAPL", allocation: 25, performance: 3.2 },
                { symbol: "MSFT", allocation: 20, performance: 2.1 },
                { symbol: "NVDA", allocation: 30, performance: 4.5 },
                { symbol: "AMZN", allocation: 15, performance: 1.8 },
                { symbol: "GOOGL", allocation: 10, performance: -0.5 },
              ],
              performanceHistory: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                values: [1.2, 2.5, 3.8, 5.6, 8.9, 12.5],
              },
            },
            strat2: {
              id: "strat2",
              name: "Sentiment Trader",
              description:
                "Analyzes market sentiment from news and social media using natural language processing to identify trading opportunities before they become apparent in price action.",
              performance: 1.5,
              risk: "Medium-High",
              status: "Active",
              allocation: 25,
              lastUpdated: "2025-06-04T14:45:00Z",
              inception: "2025-02-01T00:00:00Z",
              totalReturn: 8.3,
              sharpeRatio: 1.4,
              maxDrawdown: -7.8,
              winRate: 62,
              parameters: [
                { name: "Sentiment Sources", value: "News, Twitter, Reddit" },
                { name: "Update Frequency", value: "15 minutes" },
                { name: "Sentiment Threshold", value: "0.65" },
                { name: "Position Duration", value: "1-3 days" },
              ],
              holdings: [
                { symbol: "TSLA", allocation: 30, performance: 2.8 },
                { symbol: "META", allocation: 25, performance: 1.9 },
                { symbol: "NFLX", allocation: 20, performance: -1.2 },
                { symbol: "PYPL", allocation: 15, performance: 0.8 },
                { symbol: "TWTR", allocation: 10, performance: 3.5 },
              ],
              performanceHistory: {
                labels: ["Feb", "Mar", "Apr", "May", "Jun"],
                values: [1.5, 3.2, 4.1, 6.7, 8.3],
              },
            },
            strat3: {
              id: "strat3",
              name: "ML Predictor",
              description:
                "Uses machine learning to predict short-term price movements based on historical patterns, market microstructure, and alternative data sources.",
              performance: -0.8,
              risk: "High",
              status: "Active",
              allocation: 20,
              lastUpdated: "2025-06-04T16:15:00Z",
              inception: "2025-03-01T00:00:00Z",
              totalReturn: -2.5,
              sharpeRatio: 0.7,
              maxDrawdown: -8.5,
              winRate: 54,
              parameters: [
                { name: "Model Type", value: "LSTM Neural Network" },
                { name: "Training Window", value: "90 days" },
                { name: "Prediction Horizon", value: "3 days" },
                { name: "Confidence Threshold", value: "0.75" },
              ],
              holdings: [
                { symbol: "COIN", allocation: 20, performance: -3.5 },
                { symbol: "SQ", allocation: 20, performance: -1.8 },
                { symbol: "PLTR", allocation: 25, performance: 1.2 },
                { symbol: "SNOW", allocation: 20, performance: -2.4 },
                { symbol: "DDOG", allocation: 15, performance: 0.5 },
              ],
              performanceHistory: {
                labels: ["Mar", "Apr", "May", "Jun"],
                values: [2.1, 4.5, -1.2, -2.5],
              },
            },
            strat4: {
              id: "strat4",
              name: "Value Investor",
              description:
                "Identifies undervalued assets based on fundamentals using a combination of financial metrics and qualitative analysis.",
              performance: 0.9,
              risk: "Low",
              status: "Active",
              allocation: 15,
              lastUpdated: "2025-06-04T13:20:00Z",
              inception: "2025-01-01T00:00:00Z",
              totalReturn: 5.8,
              sharpeRatio: 1.2,
              maxDrawdown: -3.1,
              winRate: 65,
              parameters: [
                { name: "P/E Threshold", value: "<20" },
                { name: "Debt/Equity Ratio", value: "<0.5" },
                { name: "Minimum Market Cap", value: "$10B" },
                { name: "Holding Period", value: "3-6 months" },
              ],
              holdings: [
                { symbol: "JNJ", allocation: 25, performance: 1.2 },
                { symbol: "PG", allocation: 20, performance: 0.8 },
                { symbol: "KO", allocation: 20, performance: 0.5 },
                { symbol: "VZ", allocation: 15, performance: 1.5 },
                { symbol: "WMT", allocation: 20, performance: 0.7 },
              ],
              performanceHistory: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                values: [0.8, 1.5, 2.3, 3.1, 4.5, 5.8],
              },
            },
            strat5: {
              id: "strat5",
              name: "Trend Follower",
              description:
                "Follows established market trends with adaptive entry/exit points and dynamic position sizing based on trend strength.",
              performance: 1.2,
              risk: "Medium",
              status: "Active",
              allocation: 10,
              lastUpdated: "2025-06-04T12:10:00Z",
              inception: "2025-02-15T00:00:00Z",
              totalReturn: 6.5,
              sharpeRatio: 1.5,
              maxDrawdown: -4.8,
              winRate: 60,
              parameters: [
                { name: "Trend Indicator", value: "Moving Average Crossover" },
                { name: "Fast/Slow MAs", value: "20/50 days" },
                { name: "Confirmation Indicator", value: "ADX > 25" },
                { name: "Exit Strategy", value: "Trailing Stop" },
              ],
              holdings: [
                { symbol: "QQQ", allocation: 30, performance: 2.1 },
                { symbol: "SPY", allocation: 25, performance: 1.5 },
                { symbol: "IWM", allocation: 15, performance: 0.8 },
                { symbol: "EEM", allocation: 15, performance: -0.5 },
                { symbol: "GLD", allocation: 15, performance: 1.2 },
              ],
              performanceHistory: {
                labels: ["Feb", "Mar", "Apr", "May", "Jun"],
                values: [1.2, 2.5, 3.8, 5.2, 6.5],
              },
            },
          };

          resolve({
            data: strategies[strategyId] || null,
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching strategy details:", error);
      throw new Error(
        error.response?.data?.message || "Failed to fetch strategy details",
      );
    }
  }

  async updateStrategyAllocation(strategyId, allocation) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              success: true,
              message: "Strategy allocation updated successfully",
              strategy: {
                id: strategyId,
                allocation,
                lastUpdated: new Date().toISOString(),
              },
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error updating strategy allocation:", error);
      throw new Error(
        error.response?.data?.message || "Failed to update strategy allocation",
      );
    }
  }

  async toggleStrategyStatus(strategyId, active) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              success: true,
              message: `Strategy ${active ? "activated" : "deactivated"} successfully`,
              strategy: {
                id: strategyId,
                status: active ? "Active" : "Inactive",
                lastUpdated: new Date().toISOString(),
              },
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error toggling strategy status:", error);
      throw new Error(
        error.response?.data?.message || "Failed to update strategy status",
      );
    }
  }

  async getAvailableStrategies() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: "strat6",
                name: "Mean Reversion",
                description: "Capitalizes on price reversals to the mean",
                risk: "Medium",
                expectedReturn: "8-12%",
                minimumInvestment: 5000,
              },
              {
                id: "strat7",
                name: "Options Volatility",
                description: "Exploits volatility patterns in options markets",
                risk: "High",
                expectedReturn: "15-25%",
                minimumInvestment: 10000,
              },
              {
                id: "strat8",
                name: "Sector Rotation",
                description: "Rotates between sectors based on economic cycles",
                risk: "Medium-Low",
                expectedReturn: "7-10%",
                minimumInvestment: 5000,
              },
            ],
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching available strategies:", error);
      throw new Error(
        error.response?.data?.message || "Failed to fetch available strategies",
      );
    }
  }
}

export const strategyService = new StrategyService();
