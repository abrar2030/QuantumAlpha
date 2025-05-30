import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, SafeAreaView } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const screenWidth = Dimensions.get('window').width;

const DashboardScreen = () => {
  const [portfolioValue, setPortfolioValue] = useState(0);
  const [dailyChange, setDailyChange] = useState(0);
  const [percentChange, setPercentChange] = useState(0);
  const [chartData, setChartData] = useState({
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [
      {
        data: [10000, 10050, 10150, 10080, 10200, 10300, 10400],
        color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
        strokeWidth: 2
      }
    ]
  });
  
  useEffect(() => {
    // Simulating API fetch for portfolio data
    const fetchPortfolioData = async () => {
      // In a real app, this would be an API call
      setTimeout(() => {
        setPortfolioValue(10400);
        setDailyChange(100);
        setPercentChange(0.97);
      }, 1000);
    };
    
    fetchPortfolioData();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <Text style={styles.title}>QuantumAlpha</Text>
          <Text style={styles.subtitle}>Portfolio Dashboard</Text>
        </View>
        
        <View style={styles.portfolioSummary}>
          <Text style={styles.portfolioValue}>${portfolioValue.toLocaleString()}</Text>
          <View style={styles.changeContainer}>
            <Text style={dailyChange >= 0 ? styles.positiveChange : styles.negativeChange}>
              {dailyChange >= 0 ? '+' : ''}{dailyChange.toLocaleString()} ({percentChange}%)
            </Text>
          </View>
        </View>
        
        <View style={styles.chartContainer}>
          <Text style={styles.sectionTitle}>Performance</Text>
          <LineChart
            data={chartData}
            width={screenWidth - 40}
            height={220}
            chartConfig={{
              backgroundColor: '#1e1e1e',
              backgroundGradientFrom: '#1e1e1e',
              backgroundGradientTo: '#1e1e1e',
              decimalPlaces: 0,
              color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              style: {
                borderRadius: 16
              },
              propsForDots: {
                r: '6',
                strokeWidth: '2',
                stroke: '#1aff92'
              }
            }}
            bezier
            style={styles.chart}
          />
        </View>
        
        <View style={styles.strategiesContainer}>
          <Text style={styles.sectionTitle}>Active Strategies</Text>
          <TouchableOpacity style={styles.strategyCard}>
            <Text style={styles.strategyName}>Momentum Alpha</Text>
            <Text style={styles.strategyPerformance}>+2.3%</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.strategyCard}>
            <Text style={styles.strategyName}>Sentiment Trader</Text>
            <Text style={styles.strategyPerformance}>+1.5%</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.strategyCard}>
            <Text style={styles.strategyName}>ML Predictor</Text>
            <Text style={styles.strategyPerformance}>-0.8%</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.alertsContainer}>
          <Text style={styles.sectionTitle}>Recent Alerts</Text>
          <View style={styles.alertItem}>
            <Text style={styles.alertTime}>10:32 AM</Text>
            <Text style={styles.alertText}>New trading signal: Buy AAPL</Text>
          </View>
          <View style={styles.alertItem}>
            <Text style={styles.alertTime}>09:45 AM</Text>
            <Text style={styles.alertText}>Risk threshold exceeded on Strategy #2</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  header: {
    padding: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  subtitle: {
    fontSize: 16,
    color: '#aaaaaa',
    marginTop: 5,
  },
  portfolioSummary: {
    padding: 20,
    backgroundColor: '#1e1e1e',
    borderRadius: 10,
    marginHorizontal: 20,
  },
  portfolioValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  changeContainer: {
    marginTop: 10,
  },
  positiveChange: {
    color: '#1aff92',
    fontSize: 18,
  },
  negativeChange: {
    color: '#ff4d4d',
    fontSize: 18,
  },
  chartContainer: {
    marginTop: 20,
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 15,
  },
  chart: {
    borderRadius: 16,
  },
  strategiesContainer: {
    marginTop: 10,
    padding: 20,
  },
  strategyCard: {
    backgroundColor: '#1e1e1e',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  strategyName: {
    fontSize: 16,
    color: '#ffffff',
  },
  strategyPerformance: {
    fontSize: 16,
    color: '#1aff92',
    fontWeight: 'bold',
  },
  alertsContainer: {
    marginTop: 10,
    padding: 20,
    paddingBottom: 40,
  },
  alertItem: {
    backgroundColor: '#1e1e1e',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  alertTime: {
    fontSize: 14,
    color: '#aaaaaa',
  },
  alertText: {
    fontSize: 16,
    color: '#ffffff',
    marginTop: 5,
  },
});

export default DashboardScreen;
