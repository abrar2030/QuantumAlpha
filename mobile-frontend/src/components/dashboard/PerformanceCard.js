import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { useTheme } from "../../context/ThemeContext";

const PerformanceCard = ({ title, value, change, period }) => {
  const { theme } = useTheme();

  return (
    <View style={[styles.container, { backgroundColor: theme.card }]}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.text }]}>{title}</Text>
        <TouchableOpacity>
          <Text style={[styles.periodText, { color: theme.primary }]}>
            {period}
          </Text>
        </TouchableOpacity>
      </View>

      <Text style={[styles.value, { color: theme.text }]}>{value}</Text>

      <View style={styles.changeContainer}>
        <Text
          style={[
            styles.changeText,
            { color: change >= 0 ? theme.success : theme.error },
          ]}
        >
          {change >= 0 ? "+" : ""}
          {change}%
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    padding: 16,
    marginRight: 12,
    width: 180,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  title: {
    fontSize: 14,
  },
  periodText: {
    fontSize: 12,
    fontWeight: "500",
  },
  value: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 8,
  },
  changeContainer: {
    flexDirection: "row",
    alignItems: "center",
  },
  changeText: {
    fontSize: 16,
    fontWeight: "500",
  },
});

export default PerformanceCard;
