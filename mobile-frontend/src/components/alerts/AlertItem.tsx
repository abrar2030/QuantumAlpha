import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
} from "react-native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useTheme } from "../../context/ThemeContext";
import { Alert } from "../../types";

interface AlertItemProps {
  alert: Alert;
  onPress?: () => void;
  onDismiss?: (id: string) => void;
}

const AlertItem: React.FC<AlertItemProps> = ({ alert, onPress, onDismiss }) => {
  const { theme } = useTheme();
  const [dismissed, setDismissed] = React.useState(false);
  const slideAnim = React.useRef(new Animated.Value(0)).current;
  const opacityAnim = React.useRef(new Animated.Value(1)).current;

  const getAlertIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case "price":
        return "chart-line";
      case "news":
        return "newspaper";
      case "trade":
        return "swap-horizontal";
      case "system":
        return "cog";
      case "warning":
        return "alert";
      case "error":
        return "alert-circle";
      default:
        return "bell";
    }
  };

  const getAlertColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case "high":
      case "critical":
        return "#ff4d4d";
      case "medium":
        return "#ffcc00";
      case "low":
        return "#34c759";
      default:
        return theme.primary;
    }
  };

  const handleDismiss = () => {
    if (onDismiss && alert.id) {
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start(() => {
        setDismissed(true);
        onDismiss(alert.id);
      });
    }
  };

  if (dismissed) {
    return null;
  }

  const alertColor = getAlertColor(alert.priority || "low");
  const slideTranslate = slideAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 300],
  });

  return (
    <Animated.View
      style={[
        styles.container,
        {
          backgroundColor: theme.card,
          borderLeftColor: alertColor,
          opacity: opacityAnim,
          transform: [{ translateX: slideTranslate }],
        },
      ]}
    >
      <TouchableOpacity
        style={styles.content}
        onPress={onPress}
        activeOpacity={0.7}
      >
        <View
          style={[styles.iconContainer, { backgroundColor: alertColor + "20" }]}
        >
          <Icon name={getAlertIcon(alert.type)} size={24} color={alertColor} />
        </View>

        <View style={styles.textContainer}>
          <Text style={[styles.title, { color: theme.text }]} numberOfLines={1}>
            {alert.title}
          </Text>
          <Text
            style={[styles.message, { color: theme.text + "CC" }]}
            numberOfLines={2}
          >
            {alert.message}
          </Text>
          {alert.timestamp && (
            <Text style={[styles.timestamp, { color: theme.text + "80" }]}>
              {new Date(alert.timestamp).toLocaleString()}
            </Text>
          )}
        </View>

        {onDismiss && (
          <TouchableOpacity
            style={styles.dismissButton}
            onPress={handleDismiss}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <Icon name="close" size={20} color={theme.text + "99"} />
          </TouchableOpacity>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 16,
    marginVertical: 8,
    borderRadius: 12,
    borderLeftWidth: 4,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  content: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  textContainer: {
    flex: 1,
    marginRight: 8,
  },
  title: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 4,
  },
  message: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 4,
  },
  timestamp: {
    fontSize: 12,
    marginTop: 4,
  },
  dismissButton: {
    padding: 4,
  },
});

export default AlertItem;
