/**
 * Unit tests for DashboardScreen component
 */
import React from "react";
import {
  render,
  screen,
  fireEvent,
  waitFor,
} from "@testing-library/react-native";
import DashboardScreen from "../../../QuantumAlpha-main/mobile-frontend/src/screens/dashboard/DashboardScreen";

// Mock dependencies
jest.mock("@react-navigation/native", () => ({
  useNavigation: () => ({
    navigate: jest.fn(),
  }),
}));

jest.mock("react-native-chart-kit", () => ({
  LineChart: "LineChart",
}));

jest.mock("react-native-vector-icons/Feather", () => "Icon");

// Mock components
jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/components/dashboard/MarketOverview",
  () => "MarketOverview",
);
jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/components/dashboard/StrategyCard",
  () => "StrategyCard",
);
jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/components/dashboard/AlertItem",
  () => "AlertItem",
);

// Mock hooks
jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/hooks/useTheme",
  () => () => ({
    primary: "#1976d2",
    background: "#ffffff",
    card: "#f5f5f5",
    text: "#000000",
    border: "#e0e0e0",
    notification: "#ff4081",
    error: "#f44336",
    success: "#4caf50",
    warning: "#ff9800",
    chartBackground: "#ffffff",
    chartBackgroundGradientFrom: "#ffffff",
    chartBackgroundGradientTo: "#f5f5f5",
    isDarkMode: false,
  }),
);

// Mock services
jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/services/portfolioService",
  () => ({
    getPortfolioSummary: jest.fn().mockResolvedValue({
      totalValue: 125000,
      dailyChange: 2500,
      dailyChangePercent: 2.0,
      positions: [
        { symbol: "AAPL", quantity: 100, currentValue: 15000 },
        { symbol: "MSFT", quantity: 50, currentValue: 12500 },
      ],
    }),
    getPerformanceData: jest.fn().mockResolvedValue([
      { date: "2023-01-01", value: 100000 },
      { date: "2023-02-01", value: 105000 },
      { date: "2023-03-01", value: 110000 },
      { date: "2023-04-01", value: 115000 },
      { date: "2023-05-01", value: 125000 },
    ]),
  }),
);

jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/services/strategyService",
  () => ({
    getActiveStrategies: jest.fn().mockResolvedValue([
      {
        id: "strategy1",
        name: "Momentum Strategy",
        performance: 12.5,
        risk: "medium",
      },
      {
        id: "strategy2",
        name: "Value Strategy",
        performance: 8.3,
        risk: "low",
      },
    ]),
  }),
);

jest.mock(
  "../../../QuantumAlpha-main/mobile-frontend/src/services/alertService",
  () => ({
    getRecentAlerts: jest.fn().mockResolvedValue([
      {
        id: "alert1",
        type: "price",
        symbol: "AAPL",
        message: "AAPL reached target price",
        timestamp: "2023-05-01T10:30:00Z",
      },
      {
        id: "alert2",
        type: "strategy",
        symbol: "MSFT",
        message: "Buy signal for MSFT",
        timestamp: "2023-05-01T09:15:00Z",
      },
    ]),
  }),
);

describe("DashboardScreen Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders loading state initially", () => {
    render(<DashboardScreen />);

    expect(screen.getByTestId("loading-indicator")).toBeTruthy();
    expect(screen.getByText("Loading dashboard...")).toBeTruthy();
  });

  test("renders dashboard content after loading", async () => {
    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Check portfolio summary
    expect(screen.getByText("$125,000")).toBeTruthy();
    expect(screen.getByText("+$2,500 (2.0%)")).toBeTruthy();

    // Check performance chart
    expect(screen.getByTestId("performance-chart")).toBeTruthy();

    // Check market overview
    expect(screen.getByTestId("market-overview")).toBeTruthy();

    // Check strategies section
    expect(screen.getByText("Active Strategies")).toBeTruthy();
    expect(screen.getByText("See All")).toBeTruthy();

    // Check strategy cards
    const strategyCards = screen.getAllByTestId("strategy-card");
    expect(strategyCards.length).toBe(2);

    // Check alerts section
    expect(screen.getByText("Recent Alerts")).toBeTruthy();

    // Check alert items
    const alertItems = screen.getAllByTestId("alert-item");
    expect(alertItems.length).toBe(2);
  });

  test("handles empty alerts gracefully", async () => {
    // Mock empty alerts
    require("../../../QuantumAlpha-main/mobile-frontend/src/services/alertService").getRecentAlerts.mockResolvedValueOnce(
      [],
    );

    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Check empty state for alerts
    expect(screen.getByText("No recent alerts")).toBeTruthy();
  });

  test("navigates to strategy details when strategy card is pressed", async () => {
    const navigation = require("@react-navigation/native").useNavigation();

    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Find and press the first strategy card
    const strategyCards = screen.getAllByTestId("strategy-card");
    fireEvent.press(strategyCards[0]);

    // Check if navigation was called with correct params
    expect(navigation.navigate).toHaveBeenCalledWith("StrategyDetail", {
      strategyId: "strategy1",
    });
  });

  test('navigates to alerts screen when "See All" is pressed in alerts section', async () => {
    const navigation = require("@react-navigation/native").useNavigation();

    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Find and press the "See All" button in alerts section
    const seeAllButtons = screen.getAllByText("See All");
    // The second "See All" button should be for alerts
    fireEvent.press(seeAllButtons[1]);

    // Check if navigation was called with correct screen
    expect(navigation.navigate).toHaveBeenCalledWith("AlertsTab");
  });

  test('navigates to strategies screen when "See All" is pressed in strategies section', async () => {
    const navigation = require("@react-navigation/native").useNavigation();

    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Find and press the "See All" button in strategies section
    const seeAllButtons = screen.getAllByText("See All");
    // The first "See All" button should be for strategies
    fireEvent.press(seeAllButtons[0]);

    // Check if navigation was called with correct screen
    expect(navigation.navigate).toHaveBeenCalledWith("StrategyTab");
  });

  test("handles error state gracefully", async () => {
    // Mock service error
    require("../../../QuantumAlpha-main/mobile-frontend/src/services/portfolioService").getPortfolioSummary.mockRejectedValueOnce(
      new Error("Failed to fetch portfolio data"),
    );

    render(<DashboardScreen />);

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Check error state
    expect(screen.getByText("Error loading dashboard data")).toBeTruthy();
    expect(screen.getByText("Please try again later")).toBeTruthy();
    expect(screen.getByTestId("retry-button")).toBeTruthy();

    // Test retry functionality
    require("../../../QuantumAlpha-main/mobile-frontend/src/services/portfolioService").getPortfolioSummary.mockResolvedValueOnce(
      {
        totalValue: 125000,
        dailyChange: 2500,
        dailyChangePercent: 2.0,
        positions: [
          { symbol: "AAPL", quantity: 100, currentValue: 15000 },
          { symbol: "MSFT", quantity: 50, currentValue: 12500 },
        ],
      },
    );

    fireEvent.press(screen.getByTestId("retry-button"));

    // Should show loading again
    expect(screen.getByTestId("loading-indicator")).toBeTruthy();

    // Wait for loading to complete again
    await waitFor(() => {
      expect(screen.queryByTestId("loading-indicator")).toBeNull();
    });

    // Should show dashboard content now
    expect(screen.getByText("$125,000")).toBeTruthy();
  });
});
