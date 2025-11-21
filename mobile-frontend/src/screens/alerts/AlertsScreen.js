import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Animated,
  TextInput,
  Dimensions,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useTheme } from "../../context/ThemeContext";
import { useAlert } from "../../context/AlertContext";
import { alertService } from "../../services/alertService";

const AlertsScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  const { markAllAsRead } = useAlert();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState("all");

  // Animation values
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const translateY = React.useRef(new Animated.Value(50)).current;

  useEffect(() => {
    loadAlerts();

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

    // Set up alert listener for real-time updates
    const alertListener = alertService.subscribeToAlerts((newAlert) => {
      setAlerts((prev) => [newAlert, ...prev]);
    });

    // Simulate receiving new alerts every 30 seconds (for demo purposes)
    const interval = setInterval(() => {
      const newAlert = alertService.simulateNewAlert();
      setAlerts((prev) => [newAlert, ...prev]);
    }, 30000);

    return () => {
      alertListener.unsubscribe();
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    filterAlerts();
  }, [alerts, searchQuery, activeFilter]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const response = await alertService.getAllAlerts();
      setAlerts(response.alerts);
    } catch (error) {
      console.error("Error loading alerts:", error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadAlerts();
  };

  const filterAlerts = () => {
    let filtered = [...alerts];

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(
        (alert) =>
          alert.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          alert.message.toLowerCase().includes(searchQuery.toLowerCase()),
      );
    }

    // Apply type filter
    if (activeFilter !== "all") {
      filtered = filtered.filter((alert) => alert.type === activeFilter);
    }

    setFilteredAlerts(filtered);
  };

  const handleMarkAsRead = async (alertId) => {
    try {
      await alertService.markAsRead(alertId);

      // Update local state
      setAlerts((prev) =>
        prev.map((alert) =>
          alert.id === alertId ? { ...alert, read: true } : alert,
        ),
      );
    } catch (error) {
      console.error("Error marking alert as read:", error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await alertService.markAllAsRead();

      // Update local state
      setAlerts((prev) => prev.map((alert) => ({ ...alert, read: true })));

      // Update context
      markAllAsRead();
    } catch (error) {
      console.error("Error marking all alerts as read:", error);
    }
  };

  const handleDeleteAlert = async (alertId) => {
    try {
      await alertService.deleteAlert(alertId);

      // Update local state
      setAlerts((prev) => prev.filter((alert) => alert.id !== alertId));
    } catch (error) {
      console.error("Error deleting alert:", error);
    }
  };

  const renderAlertItem = ({ item, index }) => {
    const itemFadeAnim = React.useRef(new Animated.Value(0)).current;
    const itemTranslateX = React.useRef(new Animated.Value(-50)).current;

    React.useEffect(() => {
      // Stagger the animations for each item
      Animated.parallel([
        Animated.timing(itemFadeAnim, {
          toValue: 1,
          duration: 500,
          delay: index * 50,
          useNativeDriver: true,
        }),
        Animated.timing(itemTranslateX, {
          toValue: 0,
          duration: 500,
          delay: index * 50,
          useNativeDriver: true,
        }),
      ]).start();
    }, []);

    const getPriorityColor = () => {
      switch (item.priority) {
        case "high":
          return theme.error;
        case "medium":
          return theme.warning;
        case "low":
        default:
          return theme.info;
      }
    };

    const getTypeIcon = () => {
      switch (item.type) {
        case "TRADE_SIGNAL":
          return "signal";
        case "RISK_WARNING":
          return "alert";
        case "MARKET_UPDATE":
          return "chart-line";
        case "TRADE_EXECUTED":
          return "check-circle";
        case "SYSTEM_UPDATE":
          return "cog";
        case "PERFORMANCE_UPDATE":
          return "trending-up";
        default:
          return "bell";
      }
    };

    return (
      <Animated.View
        style={[
          styles.alertItemContainer,
          {
            opacity: itemFadeAnim,
            transform: [{ translateX: itemTranslateX }],
          },
        ]}
      >
        <TouchableOpacity
          style={[
            styles.alertItem,
            {
              backgroundColor: theme.card,
              opacity: item.read ? 0.7 : 1,
            },
          ]}
          onPress={() => {
            if (!item.read) {
              handleMarkAsRead(item.id);
            }
          }}
        >
          <View
            style={[
              styles.priorityIndicator,
              { backgroundColor: getPriorityColor() },
            ]}
          />

          <View style={styles.alertIconContainer}>
            <View
              style={[
                styles.alertIcon,
                {
                  backgroundColor: getPriorityColor() + "20",
                },
              ]}
            >
              <Icon name={getTypeIcon()} size={20} color={getPriorityColor()} />
            </View>
          </View>

          <View style={styles.alertContent}>
            <View style={styles.alertHeader}>
              <Text
                style={[
                  styles.alertTitle,
                  {
                    color: theme.text,
                    fontWeight: item.read ? "normal" : "bold",
                  },
                ]}
              >
                {item.title}
              </Text>
              {!item.read && (
                <View
                  style={[styles.unreadDot, { backgroundColor: theme.primary }]}
                />
              )}
            </View>

            <Text style={[styles.alertMessage, { color: theme.text + "CC" }]}>
              {item.message}
            </Text>

            <View style={styles.alertFooter}>
              <Text style={[styles.alertTime, { color: theme.text + "99" }]}>
                {new Date(item.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
                {" · "}
                {new Date(item.timestamp).toLocaleDateString()}
              </Text>

              <TouchableOpacity
                style={styles.deleteButton}
                onPress={() => handleDeleteAlert(item.id)}
              >
                <Icon
                  name="delete-outline"
                  size={18}
                  color={theme.text + "99"}
                />
              </TouchableOpacity>
            </View>
          </View>
        </TouchableOpacity>
      </Animated.View>
    );
  };

  const renderFilterButton = (filter, label, iconName) => {
    const isActive = activeFilter === filter;

    return (
      <TouchableOpacity
        style={[
          styles.filterButton,
          {
            backgroundColor: isActive ? theme.primary : theme.card,
            borderColor: isActive ? theme.primary : theme.border,
          },
        ]}
        onPress={() => setActiveFilter(filter)}
      >
        <Icon
          name={iconName}
          size={16}
          color={isActive ? "#FFFFFF" : theme.text}
        />
        <Text
          style={[
            styles.filterButtonText,
            {
              color: isActive ? "#FFFFFF" : theme.text,
            },
          ]}
        >
          {label}
        </Text>
      </TouchableOpacity>
    );
  };

  if (loading && !refreshing) {
    return (
      <View
        style={[styles.loadingContainer, { backgroundColor: theme.background }]}
      >
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading alerts...
        </Text>
      </View>
    );
  }

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
        <View style={styles.searchContainer}>
          <Icon name="magnify" size={20} color={theme.text + "99"} />
          <TextInput
            style={[styles.searchInput, { color: theme.text }]}
            placeholder="Search alerts..."
            placeholderTextColor={theme.text + "99"}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
          {searchQuery ? (
            <TouchableOpacity onPress={() => setSearchQuery("")}>
              <Icon name="close" size={20} color={theme.text + "99"} />
            </TouchableOpacity>
          ) : null}
        </View>

        <View style={styles.filterContainer}>
          {renderFilterButton("all", "All", "bell")}
          {renderFilterButton("TRADE_SIGNAL", "Signals", "signal")}
          {renderFilterButton("RISK_WARNING", "Warnings", "alert")}
          {renderFilterButton("MARKET_UPDATE", "Market", "chart-line")}
          {renderFilterButton("TRADE_EXECUTED", "Trades", "check-circle")}
        </View>
      </Animated.View>

      <View style={styles.listContainer}>
        <View style={styles.listHeader}>
          <Text style={[styles.listTitle, { color: theme.text }]}>
            {filteredAlerts.length}{" "}
            {filteredAlerts.length === 1 ? "Alert" : "Alerts"}
          </Text>

          <TouchableOpacity
            style={styles.markAllButton}
            onPress={handleMarkAllAsRead}
          >
            <Icon name="check-all" size={18} color={theme.primary} />
            <Text style={[styles.markAllText, { color: theme.primary }]}>
              Mark all as read
            </Text>
          </TouchableOpacity>
        </View>

        <FlatList
          data={filteredAlerts}
          renderItem={renderAlertItem}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor={theme.primary}
              colors={[theme.primary]}
            />
          }
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Icon name="bell-off" size={60} color={theme.text + "60"} />
              <Text style={[styles.emptyText, { color: theme.text }]}>
                No alerts found
              </Text>
              <Text style={[styles.emptySubtext, { color: theme.text + "99" }]}>
                {searchQuery || activeFilter !== "all"
                  ? "Try changing your filters"
                  : "New alerts will appear here"}
              </Text>
            </View>
          }
        />
      </View>
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
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(0,0,0,0.05)",
    borderRadius: 8,
    paddingHorizontal: 12,
    height: 40,
  },
  searchInput: {
    flex: 1,
    marginLeft: 8,
    fontSize: 16,
  },
  filterContainer: {
    flexDirection: "row",
    marginTop: 12,
    flexWrap: "wrap",
  },
  filterButton: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginRight: 8,
    marginBottom: 8,
    borderWidth: 1,
  },
  filterButtonText: {
    fontSize: 12,
    fontWeight: "500",
    marginLeft: 4,
  },
  listContainer: {
    flex: 1,
  },
  listHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  listTitle: {
    fontSize: 16,
    fontWeight: "500",
  },
  markAllButton: {
    flexDirection: "row",
    alignItems: "center",
  },
  markAllText: {
    fontSize: 14,
    marginLeft: 4,
  },
  listContent: {
    padding: 16,
    paddingTop: 0,
  },
  alertItemContainer: {
    marginBottom: 12,
  },
  alertItem: {
    borderRadius: 12,
    overflow: "hidden",
    flexDirection: "row",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  priorityIndicator: {
    width: 4,
    height: "100%",
  },
  alertIconContainer: {
    padding: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  alertIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: "center",
    justifyContent: "center",
  },
  alertContent: {
    flex: 1,
    padding: 12,
    paddingLeft: 8,
  },
  alertHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  alertTitle: {
    fontSize: 16,
    flex: 1,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginLeft: 8,
  },
  alertMessage: {
    fontSize: 14,
    marginTop: 4,
  },
  alertFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 8,
  },
  alertTime: {
    fontSize: 12,
  },
  deleteButton: {
    padding: 4,
  },
  emptyContainer: {
    alignItems: "center",
    justifyContent: "center",
    padding: 40,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: "bold",
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    marginTop: 8,
    textAlign: "center",
  },
});

export default AlertsScreen;
