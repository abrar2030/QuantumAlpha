import React, { useState, forwardRef } from "react";
import {
  View,
  TextInput,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInputProps,
  ViewStyle,
} from "react-native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useTheme } from "../../context/ThemeContext";

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: string;
  rightIcon?: string;
  onRightIconPress?: () => void;
  variant?: "outlined" | "filled" | "underlined";
  size?: "small" | "medium" | "large";
  containerStyle?: ViewStyle;
  required?: boolean;
}

const Input = forwardRef<TextInput, InputProps>(
  (
    {
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      onRightIconPress,
      variant = "outlined",
      size = "medium",
      containerStyle,
      required = false,
      style,
      ...props
    },
    ref,
  ) => {
    const { theme } = useTheme();
    const [isFocused, setIsFocused] = useState(false);

    const getContainerStyle = () => {
      const baseStyle = {
        ...styles.container,
        ...styles[size],
      };

      switch (variant) {
        case "outlined":
          return {
            ...baseStyle,
            ...styles.outlined,
            borderColor: error
              ? theme.error
              : isFocused
                ? theme.primary
                : theme.border,
            backgroundColor: theme.card,
          };
        case "filled":
          return {
            ...baseStyle,
            ...styles.filled,
            backgroundColor: theme.background,
            borderBottomColor: error
              ? theme.error
              : isFocused
                ? theme.primary
                : theme.border,
          };
        case "underlined":
          return {
            ...baseStyle,
            ...styles.underlined,
            borderBottomColor: error
              ? theme.error
              : isFocused
                ? theme.primary
                : theme.border,
          };
        default:
          return baseStyle;
      }
    };

    const getInputStyle = () => {
      return {
        ...styles.input,
        color: theme.text,
        fontSize: size === "small" ? 14 : size === "large" ? 18 : 16,
      };
    };

    return (
      <View style={[containerStyle]}>
        {label && (
          <Text style={[styles.label, { color: theme.text }]}>
            {label}
            {required && <Text style={{ color: theme.error }}> *</Text>}
          </Text>
        )}

        <View style={getContainerStyle()}>
          {leftIcon && (
            <Icon
              name={leftIcon}
              size={20}
              color={theme.text}
              style={styles.leftIcon}
            />
          )}

          <TextInput
            ref={ref}
            style={[getInputStyle(), style]}
            placeholderTextColor={theme.text + "80"}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            {...props}
          />

          {rightIcon && (
            <TouchableOpacity
              onPress={onRightIconPress}
              style={styles.rightIcon}
            >
              <Icon name={rightIcon} size={20} color={theme.text} />
            </TouchableOpacity>
          )}
        </View>

        {(error || helperText) && (
          <Text
            style={[
              styles.helperText,
              { color: error ? theme.error : theme.text + "80" },
            ]}
          >
            {error || helperText}
          </Text>
        )}
      </View>
    );
  },
);

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 8,
    paddingHorizontal: 12,
  },
  small: {
    minHeight: 36,
    paddingHorizontal: 8,
  },
  medium: {
    minHeight: 44,
    paddingHorizontal: 12,
  },
  large: {
    minHeight: 52,
    paddingHorizontal: 16,
  },
  outlined: {
    borderWidth: 1,
  },
  filled: {
    borderBottomWidth: 2,
  },
  underlined: {
    borderBottomWidth: 1,
    borderRadius: 0,
    paddingHorizontal: 0,
  },
  input: {
    flex: 1,
    fontSize: 16,
    paddingVertical: 0,
  },
  label: {
    fontSize: 14,
    fontWeight: "500",
    marginBottom: 8,
  },
  helperText: {
    fontSize: 12,
    marginTop: 4,
    marginLeft: 4,
  },
  leftIcon: {
    marginRight: 8,
  },
  rightIcon: {
    marginLeft: 8,
    padding: 4,
  },
});

Input.displayName = "Input";

export default Input;
