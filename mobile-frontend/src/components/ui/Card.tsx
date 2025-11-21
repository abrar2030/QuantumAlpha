import React from "react";
import { View, StyleSheet, TouchableOpacity, ViewStyle } from "react-native";
import * as Animatable from "react-native-animatable";
import { useTheme } from "../../context/ThemeContext";

interface CardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  onPress?: () => void;
  variant?: "default" | "elevated" | "outlined" | "filled";
  padding?: "none" | "small" | "medium" | "large";
  margin?: "none" | "small" | "medium" | "large";
  animated?: boolean;
  animationType?: "fadeIn" | "slideInUp" | "slideInDown" | "zoomIn";
  animationDelay?: number;
}

const Card: React.FC<CardProps> = ({
  children,
  style,
  onPress,
  variant = "default",
  padding = "medium",
  margin = "none",
  animated = false,
  animationType = "fadeIn",
  animationDelay = 0,
}) => {
  const { theme, isDarkMode } = useTheme();

  const getCardStyle = () => {
    const baseStyle = {
      ...styles.card,
      backgroundColor: theme.card,
    };

    switch (variant) {
      case "elevated":
        return {
          ...baseStyle,
          ...styles.elevated,
          shadowColor: isDarkMode ? "#000" : "#000",
        };
      case "outlined":
        return {
          ...baseStyle,
          ...styles.outlined,
          borderColor: theme.border,
        };
      case "filled":
        return {
          ...baseStyle,
          backgroundColor: theme.background,
        };
      default:
        return baseStyle;
    }
  };

  const getPaddingStyle = () => {
    switch (padding) {
      case "none":
        return {};
      case "small":
        return styles.paddingSmall;
      case "medium":
        return styles.paddingMedium;
      case "large":
        return styles.paddingLarge;
      default:
        return styles.paddingMedium;
    }
  };

  const getMarginStyle = () => {
    switch (margin) {
      case "none":
        return {};
      case "small":
        return styles.marginSmall;
      case "medium":
        return styles.marginMedium;
      case "large":
        return styles.marginLarge;
      default:
        return {};
    }
  };

  const cardStyle = [
    getCardStyle(),
    getPaddingStyle(),
    getMarginStyle(),
    style,
  ];

  const CardComponent = onPress ? TouchableOpacity : View;

  const cardContent = (
    <CardComponent
      style={cardStyle}
      onPress={onPress}
      activeOpacity={onPress ? 0.8 : 1}
    >
      {children}
    </CardComponent>
  );

  if (animated) {
    return (
      <Animatable.View
        animation={animationType}
        delay={animationDelay}
        duration={600}
        useNativeDriver
      >
        {cardContent}
      </Animatable.View>
    );
  }

  return cardContent;
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    overflow: "hidden",
  },
  elevated: {
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  outlined: {
    borderWidth: 1,
  },
  paddingSmall: {
    padding: 8,
  },
  paddingMedium: {
    padding: 16,
  },
  paddingLarge: {
    padding: 24,
  },
  marginSmall: {
    margin: 8,
  },
  marginMedium: {
    margin: 16,
  },
  marginLarge: {
    margin: 24,
  },
});

export default Card;
