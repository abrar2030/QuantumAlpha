import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Image,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import FastImage from 'react-native-fast-image';

import { useTheme } from '../../context/ThemeContext';
import Card from '../ui/Card';
import { SkeletonLoader } from '../ui/LoadingSpinner';
import { formatRelativeTime, truncateText } from '../../utils';
import { SPACING, COLORS } from '../../constants';
import { NewsArticle } from '../../types';

interface NewsWidgetProps {
  data?: NewsArticle[];
  loading?: boolean;
}

const NewsWidget: React.FC<NewsWidgetProps> = ({ data, loading }) => {
  const navigation = useNavigation();
  const { theme } = useTheme();

  const handleNewsPress = (article: NewsArticle) => {
    navigation.navigate('NewsDetail' as never, { article } as never);
  };

  const handleSeeAllPress = () => {
    navigation.navigate('News' as never);
  };

  const getSentimentColor = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive':
        return COLORS.CHART.POSITIVE;
      case 'negative':
        return COLORS.CHART.NEGATIVE;
      default:
        return COLORS.CHART.NEUTRAL;
    }
  };

  const getSentimentIcon = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive':
        return 'trending-up';
      case 'negative':
        return 'trending-down';
      default:
        return 'trending-neutral';
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.text }]}>Market News</Text>
        </View>
        <SkeletonLoader type="list" count={3} />
      </View>
    );
  }

  if (!data || data.length === 0) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.text }]}>Market News</Text>
        </View>
        <Card variant="outlined" padding="large" margin="medium">
          <View style={styles.emptyState}>
            <Icon name="newspaper-variant-outline" size={40} color={theme.text + '60'} />
            <Text style={[styles.emptyStateText, { color: theme.text }]}>
              No news available
            </Text>
          </View>
        </Card>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.text }]}>Market News</Text>
        <TouchableOpacity onPress={handleSeeAllPress}>
          <Text style={[styles.seeAllText, { color: theme.primary }]}>
            See All
          </Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.newsContainer}
      >
        {data.slice(0, 5).map((article, index) => (
          <Card
            key={article.id}
            variant="elevated"
            padding="none"
            margin="none"
            style={[
              styles.newsCard,
              { marginLeft: index === 0 ? SPACING.MD : SPACING.SM }
            ]}
            onPress={() => handleNewsPress(article)}
            animated
            animationType="slideInUp"
            animationDelay={index * 100}
          >
            {article.imageUrl && (
              <FastImage
                source={{ uri: article.imageUrl }}
                style={styles.newsImage}
                resizeMode={FastImage.resizeMode.cover}
              />
            )}

            <View style={styles.newsContent}>
              <View style={styles.newsHeader}>
                <Text style={[styles.newsSource, { color: theme.primary }]}>
                  {article.source}
                </Text>
                {article.sentiment && (
                  <View style={styles.sentimentContainer}>
                    <Icon
                      name={getSentimentIcon(article.sentiment)}
                      size={12}
                      color={getSentimentColor(article.sentiment)}
                    />
                  </View>
                )}
              </View>

              <Text style={[styles.newsTitle, { color: theme.text }]} numberOfLines={3}>
                {article.title}
              </Text>

              <Text style={[styles.newsSummary, { color: theme.text + '80' }]} numberOfLines={2}>
                {truncateText(article.summary, 100)}
              </Text>

              <View style={styles.newsFooter}>
                <Text style={[styles.newsTime, { color: theme.text + '60' }]}>
                  {formatRelativeTime(article.publishedAt)}
                </Text>
                {article.relevantSymbols.length > 0 && (
                  <View style={styles.symbolsContainer}>
                    {article.relevantSymbols.slice(0, 2).map((symbol) => (
                      <View
                        key={symbol}
                        style={[styles.symbolTag, { backgroundColor: theme.primary + '20' }]}
                      >
                        <Text style={[styles.symbolText, { color: theme.primary }]}>
                          {symbol}
                        </Text>
                      </View>
                    ))}
                  </View>
                )}
              </View>
            </View>
          </Card>
        ))}
      </ScrollView>
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
  newsContainer: {
    paddingRight: SPACING.MD,
  },
  newsCard: {
    width: 280,
    marginRight: SPACING.SM,
  },
  newsImage: {
    width: '100%',
    height: 120,
  },
  newsContent: {
    padding: SPACING.MD,
  },
  newsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.XS,
  },
  newsSource: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  sentimentContainer: {
    padding: 2,
  },
  newsTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    lineHeight: 18,
    marginBottom: SPACING.XS,
  },
  newsSummary: {
    fontSize: 12,
    lineHeight: 16,
    marginBottom: SPACING.SM,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  newsTime: {
    fontSize: 10,
  },
  symbolsContainer: {
    flexDirection: 'row',
  },
  symbolTag: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
    marginLeft: 4,
  },
  symbolText: {
    fontSize: 10,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.LG,
  },
  emptyStateText: {
    marginTop: SPACING.SM,
    fontSize: 14,
    textAlign: 'center',
  },
});

export default NewsWidget;
