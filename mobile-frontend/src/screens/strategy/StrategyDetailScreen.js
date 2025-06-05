import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Dimensions,
  Animated,
} from 'react-native';
import { useRoute, useNavigation } from '@react-navigation/native';
import { LineChart, PieChart } from 'react-native-chart-kit';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';
import { strategyService } from '../../services/strategyService';

const StrategyDetailScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { theme } = useTheme();
  const { id, name } = route.params;
  
  const [loading, setLoading] = useState(true);
  const [strategy, setStrategy] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  
  // Animation values
  const fadeAnim = new Animated.Value(0);
  const translateY = new Animated.Value(50);
  
  useEffect(() => {
    loadStrategyDetails();
    
    // Set navigation options dynamically
    navigation.setOptions({
      title: name || 'Strategy Details',
      headerRight: () => (
        <TouchableOpacity
          style={{ marginRight: 16 }}
          onPress={() => {
            // In a real app, this would open a menu with options
            alert('Strategy options');
          }}
        >
          <Icon name="dots-vertical" size={24} color={theme.text} />
        </TouchableOpacity>
      ),
    });
  }, []);
  
  useEffect(() => {
    if (!loading) {
      // Start animations when data is loaded
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
    }
  }, [loading]);
  
  const loadStrategyDetails = async () => {
    try {
      setLoading(true);
      const data = await strategyService.getStrategyDetails(id);
      setStrategy(data);
    } catch (error) {
      console.error('Error loading strategy details:', error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
    }
  };
  
  const toggleStrategyStatus = async () => {
    try {
      const newStatus = strategy.status === 'Active' ? false : true;
      await strategyService.toggleStrategyStatus(id, newStatus);
      
      // Update local state
      setStrategy({
        ...strategy,
        status: newStatus ? 'Active' : 'Inactive',
      });
    } catch (error) {
      console.error('Error toggling strategy status:', error);
      // In a real app, you would handle errors appropriately
    }
  };
  
  const updateAllocation = async (newAllocation) => {
    try {
      await strategyService.updateStrategyAllocation(id, newAllocation);
      
      // Update local state
      setStrategy({
        ...strategy,
        allocation: newAllocation,
      });
    } catch (error) {
      console.error('Error updating allocation:', error);
      // In a real app, you would handle errors appropriately
    }
  };
  
  if (loading) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: theme.background }]}>
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading strategy details...
        </Text>
      </View>
    );
  }
  
  if (!strategy) {
    return (
      <View style={[styles.errorContainer, { backgroundColor: theme.background }]}>
        <Icon name="alert-circle" size={60} color={theme.error} />
        <Text style={[styles.errorText, { color: theme.text }]}>
          Strategy not found
        </Text>
        <TouchableOpacity
          style={[styles.backButton, { backgroundColor: theme.primary }]}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  const screenWidth = Dimensions.get('window').width;
  
  const renderOverviewTab = () => {
    return (
      <View style={styles.tabContent}>
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>Performance</Text>
          <View style={styles.performanceSummary}>
            <View style={styles.performanceItem}>
              <Text style={[styles.performanceValue, { color: theme.text }]}>
                {strategy.totalReturn}%
              </Text>
              <Text style={[styles.performanceLabel, { color: theme.text + 'CC' }]}>
                Total Return
              </Text>
            </View>
            <View style={styles.performanceItem}>
              <Text style={[styles.performanceValue, { color: theme.text }]}>
                {strategy.sharpeRatio}
              </Text>
              <Text style={[styles.performanceLabel, { color: theme.text + 'CC' }]}>
                Sharpe Ratio
              </Text>
            </View>
            <View style={styles.performanceItem}>
              <Text style={[styles.performanceValue, { color: theme.text }]}>
                {strategy.maxDrawdown}%
              </Text>
              <Text style={[styles.performanceLabel, { color: theme.text + 'CC' }]}>
                Max Drawdown
              </Text>
            </View>
          </View>
          
          <LineChart
            data={{
              labels: strategy.performanceHistory.labels,
              datasets: [
                {
                  data: strategy.performanceHistory.values,
                },
              ],
            }}
            width={screenWidth - 40}
            height={220}
            chartConfig={{
              backgroundColor: theme.chartBackground,
              backgroundGradientFrom: theme.chartBackgroundGradientFrom,
              backgroundGradientTo: theme.chartBackgroundGradientTo,
              decimalPlaces: 1,
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
        
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>Strategy Details</Text>
          <Text style={[styles.description, { color: theme.text }]}>
            {strategy.description}
          </Text>
          
          <View style={styles.detailsGrid}>
            <View style={styles.detailItem}>
              <Icon name="calendar" size={20} color={theme.text + 'CC'} />
              <View style={styles.detailTextContainer}>
                <Text style={[styles.detailLabel, { color: theme.text + 'CC' }]}>
                  Inception
                </Text>
                <Text style={[styles.detailValue, { color: theme.text }]}>
                  {new Date(strategy.inception).toLocaleDateString()}
                </Text>
              </View>
            </View>
            
            <View style={styles.detailItem}>
              <Icon name="shield-outline" size={20} color={theme.text + 'CC'} />
              <View style={styles.detailTextContainer}>
                <Text style={[styles.detailLabel, { color: theme.text + 'CC' }]}>
                  Risk Level
                </Text>
                <Text style={[styles.detailValue, { color: theme.text }]}>
                  {strategy.risk}
                </Text>
              </View>
            </View>
            
            <View style={styles.detailItem}>
              <Icon name="chart-line" size={20} color={theme.text + 'CC'} />
              <View style={styles.detailTextContainer}>
                <Text style={[styles.detailLabel, { color: theme.text + 'CC' }]}>
                  Win Rate
                </Text>
                <Text style={[styles.detailValue, { color: theme.text }]}>
                  {strategy.winRate}%
                </Text>
              </View>
            </View>
            
            <View style={styles.detailItem}>
              <Icon name="chart-pie" size={20} color={theme.text + 'CC'} />
              <View style={styles.detailTextContainer}>
                <Text style={[styles.detailLabel, { color: theme.text + 'CC' }]}>
                  Allocation
                </Text>
                <Text style={[styles.detailValue, { color: theme.text }]}>
                  {strategy.allocation}%
                </Text>
              </View>
            </View>
          </View>
        </View>
        
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>Holdings</Text>
          
          <View style={styles.holdingsContainer}>
            {strategy.holdings.map((holding, index) => (
              <View
                key={index}
                style={[
                  styles.holdingItem,
                  index < strategy.holdings.length - 1 && {
                    borderBottomWidth: 1,
                    borderBottomColor: theme.border,
                  },
                ]}
              >
                <View style={styles.holdingMain}>
                  <Text style={[styles.holdingSymbol, { color: theme.text }]}>
                    {holding.symbol}
                  </Text>
                  <Text
                    style={[
                      styles.holdingPerformance,
                      {
                        color:
                          holding.performance >= 0 ? theme.success : theme.error,
                      },
                    ]}
                  >
                    {holding.performance >= 0 ? '+' : ''}
                    {holding.performance}%
                  </Text>
                </View>
                <View style={styles.holdingAllocationContainer}>
                  <View
                    style={[
                      styles.holdingAllocationBar,
                      { backgroundColor: theme.border },
                    ]}
                  >
                    <View
                      style={[
                        styles.holdingAllocationFill,
                        {
                          backgroundColor: theme.primary,
                          width: `${holding.allocation}%`,
                        },
                      ]}
                    />
                  </View>
                  <Text
                    style={[styles.holdingAllocationText, { color: theme.text + 'CC' }]}
                  >
                    {holding.allocation}%
                  </Text>
                </View>
              </View>
            ))}
          </View>
        </View>
      </View>
    );
  };
  
  const renderParametersTab = () => {
    return (
      <View style={styles.tabContent}>
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Strategy Parameters
          </Text>
          <Text style={[styles.paramDescription, { color: theme.text + 'CC' }]}>
            These parameters define how the strategy operates and makes trading decisions.
          </Text>
          
          {strategy.parameters.map((param, index) => (
            <View
              key={index}
              style={[
                styles.parameterItem,
                index < strategy.parameters.length - 1 && {
                  borderBottomWidth: 1,
                  borderBottomColor: theme.border,
                },
              ]}
            >
              <Text style={[styles.parameterName, { color: theme.text }]}>
                {param.name}
              </Text>
              <Text style={[styles.parameterValue, { color: theme.primary }]}>
                {param.value}
              </Text>
            </View>
          ))}
        </View>
        
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Allocation Control
          </Text>
          <Text style={[styles.paramDescription, { color: theme.text + 'CC' }]}>
            Adjust the capital allocation for this strategy.
          </Text>
          
          <View style={styles.allocationControl}>
            <Text style={[styles.allocationValue, { color: theme.text }]}>
              {strategy.allocation}%
            </Text>
            <View style={styles.allocationButtons}>
              <TouchableOpacity
                style={[
                  styles.allocationButton,
                  { backgroundColor: theme.card, borderColor: theme.border },
                ]}
                onPress={() => {
                  if (strategy.allocation > 5) {
                    updateAllocation(strategy.allocation - 5);
                  }
                }}
              >
                <Icon name="minus" size={20} color={theme.text} />
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.allocationButton,
                  { backgroundColor: theme.card, borderColor: theme.border },
                ]}
                onPress={() => {
                  if (strategy.allocation < 100) {
                    updateAllocation(strategy.allocation + 5);
                  }
                }}
              >
                <Icon name="plus" size={20} color={theme.text} />
              </TouchableOpacity>
            </View>
          </View>
          
          <View style={styles.allocationBarContainer}>
            <View
              style={[styles.allocationBar, { backgroundColor: theme.border }]}
            >
              <View
                style={[
                  styles.allocationFill,
                  { backgroundColor: theme.primary, width: `${strategy.allocation}%` },
                ]}
              />
            </View>
            <View style={styles.allocationLabels}>
              <Text style={[styles.allocationLabel, { color: theme.text + 'CC' }]}>
                0%
              </Text>
              <Text style={[styles.allocationLabel, { color: theme.text + 'CC' }]}>
                50%
              </Text>
              <Text style={[styles.allocationLabel, { color: theme.text + 'CC' }]}>
                100%
              </Text>
            </View>
          </View>
        </View>
        
        <View style={[styles.card, { backgroundColor: theme.card }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Strategy Controls
          </Text>
          
          <View style={styles.controlButtons}>
            <TouchableOpacity
              style={[
                styles.controlButton,
                {
                  backgroundColor:
                    strategy.status === 'Active' ? theme.error : theme.success,
                },
              ]}
              onPress={toggleStrategyStatus}
            >
              <Icon
                name={strategy.status === 'Active' ? 'pause' : 'play'}
                size={20}
                color="#FFFFFF"
              />
              <Text style={styles.controlButtonText}>
                {strategy.status === 'Active' ? 'Pause Strategy' : 'Activate Strategy'}
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.controlButton, { backgroundColor: theme.info }]}
              onPress={() => {
                // In a real app, this would navigate to a backtest screen
                alert('Would navigate to backtest screen');
              }}
            >
              <Icon name="test-tube" size={20} color="#FFFFFF" />
              <Text style={styles.controlButtonText}>Run Backtest</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.controlButton, { backgroundColor: theme.warning }]}
              onPress={() => {
                // In a real app, this would reset the strategy
                alert('Would reset strategy parameters');
              }}
            >
              <Icon name="refresh" size={20} color="#FFFFFF" />
              <Text style={styles.controlButtonText}>Reset Parameters</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    );
  };
  
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
        <View style={styles.statusContainer}>
          <View
            style={[
              styles.statusIndicator,
              {
                backgroundColor:
                  strategy.status === 'Active' ? theme.success : theme.error,
              },
            ]}
          />
          <Text style={[styles.statusText, { color: theme.text }]}>
            {strategy.status}
          </Text>
        </View>
        
        <Text style={[styles.strategyName, { color: theme.text }]}>
          {strategy.name}
        </Text>
        
        <View style={styles.performanceContainer}>
          <Text
            style={[
              styles.performanceText,
              {
                color: strategy.performance >= 0 ? theme.success : theme.error,
              },
            ]}
          >
            {strategy.performance >= 0 ? '+' : ''}
            {strategy.performance}%
          </Text>
          <Text style={[styles.performancePeriod, { color: theme.text + 'CC' }]}>
            Today
          </Text>
        </View>
      </Animated.View>
      
      <View style={[styles.tabs, { backgroundColor: theme.card }]}>
        <TouchableOpacity
          style={[
            styles.tab,
            activeTab === 'overview' && [
              styles.activeTab,
              { borderBottomColor: theme.primary },
            ],
          ]}
          onPress={() => setActiveTab('overview')}
        >
          <Text
            style={[
              styles.tabText,
              {
                color:
                  activeTab === 'overview' ? theme.primary : theme.text + 'CC',
              },
            ]}
          >
            Overview
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[
            styles.tab,
            activeTab === 'parameters' && [
              styles.activeTab,
              { borderBottomColor: theme.primary },
            ],
          ]}
          onPress={() => setActiveTab('parameters')}
        >
          <Text
            style={[
              styles.tabText,
              {
                color:
                  activeTab === 'parameters' ? theme.primary : theme.text + 'CC',
              },
            ]}
          >
            Parameters
          </Text>
        </TouchableOpacity>
      </View>
      
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {activeTab === 'overview' ? renderOverviewTab() : renderParametersTab()}
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
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    marginTop: 20,
    marginBottom: 20,
  },
  backButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  backButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  header: {
    padding: 20,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 14,
  },
  strategyName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 5,
  },
  performanceContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginTop: 5,
  },
  performanceText: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  performancePeriod: {
    fontSize: 14,
    marginLeft: 5,
  },
  tabs: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  tab: {
    flex: 1,
    paddingVertical: 15,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 2,
  },
  tabText: {
    fontSize: 16,
    fontWeight: '500',
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 30,
  },
  tabContent: {
    flex: 1,
  },
  card: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  performanceSummary: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  performanceItem: {
    alignItems: 'center',
  },
  performanceValue: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  performanceLabel: {
    fontSize: 12,
    marginTop: 5,
  },
  chart: {
    borderRadius: 16,
    marginTop: 10,
  },
  description: {
    fontSize: 14,
    lineHeight: 22,
    marginBottom: 20,
  },
  detailsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -8,
  },
  detailItem: {
    width: '50%',
    paddingHorizontal: 8,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  detailTextContainer: {
    marginLeft: 10,
  },
  detailLabel: {
    fontSize: 12,
  },
  detailValue: {
    fontSize: 16,
    fontWeight: '500',
    marginTop: 2,
  },
  holdingsContainer: {
    marginTop: 5,
  },
  holdingItem: {
    paddingVertical: 12,
  },
  holdingMain: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  holdingSymbol: {
    fontSize: 16,
    fontWeight: '500',
  },
  holdingPerformance: {
    fontSize: 14,
    fontWeight: '500',
  },
  holdingAllocationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  holdingAllocationBar: {
    flex: 1,
    height: 6,
    borderRadius: 3,
    marginRight: 10,
    overflow: 'hidden',
  },
  holdingAllocationFill: {
    height: '100%',
    borderRadius: 3,
  },
  holdingAllocationText: {
    fontSize: 12,
    width: 40,
    textAlign: 'right',
  },
  paramDescription: {
    fontSize: 14,
    marginBottom: 20,
  },
  parameterItem: {
    paddingVertical: 12,
  },
  parameterName: {
    fontSize: 16,
    marginBottom: 4,
  },
  parameterValue: {
    fontSize: 14,
    fontWeight: '500',
  },
  allocationControl: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  allocationValue: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  allocationButtons: {
    flexDirection: 'row',
  },
  allocationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 10,
  },
  allocationBarContainer: {
    marginBottom: 10,
  },
  allocationBar: {
    height: 8,
    borderRadius: 4,
    marginBottom: 5,
    overflow: 'hidden',
  },
  allocationFill: {
    height: '100%',
    borderRadius: 4,
  },
  allocationLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  allocationLabel: {
    fontSize: 12,
  },
  controlButtons: {
    marginTop: 10,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    borderRadius: 8,
    marginBottom: 10,
  },
  controlButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '500',
    marginLeft: 8,
  },
});

export default StrategyDetailScreen;
