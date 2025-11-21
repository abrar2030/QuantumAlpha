import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
} from "react-native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useTheme } from "../../context/ThemeContext";

const NotificationsScreen = () => {
  const { theme } = useTheme();

  // Mock notifications data
  const notifications = [
    {
      id: "notif1",
      type: "system",
      title: "System Update",
      message:
        "QuantumAlpha has been updated to version 1.0.0 with new features and improvements.",
      timestamp: "2025-06-05T08:00:00Z",
      read: false,
    },
    {
      id: "notif2",
      type: "feature",
      title: "New Feature Available",
      message: "Try our new AI-powered strategy recommendation engine.",
      timestamp: "2025-06-04T14:30:00Z",
      read: true,
    },
    {
      id: "notif3",
      type: "promo",
      title: "Premium Discount",
      message: "Upgrade to Premium and get 20% off for the first 3 months.",
      timestamp: "2025-06-03T10:15:00Z",
      read: true,
    },
    {
      id: "notif4",
      type: "system",
      title: "Account Security",
      message:
        "We recommend enabling two-factor authentication for enhanced security.",
      timestamp: "2025-06-02T16:45:00Z",
      read: true,
    },
  ];

  const getNotificationIcon = (type) => {
    switch (type) {
      case "system":
        return "cog";
      case "feature":
        return "star";
      case "promo":
        return "tag";
      default:
        return "bell";
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case "system":
        return theme.info;
      case "feature":
        return theme.primary;
      case "promo":
        return theme.warning;
      default:
        return theme.text;
    }
  };

  const renderNotification = (notification, index) => {
    return (
      <TouchableOpacity
        key={notification.id}
        style={[
          styles.notificationItem,
          {
            backgroundColor: notification.read ? theme.card : theme.card + "80",
          },
          index < notifications.length - 1 && styles.notificationBorder,
          { borderBottomColor: theme.border },
        ]}
        onPress={() => {
          // In a real app, this would mark the notification as read
          alert(`Notification: ${notification.title}`);
        }}
      >
        <View
          style={[
            styles.notificationIcon,
            { backgroundColor: getNotificationColor(notification.type) + "20" },
          ]}
        >
          <Icon
            name={getNotificationIcon(notification.type)}
            size={24}
            color={getNotificationColor(notification.type)}
          />
        </View>

        <View style={styles.notificationContent}>
          <View style={styles.notificationHeader}>
            <Text style={[styles.notificationTitle, { color: theme.text }]}>
              {notification.title}
            </Text>
            {!notification.read && (
              <View
                style={[styles.unreadDot, { backgroundColor: theme.primary }]}
              />
            )}
          </View>

          <Text
            style={[styles.notificationMessage, { color: theme.text + "CC" }]}
          >
            {notification.message}
          </Text>

          <Text style={[styles.notificationTime, { color: theme.text + "99" }]}>
            {new Date(notification.timestamp).toLocaleDateString()} at{" "}
            {new Date(notification.timestamp).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <View style={[styles.header, { backgroundColor: theme.card }]}>
        <Text style={[styles.headerTitle, { color: theme.text }]}>
          Notifications
        </Text>
        <TouchableOpacity
          style={styles.clearButton}
          onPress={() => {
            // In a real app, this would clear all notifications
            alert("Would clear all notifications");
          }}
        >
          <Text style={[styles.clearButtonText, { color: theme.primary }]}>
            Clear All
          </Text>
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {notifications.length > 0 ? (
          notifications.map(renderNotification)
        ) : (
          <View style={styles.emptyContainer}>
            <Image
              source={require("../../assets/empty-notifications.png")}
              style={styles.emptyImage}
              resizeMode="contain"
            />
            <Text style={[styles.emptyText, { color: theme.text }]}>
              No notifications
            </Text>
            <Text style={[styles.emptySubtext, { color: theme.text + "99" }]}>
              You're all caught up! New notifications will appear here.
            </Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: "bold",
  },
  clearButton: {
    padding: 8,
  },
  clearButtonText: {
    fontSize: 16,
    fontWeight: "500",
  },
  scrollContent: {
    flexGrow: 1,
  },
  notificationItem: {
    flexDirection: "row",
    padding: 16,
  },
  notificationBorder: {
    borderBottomWidth: 1,
  },
  notificationIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 16,
  },
  notificationContent: {
    flex: 1,
  },
  notificationHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  notificationTitle: {
    fontSize: 16,
    fontWeight: "bold",
    flex: 1,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginLeft: 8,
  },
  notificationMessage: {
    fontSize: 14,
    marginBottom: 8,
  },
  notificationTime: {
    fontSize: 12,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 40,
  },
  emptyImage: {
    width: 120,
    height: 120,
    marginBottom: 20,
    opacity: 0.7,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    textAlign: "center",
  },
});

export default NotificationsScreen;
