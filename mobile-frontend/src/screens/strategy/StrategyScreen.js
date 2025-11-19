import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Animated,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';
import { strategyService } from '../../services/strategyService';

const StrategyScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [strategies, setStrategies] = useState([]);
  const [availableStrategies, setAvailableStrategies] = useState([]);

  // Animation values
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const translateY = React.useRef(new Animated.Value(50)).current;

  React.useEffect(() => {
    loadStrategies();

    // Start animations when component mounts
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
  }, []);

  const loadStrategies = async () => {
    try {
      setLoading(true);

      // In a real app, these would be API calls
      const activeStrategies = await strategyService.getActiveStrategies();
      const available = await strategyService.getAvailableStrategies();

      setStrategies(activeStrategies);
      setAvailableStrategies(available);
    } catch (error) {
      console.error('Error loading strategies:', error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadStrategies();
  };

  const navigateToStrategyDetail = (strategy) => {
    navigation.navigate('StrategyDetail', {
      id: strategy.id,
      name: strategy.name,
    });
  };

  const renderStrategyItem = ({ item, index }) => {
    const itemFadeAnim = React.useRef(new Animated.Value(0)).current;
    const itemTranslateY = React.useRef(new Animated.Value(20)).current;

    React.useEffect(() => {
      // Stagger the animations for each item
      Animated.parallel([
        Animated.timing(itemFadeAnim, {
          toValue: 1,
          duration: 500,
          delay: index * 100,
          useNativeDriver: true,
        }),
        Animated.timing(itemTranslateY, {
          toValue: 0,
          duration: 500,
          delay: index * 100,
          useNativeDriver: true,
        }),
      ]).start();
    }, []);

    return (
      <Animated.View
        style={[
          styles.strategyItemContainer,
          {
            opacity: itemFadeAnim,
            transform: [{ translateY: itemTranslateY }],
          },
        ]}
      >
        <TouchableOpacity
          style={[styles.strategyItem, { backgroundColor: theme.card }]}
          onPress={() => navigateToStrategyDetail(item)}
          activeOpacity={0.7}
        >
          <View style={styles.strategyHeader}>
            <Text style={[styles.strategyName, { color: theme.text }]}>
              {item.name}
            </Text>
            <View
              style={[
                styles.performanceBadge,
                {
                  backgroundColor:
                    item.performance >= 0 ? theme.success + '20' : theme.error + '20',
                },
              ]}
            >
              <Text
                style={[
                  styles.performanceText,
                  {
                    color: item.performance >= 0 ? theme.success : theme.error,
                  },
                ]}
              >
                {item.performance >= 0 ? '+' : ''}
                {item.performance}%
              </Text>
            </View>
          </View>

          <Text
            style={[styles.strategyDescription, { color: theme.text + 'CC' }]}
            numberOfLines={2}
          >
            {item.description}
          </Text>

          <View style={styles.strategyFooter}>
            <View style={styles.strategyDetail}>
              <Icon name="shield" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                {item.risk}
              </Text>
            </View>

            <View style={styles.strategyDetail}>
              <Icon name="chart-pie" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                {item.allocation}% Allocated
              </Text>
            </View>

            <View style={styles.strategyDetail}>
              <Icon name="clock-outline" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                {new Date(item.lastUpdated).toLocaleDateString()}
              </Text>
            </View>
          </View>

          <View style={styles.arrowContainer}>
            <Icon name="chevron-right" size={24} color={theme.text + '80'} />
          </View>
        </TouchableOpacity>
      </Animated.View>
    );
  };

  const renderAvailableStrategyItem = ({ item, index }) => {
    const itemFadeAnim = React.useRef(new Animated.Value(0)).current;
    const itemTranslateY = React.useRef(new Animated.Value(20)).current;

    React.useEffect(() => {
      // Stagger the animations for each item
      Animated.parallel([
        Animated.timing(itemFadeAnim, {
          toValue: 1,
          duration: 500,
          delay: (index + strategies.length) * 100,
          useNativeDriver: true,
        }),
        Animated.timing(itemTranslateY, {
          toValue: 0,
          duration: 500,
          delay: (index + strategies.length) * 100,
          useNativeDriver: true,
        }),
      ]).start();
    }, []);

    return (
      <Animated.View
        style={[
          styles.strategyItemContainer,
          {
            opacity: itemFadeAnim,
            transform: [{ translateY: itemTranslateY }],
          },
        ]}
      >
        <TouchableOpacity
          style={[
            styles.strategyItem,
            styles.availableStrategyItem,
            { backgroundColor: theme.card },
          ]}
          onPress={() => {
            // In a real app, this would navigate to a strategy details or activation screen
            alert(`Would activate ${item.name} strategy`);
          }}
          activeOpacity={0.7}
        >
          <View style={styles.strategyHeader}>
            <Text style={[styles.strategyName, { color: theme.text }]}>
              {item.name}
            </Text>
            <View
              style={[
                styles.newBadge,
                {
                  backgroundColor: theme.primary + '20',
                },
              ]}
            >
              <Text
                style={[
                  styles.newBadgeText,
                  {
                    color: theme.primary,
                  },
                ]}
              >
                NEW
              </Text>
            </View>
          </View>

          <Text
            style={[styles.strategyDescription, { color: theme.text + 'CC' }]}
            numberOfLines={2}
          >
            {item.description}
          </Text>

          <View style={styles.strategyFooter}>
            <View style={styles.strategyDetail}>
              <Icon name="shield" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                {item.risk}
              </Text>
            </View>

            <View style={styles.strategyDetail}>
              <Icon name="chart-line-variant" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                {item.expectedReturn}
              </Text>
            </View>

            <View style={styles.strategyDetail}>
              <Icon name="cash" size={16} color={theme.text + '99'} />
              <Text style={[styles.detailText, { color: theme.text + '99' }]}>
                ${item.minimumInvestment.toLocaleString()}
              </Text>
            </View>
          </View>

          <TouchableOpacity
            style={[styles.activateButton, { backgroundColor: theme.primary }]}
            onPress={() => {
              // In a real app, this would activate the strategy
              alert(`Would activate ${item.name} strategy`);
            }}
          >
            <Text style={styles.activateButtonText}>Activate</Text>
          </TouchableOpacity>
        </TouchableOpacity>
      </Animated.View>
    );
  };

  if (loading && !refreshing) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: theme.background }]}>
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading strategies...
        </Text>
      </View>
    );
  }

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
        <Text style={[styles.headerTitle, { color: theme.text }]}>
          Trading Strategies
        </Text>
        <Text style={[styles.headerSubtitle, { color: theme.text + 'CC' }]}>
          Manage your active and available strategies
        </Text>
      </Animated.View>

      <FlatList
        data={strategies}
        renderItem={renderStrategyItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={theme.primary}
            colors={[theme.primary]}
          />
        }
        ListHeaderComponent={
          <Animated.View
            style={{
              opacity: fadeAnim,
              transform: [{ translateY }],
            }}
          >
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Active Strategies
            </Text>
          </Animated.View>
        }
        ListFooterComponent={
          <>
            <Animated.View
              style={{
                opacity: fadeAnim,
                transform: [{ translateY }],
                marginTop: 30,
              }}
            >
              <Text style={[styles.sectionTitle, { color: theme.text }]}>
                Available Strategies
              </Text>
            </Animated.View>

            {availableStrategies.map((item, index) =>
              renderAvailableStrategyItem({ item, index })
            )}

            <View style={styles.footer} />
          </>
        }
      />

      <TouchableOpacity
        style={[styles.fab, { backgroundColor: theme.primary }]}
        onPress={() => {
          // In a real app, this would navigate to a strategy creation screen
          alert('Would navigate to strategy creation');
        }}
      >
        <Icon name="plus" size={24} color="#FFFFFF" />
      </TouchableOpacity>
    </View>
  );
};

const { width } = Dimensions.get('window');

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
    padding: 20,
    paddingTop: 15,
    paddingBottom: 15,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 14,
    marginTop: 5,
  },
  listContent: {
    padding: 16,
    paddingTop: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  strategyItemContainer: {
    marginBottom: 16,
  },
  strategyItem: {
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    position: 'relative',
  },
  availableStrategyItem: {
    borderStyle: 'dashed',
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.1)',
  },
  strategyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  strategyName: {
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1,
  },
  performanceBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginLeft: 8,
  },
  performanceText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  newBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginLeft: 8,
  },
  newBadgeText: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  strategyDescription: {
    fontSize: 14,
    marginBottom: 12,
  },
  strategyFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
  },
  strategyDetail: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 12,
    marginBottom: 4,
  },
  detailText: {
    fontSize: 12,
    marginLeft: 4,
  },
  arrowContainer: {
    position: 'absolute',
    right: 16,
    top: '50%',
    marginTop: -12,
  },
  activateButton: {
    marginTop: 12,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 4,
    alignSelf: 'flex-end',
  },
  activateButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 14,
  },
  footer: {
    height: 80,
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.27,
    shadowRadius: 4.65,
  },
});

export default StrategyScreen;
