import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import HapticFeedback from 'react-native-haptic-feedback';

import { useTheme } from '../../context/ThemeContext';
import Card from '../ui/Card';
import { SPACING, COLORS } from '../../constants';

interface QuickAction {
  id: string;
  title: string;
  icon: string;
  color: string;
  route: string;
  params?: any;
}

const QuickActions: React.FC = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();

  const quickActions: QuickAction[] = [
    {
      id: 'trade',
      title: 'Trade',
      icon: 'swap-horizontal',
      color: COLORS.PRIMARY,
      route: 'TradeTab',
    },
    {
      id: 'portfolio',
      title: 'Portfolio',
      icon: 'chart-line',
      color: COLORS.SECONDARY,
      route: 'PortfolioTab',
    },
    {
      id: 'watchlist',
      title: 'Watchlist',
      icon: 'eye',
      color: COLORS.CHART.POSITIVE,
      route: 'Watchlist',
    },
    {
      id: 'news',
      title: 'News',
      icon: 'newspaper',
      color: COLORS.WARNING,
      route: 'News',
    },
    {
      id: 'scanner',
      title: 'Scanner',
      icon: 'radar',
      color: COLORS.CHART.VOLUME,
      route: 'Scanner',
    },
    {
      id: 'calculator',
      title: 'Calculator',
      icon: 'calculator',
      color: COLORS.INFO,
      route: 'Calculator',
    },
  ];

  const handleActionPress = (action: QuickAction) => {
    HapticFeedback.trigger('impactLight');
    navigation.navigate(action.route as never, action.params as never);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.text }]}>Quick Actions</Text>
      </View>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.actionsContainer}
      >
        {quickActions.map((action, index) => (
          <Card
            key={action.id}
            variant="elevated"
            padding="medium"
            margin="none"
            style={[styles.actionCard, { marginLeft: index === 0 ? SPACING.MD : SPACING.SM }]}
            onPress={() => handleActionPress(action)}
            animated
            animationType="zoomIn"
            animationDelay={index * 100}
          >
            <View style={[styles.iconContainer, { backgroundColor: action.color + '20' }]}>
              <Icon name={action.icon} size={24} color={action.color} />
            </View>
            <Text style={[styles.actionTitle, { color: theme.text }]}>
              {action.title}
            </Text>
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
    paddingHorizontal: SPACING.MD,
    marginBottom: SPACING.SM,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  actionsContainer: {
    paddingRight: SPACING.MD,
  },
  actionCard: {
    alignItems: 'center',
    minWidth: 80,
    marginRight: SPACING.SM,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.SM,
  },
  actionTitle: {
    fontSize: 12,
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default QuickActions;
