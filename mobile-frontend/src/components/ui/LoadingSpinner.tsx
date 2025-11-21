import React from "react";
import { View, ActivityIndicator, StyleSheet, ViewStyle } from "react-native";
import SkeletonPlaceholder from "react-native-skeleton-placeholder";
import { useTheme } from "../../context/ThemeContext";

interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
  color?: string;
  style?: ViewStyle;
}

interface SkeletonLoaderProps {
  type: "card" | "list" | "chart" | "profile" | "custom";
  count?: number;
  style?: ViewStyle;
  children?: React.ReactNode;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "medium",
  color,
  style,
}) => {
  const { theme } = useTheme();

  const getSize = () => {
    switch (size) {
      case "small":
        return 20;
      case "large":
        return 40;
      default:
        return 30;
    }
  };

  return (
    <View style={[styles.container, style]}>
      <ActivityIndicator size={getSize()} color={color || theme.primary} />
    </View>
  );
};

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  type,
  count = 1,
  style,
  children,
}) => {
  const { theme, isDarkMode } = useTheme();

  const renderSkeleton = () => {
    const items = [];

    for (let i = 0; i < count; i++) {
      switch (type) {
        case "card":
          items.push(
            <View key={i} style={styles.skeletonCard}>
              <SkeletonPlaceholder.Item
                width="100%"
                height={120}
                borderRadius={8}
              />
              <SkeletonPlaceholder.Item marginTop={12}>
                <SkeletonPlaceholder.Item width="80%" height={16} />
                <SkeletonPlaceholder.Item
                  marginTop={8}
                  width="60%"
                  height={14}
                />
              </SkeletonPlaceholder.Item>
            </View>,
          );
          break;

        case "list":
          items.push(
            <View key={i} style={styles.skeletonListItem}>
              <SkeletonPlaceholder.Item
                width={50}
                height={50}
                borderRadius={25}
                marginRight={12}
              />
              <SkeletonPlaceholder.Item flex={1}>
                <SkeletonPlaceholder.Item width="70%" height={16} />
                <SkeletonPlaceholder.Item
                  marginTop={8}
                  width="50%"
                  height={14}
                />
              </SkeletonPlaceholder.Item>
            </View>,
          );
          break;

        case "chart":
          items.push(
            <View key={i} style={styles.skeletonChart}>
              <SkeletonPlaceholder.Item
                width="100%"
                height={200}
                borderRadius={8}
              />
              <SkeletonPlaceholder.Item marginTop={12}>
                <SkeletonPlaceholder.Item width="40%" height={14} />
                <SkeletonPlaceholder.Item
                  marginTop={8}
                  width="60%"
                  height={12}
                />
              </SkeletonPlaceholder.Item>
            </View>,
          );
          break;

        case "profile":
          items.push(
            <View key={i} style={styles.skeletonProfile}>
              <SkeletonPlaceholder.Item
                width={80}
                height={80}
                borderRadius={40}
                alignSelf="center"
              />
              <SkeletonPlaceholder.Item marginTop={16} alignItems="center">
                <SkeletonPlaceholder.Item width="60%" height={18} />
                <SkeletonPlaceholder.Item
                  marginTop={8}
                  width="40%"
                  height={14}
                />
              </SkeletonPlaceholder.Item>
            </View>,
          );
          break;

        default:
          items.push(children);
      }
    }

    return items;
  };

  return (
    <SkeletonPlaceholder
      backgroundColor={isDarkMode ? "#2a2a2a" : "#f0f0f0"}
      highlightColor={isDarkMode ? "#3a3a3a" : "#ffffff"}
      speed={1200}
    >
      <View style={style}>{renderSkeleton()}</View>
    </SkeletonPlaceholder>
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  skeletonCard: {
    marginBottom: 16,
    padding: 16,
  },
  skeletonListItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
    paddingHorizontal: 16,
  },
  skeletonChart: {
    marginBottom: 16,
    padding: 16,
  },
  skeletonProfile: {
    padding: 20,
  },
});

export default LoadingSpinner;
