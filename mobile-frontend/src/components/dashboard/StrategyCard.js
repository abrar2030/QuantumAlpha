import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useTheme } from '../../context/ThemeContext';

const StrategyCard = ({ strategy, onPress }) => {
  const { theme } = useTheme();
  
  return (
    <TouchableOpacity 
      style={[styles.container, { backgroundColor: theme.card }]}
      onPress={onPress}
    >
      <View style={styles.header}>
        <Text style={[styles.name, { color: theme.text }]}>{strategy.name}</Text>
        <Text 
          style={[
            styles.performance, 
            { color: strategy.performance >= 0 ? theme.success : theme.error }
          ]}
        >
          {strategy.performance >= 0 ? '+' : ''}{strategy.performance}%
        </Text>
      </View>
      
      <Text 
        style={[styles.description, { color: theme.text + 'CC' }]}
        numberOfLines={2}
      >
        {strategy.description}
      </Text>
      
      <View style={styles.footer}>
        <View style={styles.detail}>
          <Text style={[styles.detailLabel, { color: theme.text + '99' }]}>Risk</Text>
          <Text style={[styles.detailValue, { color: theme.text }]}>{strategy.risk}</Text>
        </View>
        
        <View style={styles.detail}>
          <Text style={[styles.detailLabel, { color: theme.text + '99' }]}>Allocation</Text>
          <Text style={[styles.detailValue, { color: theme.text }]}>{strategy.allocation}%</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  performance: {
    fontSize: 16,
    fontWeight: '500',
  },
  description: {
    fontSize: 14,
    marginBottom: 12,
  },
  footer: {
    flexDirection: 'row',
  },
  detail: {
    marginRight: 24,
  },
  detailLabel: {
    fontSize: 12,
    marginBottom: 2,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '500',
  },
});

export default StrategyCard;
