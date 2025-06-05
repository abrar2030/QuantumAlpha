import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Animated,
  Dimensions,
  FlatList,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';

const TradeScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [orderType, setOrderType] = useState('market');
  const [orderSide, setOrderSide] = useState('buy');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  
  // Animation values
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const translateY = React.useRef(new Animated.Value(50)).current;
  
  // Mock data for popular assets
  const popularAssets = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 320.45, change: 1.2 },
    { symbol: 'MSFT', name: 'Microsoft Corp.', price: 350.20, change: 0.8 },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 1200.75, change: -0.5 },
    { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 2000.10, change: 1.5 },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 780.65, change: 2.3 },
    { symbol: 'META', name: 'Meta Platforms Inc.', price: 320.30, change: -0.3 },
  ];
  
  useEffect(() => {
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
  
  useEffect(() => {
    if (searchQuery.length > 0) {
      // Simulate search results
      const results = popularAssets.filter(
        (asset) =>
          asset.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
          asset.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);
  
  const handleAssetSelect = (asset) => {
    setSelectedAsset(asset);
    setSearchQuery('');
    setSearchResults([]);
  };
  
  const handlePlaceOrder = () => {
    if (!selectedAsset || !quantity) {
      alert('Please select an asset and enter quantity');
      return;
    }
    
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      alert(`Order placed: ${orderSide.toUpperCase()} ${quantity} ${selectedAsset.symbol} at ${orderType === 'market' ? 'market price' : '$' + price}`);
      
      // Reset form
      setSelectedAsset(null);
      setQuantity('');
      setPrice('');
    }, 1500);
  };
  
  const renderAssetItem = ({ item }) => {
    return (
      <TouchableOpacity
        style={[styles.assetItem, { backgroundColor: theme.card }]}
        onPress={() => handleAssetSelect(item)}
      >
        <View style={styles.assetInfo}>
          <Text style={[styles.assetSymbol, { color: theme.text }]}>{item.symbol}</Text>
          <Text style={[styles.assetName, { color: theme.text + 'CC' }]}>
            {item.name}
          </Text>
        </View>
        <View style={styles.assetPrice}>
          <Text style={[styles.priceText, { color: theme.text }]}>
            ${item.price.toFixed(2)}
          </Text>
          <Text
            style={[
              styles.changeText,
              {
                color: item.change >= 0 ? theme.success : theme.error,
              },
            ]}
          >
            {item.change >= 0 ? '+' : ''}
            {item.change}%
          </Text>
        </View>
      </TouchableOpacity>
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
        <Text style={[styles.headerTitle, { color: theme.text }]}>Trade</Text>
      </Animated.View>
      
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animated.View
          style={{
            opacity: fadeAnim,
            transform: [{ translateY }],
          }}
        >
          <View style={[styles.searchContainer, { backgroundColor: theme.card }]}>
            <View style={[styles.searchInputContainer, { backgroundColor: theme.background }]}>
              <Icon name="magnify" size={20} color={theme.text + '99'} />
              <TextInput
                style={[styles.searchInput, { color: theme.text }]}
                placeholder="Search assets..."
                placeholderTextColor={theme.text + '99'}
                value={searchQuery}
                onChangeText={setSearchQuery}
              />
              {searchQuery ? (
                <TouchableOpacity onPress={() => setSearchQuery('')}>
                  <Icon name="close" size={20} color={theme.text + '99'} />
                </TouchableOpacity>
              ) : null}
            </View>
            
            {searchResults.length > 0 && (
              <View style={[styles.searchResults, { backgroundColor: theme.background }]}>
                <FlatList
                  data={searchResults}
                  renderItem={renderAssetItem}
                  keyExtractor={(item) => item.symbol}
                  contentContainerStyle={styles.searchResultsList}
                />
              </View>
            )}
          </View>
          
          {!selectedAsset ? (
            <View style={[styles.popularAssetsContainer, { backgroundColor: theme.card }]}>
              <Text style={[styles.sectionTitle, { color: theme.text }]}>
                Popular Assets
              </Text>
              {popularAssets.map((asset) => (
                <TouchableOpacity
                  key={asset.symbol}
                  style={[
                    styles.popularAssetItem,
                    { borderBottomColor: theme.border },
                  ]}
                  onPress={() => handleAssetSelect(asset)}
                >
                  <View style={styles.assetInfo}>
                    <Text style={[styles.assetSymbol, { color: theme.text }]}>
                      {asset.symbol}
                    </Text>
                    <Text style={[styles.assetName, { color: theme.text + 'CC' }]}>
                      {asset.name}
                    </Text>
                  </View>
                  <View style={styles.assetPrice}>
                    <Text style={[styles.priceText, { color: theme.text }]}>
                      ${asset.price.toFixed(2)}
                    </Text>
                    <Text
                      style={[
                        styles.changeText,
                        {
                          color: asset.change >= 0 ? theme.success : theme.error,
                        },
                      ]}
                    >
                      {asset.change >= 0 ? '+' : ''}
                      {asset.change}%
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <View style={[styles.orderFormContainer, { backgroundColor: theme.card }]}>
              <View style={styles.selectedAssetHeader}>
                <View style={styles.assetInfo}>
                  <Text style={[styles.assetSymbol, { color: theme.text }]}>
                    {selectedAsset.symbol}
                  </Text>
                  <Text style={[styles.assetName, { color: theme.text + 'CC' }]}>
                    {selectedAsset.name}
                  </Text>
                </View>
                <TouchableOpacity
                  style={styles.changeAssetButton}
                  onPress={() => setSelectedAsset(null)}
                >
                  <Text style={[styles.changeAssetText, { color: theme.primary }]}>
                    Change
                  </Text>
                </TouchableOpacity>
              </View>
              
              <View style={styles.priceContainer}>
                <Text style={[styles.currentPrice, { color: theme.text }]}>
                  ${selectedAsset.price.toFixed(2)}
                </Text>
                <Text
                  style={[
                    styles.priceChange,
                    {
                      color:
                        selectedAsset.change >= 0 ? theme.success : theme.error,
                    },
                  ]}
                >
                  {selectedAsset.change >= 0 ? '+' : ''}
                  {selectedAsset.change}%
                </Text>
              </View>
              
              <View style={styles.orderTypeContainer}>
                <Text style={[styles.formLabel, { color: theme.text }]}>
                  Order Type
                </Text>
                <View style={styles.segmentedControl}>
                  <TouchableOpacity
                    style={[
                      styles.segmentButton,
                      orderType === 'market' && [
                        styles.activeSegment,
                        { backgroundColor: theme.primary },
                      ],
                    ]}
                    onPress={() => setOrderType('market')}
                  >
                    <Text
                      style={[
                        styles.segmentText,
                        {
                          color:
                            orderType === 'market' ? '#FFFFFF' : theme.text,
                        },
                      ]}
                    >
                      Market
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[
                      styles.segmentButton,
                      orderType === 'limit' && [
                        styles.activeSegment,
                        { backgroundColor: theme.primary },
                      ],
                    ]}
                    onPress={() => setOrderType('limit')}
                  >
                    <Text
                      style={[
                        styles.segmentText,
                        {
                          color:
                            orderType === 'limit' ? '#FFFFFF' : theme.text,
                        },
                      ]}
                    >
                      Limit
                    </Text>
                  </TouchableOpacity>
                </View>
              </View>
              
              <View style={styles.orderSideContainer}>
                <Text style={[styles.formLabel, { color: theme.text }]}>
                  Order Side
                </Text>
                <View style={styles.segmentedControl}>
                  <TouchableOpacity
                    style={[
                      styles.segmentButton,
                      orderSide === 'buy' && [
                        styles.activeSegment,
                        { backgroundColor: theme.success },
                      ],
                    ]}
                    onPress={() => setOrderSide('buy')}
                  >
                    <Text
                      style={[
                        styles.segmentText,
                        {
                          color: orderSide === 'buy' ? '#FFFFFF' : theme.text,
                        },
                      ]}
                    >
                      Buy
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[
                      styles.segmentButton,
                      orderSide === 'sell' && [
                        styles.activeSegment,
                        { backgroundColor: theme.error },
                      ],
                    ]}
                    onPress={() => setOrderSide('sell')}
                  >
                    <Text
                      style={[
                        styles.segmentText,
                        {
                          color: orderSide === 'sell' ? '#FFFFFF' : theme.text,
                        },
                      ]}
                    >
                      Sell
                    </Text>
                  </TouchableOpacity>
                </View>
              </View>
              
              <View style={styles.inputContainer}>
                <Text style={[styles.formLabel, { color: theme.text }]}>
                  Quantity
                </Text>
                <TextInput
                  style={[
                    styles.formInput,
                    { color: theme.text, borderColor: theme.border },
                  ]}
                  placeholder="Enter quantity"
                  placeholderTextColor={theme.text + '99'}
                  value={quantity}
                  onChangeText={setQuantity}
                  keyboardType="numeric"
                />
              </View>
              
              {orderType === 'limit' && (
                <View style={styles.inputContainer}>
                  <Text style={[styles.formLabel, { color: theme.text }]}>
                    Limit Price
                  </Text>
                  <TextInput
                    style={[
                      styles.formInput,
                      { color: theme.text, borderColor: theme.border },
                    ]}
                    placeholder="Enter price"
                    placeholderTextColor={theme.text + '99'}
                    value={price}
                    onChangeText={setPrice}
                    keyboardType="numeric"
                  />
                </View>
              )}
              
              <View style={styles.orderSummary}>
                <Text style={[styles.summaryTitle, { color: theme.text }]}>
                  Order Summary
                </Text>
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                    Asset
                  </Text>
                  <Text style={[styles.summaryValue, { color: theme.text }]}>
                    {selectedAsset.symbol}
                  </Text>
                </View>
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                    Type
                  </Text>
                  <Text style={[styles.summaryValue, { color: theme.text }]}>
                    {orderType.charAt(0).toUpperCase() + orderType.slice(1)}
                  </Text>
                </View>
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                    Side
                  </Text>
                  <Text
                    style={[
                      styles.summaryValue,
                      {
                        color: orderSide === 'buy' ? theme.success : theme.error,
                        fontWeight: 'bold',
                      },
                    ]}
                  >
                    {orderSide.toUpperCase()}
                  </Text>
                </View>
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                    Quantity
                  </Text>
                  <Text style={[styles.summaryValue, { color: theme.text }]}>
                    {quantity || '0'}
                  </Text>
                </View>
                {orderType === 'limit' && (
                  <View style={styles.summaryRow}>
                    <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                      Price
                    </Text>
                    <Text style={[styles.summaryValue, { color: theme.text }]}>
                      ${price || '0'}
                    </Text>
                  </View>
                )}
                <View style={styles.summaryRow}>
                  <Text style={[styles.summaryLabel, { color: theme.text + 'CC' }]}>
                    Estimated Total
                  </Text>
                  <Text style={[styles.summaryValue, { color: theme.text, fontWeight: 'bold' }]}>
                    $
                    {quantity && selectedAsset.price
                      ? (parseFloat(quantity) * selectedAsset.price).toFixed(2)
                      : '0.00'}
                  </Text>
                </View>
              </View>
              
              <TouchableOpacity
                style={[
                  styles.placeOrderButton,
                  {
                    backgroundColor:
                      orderSide === 'buy' ? theme.success : theme.error,
                  },
                ]}
                onPress={handlePlaceOrder}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator color="#FFFFFF" size="small" />
                ) : (
                  <Text style={styles.placeOrderText}>
                    {orderSide === 'buy' ? 'Buy' : 'Sell'} {selectedAsset.symbol}
                  </Text>
                )}
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.cancelButton, { borderColor: theme.border }]}
                onPress={() => setSelectedAsset(null)}
                disabled={loading}
              >
                <Text style={[styles.cancelButtonText, { color: theme.text }]}>
                  Cancel
                </Text>
              </TouchableOpacity>
            </View>
          )}
        </Animated.View>
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
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  searchContainer: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    position: 'relative',
    zIndex: 10,
  },
  searchInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 8,
    paddingHorizontal: 12,
    height: 40,
  },
  searchInput: {
    flex: 1,
    marginLeft: 8,
    fontSize: 16,
  },
  searchResults: {
    position: 'absolute',
    top: 70,
    left: 0,
    right: 0,
    borderRadius: 12,
    maxHeight: 300,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 5,
    zIndex: 20,
  },
  searchResultsList: {
    padding: 8,
  },
  popularAssetsContainer: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  popularAssetItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  assetItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
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
  assetPrice: {
    alignItems: 'flex-end',
  },
  priceText: {
    fontSize: 16,
    fontWeight: '500',
  },
  changeText: {
    fontSize: 12,
    marginTop: 2,
  },
  orderFormContainer: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  selectedAssetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  changeAssetButton: {
    padding: 8,
  },
  changeAssetText: {
    fontSize: 14,
    fontWeight: '500',
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 20,
  },
  currentPrice: {
    fontSize: 24,
    fontWeight: 'bold',
    marginRight: 8,
  },
  priceChange: {
    fontSize: 16,
    fontWeight: '500',
  },
  orderTypeContainer: {
    marginBottom: 16,
  },
  formLabel: {
    fontSize: 14,
    marginBottom: 8,
  },
  segmentedControl: {
    flexDirection: 'row',
    borderRadius: 8,
    overflow: 'hidden',
  },
  segmentButton: {
    flex: 1,
    paddingVertical: 10,
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.05)',
  },
  activeSegment: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1.5,
    elevation: 2,
  },
  segmentText: {
    fontSize: 14,
    fontWeight: '500',
  },
  orderSideContainer: {
    marginBottom: 16,
  },
  inputContainer: {
    marginBottom: 16,
  },
  formInput: {
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
  },
  orderSummary: {
    marginTop: 16,
    marginBottom: 24,
    padding: 16,
    borderRadius: 8,
    backgroundColor: 'rgba(0,0,0,0.05)',
  },
  summaryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  summaryLabel: {
    fontSize: 14,
  },
  summaryValue: {
    fontSize: 14,
  },
  placeOrderButton: {
    height: 50,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  placeOrderText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  cancelButton: {
    height: 50,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
  },
  cancelButtonText: {
    fontSize: 16,
    fontWeight: '500',
  },
});

export default TradeScreen;
