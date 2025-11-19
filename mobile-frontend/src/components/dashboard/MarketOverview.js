import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../context/ThemeContext';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const MarketOverview = () => {
  const { theme } = useTheme();
  const screenWidth = Dimensions.get('window').width;

  // Mock market data
  const marketData = {
    indices: [
      { name: 'S&P 500', value: '5,328.42', change: '+0.82%', direction: 'up' },
      { name: 'NASDAQ', value: '16,742.39', change: '+1.14%', direction: 'up' },
      { name: 'DOW', value: '38,996.35', change: '-0.13%', direction: 'down' },
    ],
    chartData: {
      labels: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM'],
      datasets: [
        {
          data: [5280, 5290, 5310, 5300, 5320, 5315, 5325, 5328],
        },
      ],
    },
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.card }]}>
      <Text style={[styles.title, { color: theme.text }]}>Market Overview</Text>

      <View style={styles.indicesContainer}>
        {marketData.indices.map((index, i) => (
          <View key={i} style={styles.indexItem}>
            <Text style={[styles.indexName, { color: theme.text }]}>{index.name}</Text>
            <Text style={[styles.indexValue, { color: theme.text }]}>{index.value}</Text>
            <Text
              style={[
                styles.indexChange,
                {
                  color: index.direction === 'up' ? theme.success : theme.error,
                },
              ]}
            >
              {index.change}
            </Text>
          </View>
        ))}
      </View>

      <LineChart
        data={marketData.chartData}
        width={screenWidth - 40}
        height={180}
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
            r: '4',
            strokeWidth: '2',
            stroke: theme.primary,
          },
        }}
        bezier
        style={styles.chart}
        withDots={false}
        withInnerLines={false}
        withOuterLines={false}
        withVerticalLines={false}
        withHorizontalLines={true}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    padding: 16,
    marginTop: 20,
    marginHorizontal: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  indicesContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  indexItem: {
    alignItems: 'center',
  },
  indexName: {
    fontSize: 14,
    marginBottom: 4,
  },
  indexValue: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  indexChange: {
    fontSize: 14,
    fontWeight: '500',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
});

export default MarketOverview;
