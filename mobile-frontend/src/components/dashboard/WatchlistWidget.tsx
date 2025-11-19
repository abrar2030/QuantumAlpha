import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import * as Animatable from 'react-native-animatable';

import { useTheme } from '../../context/ThemeContext';
import { useApiQuery } from '../../hooks';
import Card from '../ui/Card';
import { SkeletonLoader } from '../ui/LoadingSpinner';
import { formatCurrency, formatPercentage } from '../../utils';
import { SPACING, COLORS } from '../../constants';
import { Asset } from '../../types';

interface WatchlistWidgetProps {
  maxItems?: number;
}

const WatchlistWidget: React.FC<WatchlistWidgetProps> = ({ maxItems = 5 }) => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  const [selectedTab, setSelectedTab] = useState<'stocks' | 'crypto'>('stocks');

  const {
    data: watchlistData,
    isLoading,
  } = useApiQuery(
    ['watchlist', selectedTab],
    () => fetchWatchlistData(selectedTab),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  );

  // Mock function - replace with actual API call
  const fetchWatchlistData = async (type: 'stocks' | 'crypto'): Promise<Asset[]> => {
    // This would be replaced with actual API call
    const mockData: Asset[] = [
      {
        symbol: type === 'stocks' ? 'AAPL' : 'BTC',
        name: type === 'stocks' ? 'Apple Inc.' : 'Bitcoin',
        type: type === 'stocks' ? 'stock' : 'crypto',
        exchange: type === 'stocks' ? 'NASDAQ' : 'Binance',
        currency: 'USD',
        price: type === 'stocks' ? 175.43 : 43250.00,
        change: type === 'stocks' ? 2.15 : -1250.00,
        changePercent: type === 'stocks' ? 1.24 : -2.81,
        volume: 1000000,
        isActive: true,
        isTradable: true,
      },
      // Add more mock data...
    ];
    return mockData;
  };

  const handleAssetPress = (asset: Asset) => {
    navigation.navigate('AssetDetail' as never, { symbol: asset.symbol } as never);
  };

  const handleSeeAllPress = () => {
    navigation.navigate('Watchlist' as never);
  };

  const handleTabPress = (tab: 'stocks' | 'crypto') => {
    setSelectedTab(tab);
  };

  const renderTabButton = (tab: 'stocks' | 'crypto', label: string) => (
    <TouchableOpacity
      style={[
        styles.tabButton,
        {
          backgroundColor: selectedTab === tab ? theme.primary : 'transparent',
          borderColor: theme.primary,
        }
      ]}
      onPress={() => handleTabPress(tab)}
    >
      <Text
        style={[
          styles.tabText,
          {
            color: selectedTab === tab ? '#ffffff' : theme.primary,
          }
        ]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );

  const renderAssetItem = (asset: Asset, index: number) => {
    const isPositive = asset.change >= 0;

    return (
      <Animatable.View
        key={asset.symbol}
        animation="fadeInRight"
        delay={index * 100}
      >
        <TouchableOpacity
          style={[styles.assetItem, { borderBottomColor: theme.border }]}
          onPress={() => handleAssetPress(asset)}
        >
          <View style={styles.assetInfo}>
            <Text style={[styles.assetSymbol, { color: theme.text }]}>
              {asset.symbol}
            </Text>
            <Text style={[styles.assetName, { color: theme.text + '80' }]} numberOfLines={1}>
              {asset.name}
            </Text>
          </View>

          <View style={styles.assetPricing}>
            <Text style={[styles.assetPrice, { color: theme.text }]}>
              {formatCurrency(asset.price)}
            </Text>
            <View style={styles.changeContainer}>
              <Icon
                name={isPositive ? 'trending-up' : 'trending-down'}
                size={12}
                color={isPositive ? COLORS.CHART.POSITIVE : COLORS.CHART.NEGATIVE}
              />
              <Text
                style={[
                  styles.assetChange,
                  {
                    color: isPositive ? COLORS.CHART.POSITIVE : COLORS.CHART.NEGATIVE,
                    marginLeft: 4,
                  }
                ]}
              >
                {formatPercentage(asset.changePercent)}
              </Text>
            </View>
          </View>
        </TouchableOpacity>
      </Animatable.View>
    );
  };

  if (isLoading) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.text }]}>Watchlist</Text>
        </View>
        <SkeletonLoader type="list" count={3} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.text }]}>Watchlist</Text>
        <TouchableOpacity onPress={handleSeeAllPress}>
          <Text style={[styles.seeAllText, { color: theme.primary }]}>
            See All
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.tabContainer}>
        {renderTabButton('stocks', 'Stocks')}
        {renderTabButton('crypto', 'Crypto')}
      </View>

      <Card variant="elevated" padding="none" margin="medium">
        {watchlistData && watchlistData.length > 0 ? (
          <View style={styles.assetList}>
            {watchlistData.slice(0, maxItems).map((asset, index) =>
              renderAssetItem(asset, index)
            )}
          </View>
        ) : (
          <View style={styles.emptyState}>
            <Icon name="eye-off" size={40} color={theme.text + '60'} />
            <Text style={[styles.emptyStateText, { color: theme.text }]}>
              No assets in watchlist
            </Text>
            <TouchableOpacity
              style={[styles.addButton, { borderColor: theme.primary }]}
              onPress={() => navigation.navigate('AssetSearch' as never)}
            >
              <Icon name="plus" size={16} color={theme.primary} />
              <Text style={[styles.addButtonText, { color: theme.primary }]}>
                Add Assets
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </Card>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: SPACING.MD,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.MD,
    marginBottom: SPACING.SM,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  seeAllText: {
    fontSize: 14,
    fontWeight: '600',
  },
  tabContainer: {
    flexDirection: 'row',
    paddingHorizontal: SPACING.MD,
    marginBottom: SPACING.SM,
  },
  tabButton: {
    paddingHorizontal: SPACING.MD,
    paddingVertical: SPACING.XS,
    borderRadius: 16,
    borderWidth: 1,
    marginRight: SPACING.SM,
  },
  tabText: {
    fontSize: 12,
    fontWeight: '600',
  },
  assetList: {
    paddingVertical: SPACING.XS,
  },
  assetItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.MD,
    paddingVertical: SPACING.SM,
    borderBottomWidth: 0.5,
  },
  assetInfo: {
    flex: 1,
  },
  assetSymbol: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  assetName: {
    fontSize: 12,
    marginTop: 2,
  },
  assetPricing: {
    alignItems: 'flex-end',
  },
  assetPrice: {
    fontSize: 16,
    fontWeight: '600',
  },
  changeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 2,
  },
  assetChange: {
    fontSize: 12,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.XXL,
  },
  emptyStateText: {
    marginTop: SPACING.SM,
    fontSize: 14,
    textAlign: 'center',
    marginBottom: SPACING.MD,
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.MD,
    paddingVertical: SPACING.SM,
    borderWidth: 1,
    borderRadius: 8,
  },
  addButtonText: {
    fontSize: 14,
    fontWeight: '600',
    marginLeft: SPACING.XS,
  },
});

export default WatchlistWidget;
