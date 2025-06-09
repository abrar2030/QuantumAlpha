import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  ScrollView,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';

import { useTheme } from '../../context/ThemeContext';
import { useAlert } from '../../context/AlertContext';
import { portfolioService } from '../../services/portfolioService';
import { strategyService } from '../../services/strategyService';
import { alertService } from '../../services/alertService';
import { authenticateWithBiometrics } from '../../auth/BiometricAuth';
import { retrieveDataSecurely } from '../../auth/SecureStorage';
import { registerForPushNotifications, sendPushNotification } from '../../services/PushNotificationService';

import PerformanceCard from '../../components/dashboard/PerformanceCard';
import StrategyCard from '../../components/dashboard/StrategyCard';
import AlertItem from '../../components/alerts/AlertItem';
import MarketOverview from '../../components/dashboard/MarketOverview';

const DashboardScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  const { addAlert } = useAlert();
  
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [portfolioData, setPortfolioData] = useState({
    value: 0,
    dailyChange: 0,
    percentChange: 0,
  });
  const [performanceData, setPerformanceData] = useState({
    labels: [],
    datasets: [{ data: [] }],
  });
  const [strategies, setStrategies] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  
  const screenWidth = Dimensions.get('window').width;
  
  useEffect(() => {
    const initApp = async () => {
      // Biometric authentication on app launch/dashboard load
      const authenticated = await authenticateWithBiometrics();
      if (!authenticated) {
        // Handle authentication failure (e.g., navigate to login, show error)
        console.log("Biometric authentication failed or cancelled.");
      }

      // Simulate retrieving a securely stored token
      const userToken = await retrieveDataSecurely("userToken");
      console.log("Retrieved user token:", userToken);

      // Register for push notifications
      const deviceToken = await registerForPushNotifications();
      console.log("Device token for push notifications:", deviceToken);

      loadDashboardData();
    };
    initApp();

    // Set up alert listener for real-time updates
    const alertListener = alertService.subscribeToAlerts((newAlert) => {
      addAlert(newAlert);
      setRecentAlerts((prev) => [newAlert, ...prev].slice(0, 5));
      // Send a push notification when a new alert is received
      sendPushNotification(deviceToken, "New Alert!", newAlert.message);
    });

    return () => {
      alertListener.unsubscribe();
    };
  }, []);
  
  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // In a real app, these would be API calls to the backend services
      const portfolioResponse = await portfolioService.getPortfolioSummary();
      const performanceResponse = await portfolioService.getPerformanceHistory();
      const strategiesResponse = await strategyService.getActiveStrategies();
      const alertsResponse = await alertService.getRecentAlerts(5);
      
      setPortfolioData({
        value: portfolioResponse.totalValue,
        dailyChange: portfolioResponse.dailyChange,
        percentChange: portfolioResponse.percentChange,
      });
      
      setPerformanceData({
        labels: performanceResponse.labels,
        datasets: [{ data: performanceResponse.values }],
      });
      
      setStrategies(strategiesResponse);
      setRecentAlerts(alertsResponse);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  const onRefresh = () => {
    setRefreshing(true);
    loadDashboardData();
  };
  
  const navigateToStrategy = (strategy) => {
    navigation.navigate('StrategyDetail', { 
      id: strategy.id,
      name: strategy.name 
    });
  };
  
  const navigateToAlerts = () => {
    navigation.navigate('AlertsTab');
  };
  
  const navigateToNotifications = () => {
    navigation.navigate('Notifications');
  };
  
  if (loading && !refreshing) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: theme.background }]}>
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading dashboard...
        </Text>
      </View>
    );
  }
  
  return (
    <SafeAreaView style={[styles.container, { backgroundColor: theme.background }]}>
      <View style={[styles.header, { backgroundColor: theme.card }]}>
        <View style={styles.headerContent}>
          <Text style={[styles.title, { color: theme.text }]}>QuantumAlpha</Text>
          <View style={styles.headerIcons}>
            <TouchableOpacity 
              style={styles.iconButton}
              onPress={navigateToNotifications}
            >
              <Icon name="bell" size={24} color={theme.text} />
              {recentAlerts.length > 0 && (
                <View style={[styles.badge, { backgroundColor: theme.notification }]}>
                  <Text style={styles.badgeText}>
                    {recentAlerts.length > 9 ? '9+' : recentAlerts.length}
                  </Text>
                </View>
              )}
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.iconButton}
              onPress={() => navigation.openDrawer()}
            >
              <Icon name="menu" size={24} color={theme.text} />
            </TouchableOpacity>
          </View>
        </View>
        <Text style={[styles.subtitle, { color: theme.text }]}>Portfolio Dashboard</Text>
      </View>
      
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={theme.primary}
            colors={[theme.primary]}
          />
        }
      >
        <View style={[styles.portfolioSummary, { backgroundColor: theme.card }]}>
          <Text style={[styles.portfolioValue, { color: theme.text }]}>
            ${portfolioData.value.toLocaleString()}
          </Text>
          <View style={styles.changeContainer}>
            <Text
              style={[
                portfolioData.dailyChange >= 0
                  ? [styles.positiveChange, { color: theme.success }]
                  : [styles.negativeChange, { color: theme.error }],
              ]}
            >
              {portfolioData.dailyChange >= 0 ? '+' : ''}
              {portfolioData.dailyChange.toLocaleString()} (
              {portfolioData.percentChange}%)
            </Text>
          </View>
        </View>
        
        <View style={styles.chartContainer}>
          <Text style={[styles.sectionTitle, { color: theme.text }]}>Performance</Text>
          <LineChart
            data={performanceData}
            width={screenWidth - 40}
            height={220}
            chartConfig={{
              backgroundColor: theme.chartBackground,
              backgroundGradientFrom: theme.chartBackgroundGradientFrom,
              backgroundGradientTo: theme.chartBackgroundGradientTo,
              decimalPlaces: 0,
              color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(${theme.isDarkMode ? '255, 255, 255' : '0, 0, 0'}, ${opacity})`,
              style: {
                borderRadius: 16,
              },
              propsForDots: {
                r: '6',
                strokeWidth: '2',
                stroke: theme.primary,
              },
            }}
            bezier
            style={styles.chart}
          />
        </View>
        
        <MarketOverview />
        
        <View style={styles.strategiesContainer}>
          <View style={styles.sectionHeader}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Active Strategies
            </Text>
            <TouchableOpacity onPress={() => navigation.navigate('StrategyTab')}>
              <Text style={[styles.seeAllText, { color: theme.primary }]}>
                See All
              </Text>
            </TouchableOpacity>
          </View>
          
          {strategies.map((strategy) => (
            <StrategyCard
              key={strategy.id}
              strategy={strategy}
              onPress={() => navigateToStrategy(strategy)}
            />
          ))}
        </View>
        
        <View style={styles.alertsContainer}>
          <View style={styles.sectionHeader}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Recent Alerts
            </Text>
            <TouchableOpacity onPress={navigateToAlerts}>
              <Text style={[styles.seeAllText, { color: theme.primary }]}>
                See All
              </Text>
            </TouchableOpacity>
          </View>
          
          {recentAlerts.length > 0 ? (
            recentAlerts.map((alert) => (
              <AlertItem key={alert.id} alert={alert} />
            ))
          ) : (
            <View style={[styles.emptyState, { backgroundColor: theme.card }]}>
              <Icon name="bell-off" size={40} color={theme.text} />
              <Text style={[styles.emptyStateText, { color: theme.text }]}>
                No recent alerts
              </Text>
            </View>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
  },
  header: {
    padding: 16,
    paddingTop: 0,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 16,
    marginTop: 4,
    opacity: 0.7,
  },
  headerIcons: {
    flexDirection: 'row',
  },
  iconButton: {
    padding: 8,
    marginLeft: 8,
    position: 'relative',
  },
  badge: {
    position: 'absolute',
    right: 0,
    top: 0,
    minWidth: 18,
    height: 18,
    borderRadius: 9,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badgeText: {
    color: '#ffffff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  scrollContent: {
    paddingBottom: 30,
  },
  portfolioSummary: {
    padding: 20,
    borderRadius: 10,
    marginHorizontal: 20,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  portfolioValue: {
    fontSize: 32,
    fontWeight: 'bold',
  },
  changeContainer: {
    marginTop: 10,
  },
  positiveChange: {
    fontSize: 18,
  },
  negativeChange: {
    fontSize: 18,
  },
  chartContainer: {
    marginTop: 20,
    padding: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  seeAllText: {
    fontSize: 14,
    fontWeight: '600',
  },
  chart: {
    borderRadius: 16,
    marginTop: 10,
  },
  strategiesContainer: {
    marginTop: 10,
    padding: 20,
  },
  alertsContainer: {
    marginTop: 10,
    padding: 20,
    paddingBottom: 40,
  },
  emptyState: {
    padding: 30,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyStateText: {
    marginTop: 10,
    fontSize: 16,
  },
});

export default DashboardScreen;
