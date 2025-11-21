import api from "./api";

class AlertService {
  constructor() {
    this.subscribers = [];
  }

  subscribeToAlerts(callback) {
    this.subscribers.push(callback);

    // Return an object with an unsubscribe method
    return {
      unsubscribe: () => {
        this.subscribers = this.subscribers.filter((cb) => cb !== callback);
      },
    };
  }

  // Simulate receiving a new alert (would be called by a websocket or push notification in a real app)
  _notifySubscribers(alert) {
    this.subscribers.forEach((callback) => callback(alert));
  }

  async getRecentAlerts(limit = 5) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: "alert1",
                type: "TRADE_SIGNAL",
                title: "New trading signal",
                message: "Buy AAPL",
                timestamp: "2025-06-05T10:32:00Z",
                priority: "medium",
                read: false,
              },
              {
                id: "alert2",
                type: "RISK_WARNING",
                title: "Risk threshold exceeded",
                message: "Risk threshold exceeded on Strategy #2",
                timestamp: "2025-06-05T09:45:00Z",
                priority: "high",
                read: false,
              },
              {
                id: "alert3",
                type: "MARKET_UPDATE",
                title: "Market volatility increasing",
                message: "VIX up 15% in the last hour",
                timestamp: "2025-06-05T09:15:00Z",
                priority: "medium",
                read: true,
              },
              {
                id: "alert4",
                type: "TRADE_EXECUTED",
                title: "Trade executed",
                message: "Sold 10 shares of MSFT at $350.25",
                timestamp: "2025-06-05T08:30:00Z",
                priority: "low",
                read: true,
              },
              {
                id: "alert5",
                type: "SYSTEM_UPDATE",
                title: "System maintenance",
                message: "Scheduled maintenance in 2 hours",
                timestamp: "2025-06-05T08:00:00Z",
                priority: "low",
                read: true,
              },
            ],
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching alerts:", error);
      throw new Error(
        error.response?.data?.message || "Failed to fetch alerts",
      );
    }
  }

  async getAllAlerts(page = 1, limit = 20) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          const alerts = [
            {
              id: "alert1",
              type: "TRADE_SIGNAL",
              title: "New trading signal",
              message: "Buy AAPL",
              timestamp: "2025-06-05T10:32:00Z",
              priority: "medium",
              read: false,
            },
            {
              id: "alert2",
              type: "RISK_WARNING",
              title: "Risk threshold exceeded",
              message: "Risk threshold exceeded on Strategy #2",
              timestamp: "2025-06-05T09:45:00Z",
              priority: "high",
              read: false,
            },
            {
              id: "alert3",
              type: "MARKET_UPDATE",
              title: "Market volatility increasing",
              message: "VIX up 15% in the last hour",
              timestamp: "2025-06-05T09:15:00Z",
              priority: "medium",
              read: true,
            },
            {
              id: "alert4",
              type: "TRADE_EXECUTED",
              title: "Trade executed",
              message: "Sold 10 shares of MSFT at $350.25",
              timestamp: "2025-06-05T08:30:00Z",
              priority: "low",
              read: true,
            },
            {
              id: "alert5",
              type: "SYSTEM_UPDATE",
              title: "System maintenance",
              message: "Scheduled maintenance in 2 hours",
              timestamp: "2025-06-05T08:00:00Z",
              priority: "low",
              read: true,
            },
            {
              id: "alert6",
              type: "TRADE_SIGNAL",
              title: "New trading signal",
              message: "Sell GOOGL",
              timestamp: "2025-06-04T15:45:00Z",
              priority: "medium",
              read: true,
            },
            {
              id: "alert7",
              type: "PERFORMANCE_UPDATE",
              title: "Strategy performance update",
              message: "Momentum Alpha up 2.3% today",
              timestamp: "2025-06-04T16:30:00Z",
              priority: "low",
              read: true,
            },
            {
              id: "alert8",
              type: "MARKET_UPDATE",
              title: "Fed announcement",
              message: "Fed maintains interest rates",
              timestamp: "2025-06-04T14:00:00Z",
              priority: "medium",
              read: true,
            },
          ];

          resolve({
            data: {
              alerts: alerts.slice((page - 1) * limit, page * limit),
              pagination: {
                page,
                limit,
                total: alerts.length,
                pages: Math.ceil(alerts.length / limit),
              },
            },
          });
        }, 800);
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching all alerts:", error);
      throw new Error(
        error.response?.data?.message || "Failed to fetch alerts",
      );
    }
  }

  async markAsRead(alertId) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              success: true,
              message: "Alert marked as read",
              alertId,
            },
          });
        }, 500);
      });

      return response.data;
    } catch (error) {
      console.error("Error marking alert as read:", error);
      throw new Error(
        error.response?.data?.message || "Failed to mark alert as read",
      );
    }
  }

  async markAllAsRead() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              success: true,
              message: "All alerts marked as read",
            },
          });
        }, 500);
      });

      return response.data;
    } catch (error) {
      console.error("Error marking all alerts as read:", error);
      throw new Error(
        error.response?.data?.message || "Failed to mark all alerts as read",
      );
    }
  }

  async deleteAlert(alertId) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful response
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              success: true,
              message: "Alert deleted",
              alertId,
            },
          });
        }, 500);
      });

      return response.data;
    } catch (error) {
      console.error("Error deleting alert:", error);
      throw new Error(
        error.response?.data?.message || "Failed to delete alert",
      );
    }
  }

  // Simulate receiving new alerts (for demo purposes)
  simulateNewAlert() {
    const alertTypes = [
      "TRADE_SIGNAL",
      "RISK_WARNING",
      "MARKET_UPDATE",
      "TRADE_EXECUTED",
      "SYSTEM_UPDATE",
    ];
    const priorities = ["low", "medium", "high"];

    const randomType =
      alertTypes[Math.floor(Math.random() * alertTypes.length)];
    const randomPriority =
      priorities[Math.floor(Math.random() * priorities.length)];

    let title, message;

    switch (randomType) {
      case "TRADE_SIGNAL":
        title = "New trading signal";
        message = `${Math.random() > 0.5 ? "Buy" : "Sell"} ${["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"][Math.floor(Math.random() * 5)]}`;
        break;
      case "RISK_WARNING":
        title = "Risk threshold exceeded";
        message = `Risk threshold exceeded on Strategy #${Math.floor(Math.random() * 5) + 1}`;
        break;
      case "MARKET_UPDATE":
        title = "Market update";
        message = `${["S&P 500", "NASDAQ", "DOW", "Russell 2000"][Math.floor(Math.random() * 4)]} ${Math.random() > 0.5 ? "up" : "down"} ${(Math.random() * 2).toFixed(1)}%`;
        break;
      case "TRADE_EXECUTED":
        title = "Trade executed";
        message = `${Math.random() > 0.5 ? "Bought" : "Sold"} ${Math.floor(Math.random() * 20) + 1} shares of ${["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"][Math.floor(Math.random() * 5)]} at $${(Math.random() * 1000 + 100).toFixed(2)}`;
        break;
      case "SYSTEM_UPDATE":
        title = "System update";
        message = "New system update available";
        break;
      default:
        title = "Notification";
        message = "You have a new notification";
    }

    const newAlert = {
      id: `alert${Date.now()}`,
      type: randomType,
      title,
      message,
      timestamp: new Date().toISOString(),
      priority: randomPriority,
      read: false,
    };

    this._notifySubscribers(newAlert);

    return newAlert;
  }
}

export const alertService = new AlertService();
