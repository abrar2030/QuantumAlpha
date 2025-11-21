import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Dimensions,
  Animated,
  TextInput,
} from "react-native";
import { LineChart, PieChart } from "react-native-chart-kit";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useNavigation } from "@react-navigation/native";
import { useTheme } from "../../context/ThemeContext";
import { portfolioService } from "../../services/portfolioService";

const PortfolioScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [portfolioData, setPortfolioData] = useState(null);
  const [performanceData, setPerformanceData] = useState(null);
  const [assetAllocation, setAssetAllocation] = useState([]);
  const [holdings, setHoldings] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState("1M");

  // Animation values
  const fadeAnim = new Animated.Value(0);
  const translateY = new Animated.Value(50);

  const screenWidth = Dimensions.get("window").width;

  useEffect(() => {
    loadPortfolioData();

    // Start animations when component mounts
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration: 800,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const loadPortfolioData = async () => {
    try {
      setLoading(true);

      // In a real app, these would be API calls
      const portfolioSummary = await portfolioService.getPortfolioSummary();
      const performance =
        await portfolioService.getPerformanceHistory(selectedPeriod);
      const allocation = await portfolioService.getAssetAllocation();
      const holdingsData = await portfolioService.getHoldings();

      setPortfolioData(portfolioSummary);
      setPerformanceData(performance);
      setAssetAllocation(allocation);
      setHoldings(holdingsData);
    } catch (error) {
      console.error("Error loading portfolio data:", error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handlePeriodChange = async (period) => {
    setSelectedPeriod(period);
    try {
      const performance = await portfolioService.getPerformanceHistory(period);
      setPerformanceData(performance);
    } catch (error) {
      console.error("Error loading performance data:", error);
    }
  };

  if (loading) {
    return (
      <View
        style={[styles.loadingContainer, { backgroundColor: theme.background }]}
      >
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading portfolio data...
        </Text>
      </View>
    );
  }

  const chartConfig = {
    backgroundColor: theme.chartBackground,
    backgroundGradientFrom: theme.chartBackgroundGradientFrom,
    backgroundGradientTo: theme.chartBackgroundGradientTo,
    decimalPlaces: 0,
    color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
    labelColor: (opacity = 1) =>
      `rgba(${theme.isDarkMode ? "255, 255, 255" : "0, 0, 0"}, ${opacity})`,
    style: {
      borderRadius: 16,
    },
    propsForDots: {
      r: "6",
      strokeWidth: "2",
      stroke: theme.primary,
    },
  };

  const pieChartData = assetAllocation.map((item, index) => {
    const colors = [
      "#1aff92", // Primary green
      "#0a84ff", // Blue
      "#ffcc00", // Yellow
      "#ff453a", // Red
      "#32d74b", // Green
      "#bf5af2", // Purple
      "#ff9f0a", // Orange
    ];

    return {
      name: item.name,
      value: item.percentage,
      color: colors[index % colors.length],
      legendFontColor: theme.text,
      legendFontSize: 12,
    };
  });

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Animated.View
        style={[
          styles.header,
          {
            backgroundColor: theme.card,
            opacity: fadeAnim,
            transform: [{ translateY }],
          },
        ]}
      >
        <Text style={[styles.headerTitle, { color: theme.text }]}>
          Portfolio
        </Text>
        <Text style={[styles.portfolioValue, { color: theme.text }]}>
          ${portfolioData.totalValue.toLocaleString()}
        </Text>
        <View style={styles.changeContainer}>
          <Text
            style={[
              portfolioData.dailyChange >= 0
                ? [styles.positiveChange, { color: theme.success }]
                : [styles.negativeChange, { color: theme.error }],
            ]}
          >
            {portfolioData.dailyChange >= 0 ? "+" : ""}
            {portfolioData.dailyChange.toLocaleString()} (
            {portfolioData.percentChange}%)
          </Text>
          <Text style={[styles.changeLabel, { color: theme.text + "CC" }]}>
            Today
          </Text>
        </View>
      </Animated.View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <View style={styles.cardHeader}>
            <Text style={[styles.cardTitle, { color: theme.text }]}>
              Performance
            </Text>
            <View style={styles.periodSelector}>
              {["1D", "1W", "1M", "3M", "1Y", "ALL"].map((period) => (
                <TouchableOpacity
                  key={period}
                  style={[
                    styles.periodButton,
                    selectedPeriod === period && [
                      styles.activePeriodButton,
                      { backgroundColor: theme.primary },
                    ],
                  ]}
                  onPress={() => handlePeriodChange(period)}
                >
                  <Text
                    style={[
                      styles.periodButtonText,
                      {
                        color:
                          selectedPeriod === period ? "#FFFFFF" : theme.text,
                      },
                    ]}
                  >
                    {period}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          <LineChart
            data={{
              labels: performanceData.labels,
              datasets: [
                {
                  data: performanceData.values,
                },
              ],
            }}
            width={screenWidth - 40}
            height={220}
            chartConfig={chartConfig}
            bezier
            style={styles.chart}
          />
        </View>

        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Asset Allocation
          </Text>

          <View style={styles.pieChartContainer}>
            <PieChart
              data={pieChartData}
              width={screenWidth - 40}
              height={220}
              chartConfig={chartConfig}
              accessor="value"
              backgroundColor="transparent"
              paddingLeft="15"
              absolute
            />
          </View>

          <View style={styles.allocationLegend}>
            {assetAllocation.map((item, index) => (
              <View key={index} style={styles.legendItem}>
                <View
                  style={[
                    styles.legendColor,
                    { backgroundColor: pieChartData[index].color },
                  ]}
                />
                <Text style={[styles.legendText, { color: theme.text }]}>
                  {item.name}: {item.percentage}% ($
                  {item.value.toLocaleString()})
                </Text>
              </View>
            ))}
          </View>
        </View>

        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <View style={styles.cardHeader}>
            <Text style={[styles.cardTitle, { color: theme.text }]}>
              Holdings
            </Text>
            <TouchableOpacity
              style={styles.viewAllButton}
              onPress={() => {
                // In a real app, this would navigate to a detailed holdings screen
                alert("Would navigate to detailed holdings view");
              }}
            >
              <Text style={[styles.viewAllText, { color: theme.primary }]}>
                View All
              </Text>
              <Icon name="chevron-right" size={16} color={theme.primary} />
            </TouchableOpacity>
          </View>

          <View style={styles.holdingsHeader}>
            <Text
              style={[styles.holdingsHeaderText, { color: theme.text + "CC" }]}
            >
              Asset
            </Text>
            <Text
              style={[styles.holdingsHeaderText, { color: theme.text + "CC" }]}
            >
              Value
            </Text>
            <Text
              style={[styles.holdingsHeaderText, { color: theme.text + "CC" }]}
            >
              Change
            </Text>
          </View>

          {holdings.map((holding, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.holdingItem,
                index < holdings.length - 1 && {
                  borderBottomWidth: 1,
                  borderBottomColor: theme.border,
                },
              ]}
              onPress={() => {
                // In a real app, this would navigate to a detailed asset view
                alert(`Would navigate to ${holding.symbol} details`);
              }}
            >
              <View style={styles.holdingInfo}>
                <Text style={[styles.holdingSymbol, { color: theme.text }]}>
                  {holding.symbol}
                </Text>
                <Text
                  style={[styles.holdingName, { color: theme.text + "CC" }]}
                >
                  {holding.name}
                </Text>
              </View>

              <View style={styles.holdingValue}>
                <Text style={[styles.holdingValueText, { color: theme.text }]}>
                  ${holding.value.toLocaleString()}
                </Text>
                <Text
                  style={[styles.holdingQuantity, { color: theme.text + "CC" }]}
                >
                  {holding.quantity} @ ${holding.price}
                </Text>
              </View>

              <View style={styles.holdingChange}>
                <Text
                  style={[
                    styles.holdingChangeText,
                    {
                      color: holding.change >= 0 ? theme.success : theme.error,
                    },
                  ]}
                >
                  {holding.change >= 0 ? "+" : ""}
                  {holding.change}%
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <View style={styles.cardHeader}>
            <Text style={[styles.cardTitle, { color: theme.text }]}>
              Quick Actions
            </Text>
          </View>

          <View style={styles.actionButtons}>
            <TouchableOpacity
              style={[
                styles.actionButton,
                { backgroundColor: theme.primary + "20" },
              ]}
              onPress={() => {
                // In a real app, this would navigate to the deposit screen
                navigation.navigate("TradeTab");
              }}
            >
              <Icon name="bank-transfer-in" size={24} color={theme.primary} />
              <Text style={[styles.actionButtonText, { color: theme.text }]}>
                Deposit
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.actionButton,
                { backgroundColor: theme.error + "20" },
              ]}
              onPress={() => {
                // In a real app, this would navigate to the withdraw screen
                navigation.navigate("TradeTab");
              }}
            >
              <Icon name="bank-transfer-out" size={24} color={theme.error} />
              <Text style={[styles.actionButtonText, { color: theme.text }]}>
                Withdraw
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.actionButton,
                { backgroundColor: theme.info + "20" },
              ]}
              onPress={() => {
                // In a real app, this would navigate to the trade screen
                navigation.navigate("TradeTab");
              }}
            >
              <Icon name="swap-horizontal" size={24} color={theme.info} />
              <Text style={[styles.actionButtonText, { color: theme.text }]}>
                Trade
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.actionButton,
                { backgroundColor: theme.warning + "20" },
              ]}
              onPress={() => {
                // In a real app, this would navigate to the strategy screen
                navigation.navigate("StrategyTab");
              }}
            >
              <Icon name="strategy" size={24} color={theme.warning} />
              <Text style={[styles.actionButtonText, { color: theme.text }]}>
                Strategies
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
  },
  header: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  headerTitle: {
    fontSize: 16,
    opacity: 0.7,
  },
  portfolioValue: {
    fontSize: 32,
    fontWeight: "bold",
    marginTop: 5,
  },
  changeContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 5,
  },
  positiveChange: {
    fontSize: 18,
    fontWeight: "500",
  },
  negativeChange: {
    fontSize: 18,
    fontWeight: "500",
  },
  changeLabel: {
    fontSize: 14,
    marginLeft: 8,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  card: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
  },
  periodSelector: {
    flexDirection: "row",
    backgroundColor: "rgba(0,0,0,0.05)",
    borderRadius: 16,
    padding: 2,
  },
  periodButton: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 14,
  },
  activePeriodButton: {
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1.5,
    elevation: 2,
  },
  periodButtonText: {
    fontSize: 12,
    fontWeight: "500",
  },
  chart: {
    borderRadius: 16,
    marginTop: 10,
  },
  pieChartContainer: {
    alignItems: "center",
    marginVertical: 10,
  },
  allocationLegend: {
    marginTop: 10,
  },
  legendItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  legendText: {
    fontSize: 14,
  },
  viewAllButton: {
    flexDirection: "row",
    alignItems: "center",
  },
  viewAllText: {
    fontSize: 14,
    fontWeight: "500",
    marginRight: 4,
  },
  holdingsHeader: {
    flexDirection: "row",
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  holdingsHeaderText: {
    fontSize: 12,
    fontWeight: "500",
  },
  holdingItem: {
    flexDirection: "row",
    paddingVertical: 12,
  },
  holdingInfo: {
    flex: 2,
  },
  holdingSymbol: {
    fontSize: 16,
    fontWeight: "500",
  },
  holdingName: {
    fontSize: 12,
    marginTop: 2,
  },
  holdingValue: {
    flex: 2,
    alignItems: "flex-end",
  },
  holdingValueText: {
    fontSize: 16,
    fontWeight: "500",
  },
  holdingQuantity: {
    fontSize: 12,
    marginTop: 2,
  },
  holdingChange: {
    flex: 1,
    alignItems: "flex-end",
  },
  holdingChangeText: {
    fontSize: 16,
    fontWeight: "500",
  },
  actionButtons: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    marginTop: 10,
  },
  actionButton: {
    width: "48%",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginBottom: 10,
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: "500",
    marginTop: 8,
  },
});

export default PortfolioScreen;
