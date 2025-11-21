import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { useTheme } from "../../context/ThemeContext";

const HelpScreen = () => {
  const { theme } = useTheme();

  const helpSections = [
    {
      title: "Getting Started",
      icon: "rocket-launch",
      items: [
        {
          title: "Account Setup",
          description: "Learn how to set up your account and profile",
        },
        {
          title: "Dashboard Overview",
          description: "Understanding your portfolio dashboard",
        },
        { title: "First Trade", description: "How to place your first trade" },
      ],
    },
    {
      title: "Trading",
      icon: "chart-line",
      items: [
        { title: "Market Orders", description: "How to place market orders" },
        { title: "Limit Orders", description: "How to place limit orders" },
        {
          title: "Order Types",
          description: "Understanding different order types",
        },
      ],
    },
    {
      title: "Strategies",
      icon: "strategy",
      items: [
        {
          title: "Strategy Overview",
          description: "Understanding algorithmic trading strategies",
        },
        {
          title: "Strategy Allocation",
          description: "How to allocate capital to strategies",
        },
        {
          title: "Strategy Performance",
          description: "How to monitor strategy performance",
        },
      ],
    },
    {
      title: "Security",
      icon: "shield-check",
      items: [
        {
          title: "Two-Factor Authentication",
          description: "Setting up 2FA for your account",
        },
        {
          title: "Password Security",
          description: "Best practices for password security",
        },
        {
          title: "Device Management",
          description: "Managing devices with access to your account",
        },
      ],
    },
  ];

  const renderHelpSection = (section, index) => {
    return (
      <View
        key={index}
        style={[styles.sectionContainer, { backgroundColor: theme.card }]}
      >
        <View style={styles.sectionHeader}>
          <Icon name={section.icon} size={24} color={theme.primary} />
          <Text style={[styles.sectionTitle, { color: theme.text }]}>
            {section.title}
          </Text>
        </View>

        {section.items.map((item, itemIndex) => (
          <TouchableOpacity
            key={itemIndex}
            style={[
              styles.helpItem,
              itemIndex < section.items.length - 1 && {
                borderBottomWidth: 1,
                borderBottomColor: theme.border,
              },
            ]}
            onPress={() => {
              // In a real app, this would navigate to a detailed help screen
              alert(`Would navigate to ${item.title} help screen`);
            }}
          >
            <View style={styles.helpItemContent}>
              <Text style={[styles.helpItemTitle, { color: theme.text }]}>
                {item.title}
              </Text>
              <Text
                style={[
                  styles.helpItemDescription,
                  { color: theme.text + "CC" },
                ]}
              >
                {item.description}
              </Text>
            </View>
            <Icon name="chevron-right" size={20} color={theme.text + "99"} />
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <View style={[styles.header, { backgroundColor: theme.card }]}>
        <Text style={[styles.headerTitle, { color: theme.text }]}>
          Help & Support
        </Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={[styles.searchContainer, { backgroundColor: theme.card }]}>
          <TouchableOpacity
            style={[styles.searchButton, { backgroundColor: theme.background }]}
            onPress={() => {
              // In a real app, this would open a search screen
              alert("Would open help search");
            }}
          >
            <Icon name="magnify" size={20} color={theme.text + "99"} />
            <Text style={[styles.searchText, { color: theme.text + "99" }]}>
              Search help articles...
            </Text>
          </TouchableOpacity>
        </View>

        <View
          style={[styles.contactContainer, { backgroundColor: theme.card }]}
        >
          <Text style={[styles.contactTitle, { color: theme.text }]}>
            Need assistance?
          </Text>

          <View style={styles.contactButtons}>
            <TouchableOpacity
              style={[
                styles.contactButton,
                { backgroundColor: theme.primary + "20" },
              ]}
              onPress={() => {
                // In a real app, this would open chat support
                alert("Would open chat support");
              }}
            >
              <Icon name="chat" size={24} color={theme.primary} />
              <Text style={[styles.contactButtonText, { color: theme.text }]}>
                Chat Support
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.contactButton,
                { backgroundColor: theme.info + "20" },
              ]}
              onPress={() => {
                // In a real app, this would open email support
                alert("Would open email support");
              }}
            >
              <Icon name="email" size={24} color={theme.info} />
              <Text style={[styles.contactButtonText, { color: theme.text }]}>
                Email Support
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {helpSections.map(renderHelpSection)}

        <View style={styles.footer}>
          <Text style={[styles.footerText, { color: theme.text + "99" }]}>
            QuantumAlpha v1.0.0
          </Text>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: "bold",
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  searchContainer: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  searchButton: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 8,
    paddingHorizontal: 12,
    height: 40,
  },
  searchText: {
    marginLeft: 8,
    fontSize: 16,
  },
  contactContainer: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  contactTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 12,
  },
  contactButtons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  contactButton: {
    width: "48%",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
  },
  contactButtonText: {
    fontSize: 14,
    fontWeight: "500",
    marginTop: 8,
  },
  sectionContainer: {
    borderRadius: 12,
    marginBottom: 16,
    overflow: "hidden",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginLeft: 12,
  },
  helpItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
  },
  helpItemContent: {
    flex: 1,
    marginRight: 16,
  },
  helpItemTitle: {
    fontSize: 16,
    marginBottom: 4,
  },
  helpItemDescription: {
    fontSize: 14,
  },
  footer: {
    alignItems: "center",
    marginTop: 20,
    marginBottom: 10,
  },
  footerText: {
    fontSize: 14,
  },
});

export default HelpScreen;
