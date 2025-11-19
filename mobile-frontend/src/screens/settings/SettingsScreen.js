import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Switch,
  Animated,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

const SettingsScreen = () => {
  const navigation = useNavigation();
  const { theme, isDarkMode, toggleTheme } = useTheme();
  const { user, logout } = useAuth();

  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [biometricEnabled, setBiometricEnabled] = useState(false);
  const [autoLockEnabled, setAutoLockEnabled] = useState(true);
  const [riskLevel, setRiskLevel] = useState('medium');

  // Animation values
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const translateY = React.useRef(new Animated.Value(50)).current;

  React.useEffect(() => {
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

  const handleLogout = async () => {
    try {
      await logout();
      // Navigation will be handled by the AuthContext
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const renderSettingSwitch = (title, description, value, onValueChange) => {
    return (
      <View style={[styles.settingItem, { borderBottomColor: theme.border }]}>
        <View style={styles.settingTextContainer}>
          <Text style={[styles.settingTitle, { color: theme.text }]}>{title}</Text>
          <Text style={[styles.settingDescription, { color: theme.text + 'CC' }]}>
            {description}
          </Text>
        </View>
        <Switch
          value={value}
          onValueChange={onValueChange}
          trackColor={{ false: theme.border, true: theme.primary }}
          thumbColor={value ? '#FFFFFF' : '#F4F3F4'}
          ios_backgroundColor={theme.border}
        />
      </View>
    );
  };

  const renderRiskLevelSelector = () => {
    return (
      <View style={[styles.settingItem, { borderBottomColor: theme.border }]}>
        <View style={styles.settingTextContainer}>
          <Text style={[styles.settingTitle, { color: theme.text }]}>
            Risk Tolerance Level
          </Text>
          <Text style={[styles.settingDescription, { color: theme.text + 'CC' }]}>
            Set your preferred risk level for trading strategies
          </Text>
        </View>
        <View style={styles.riskLevelContainer}>
          <TouchableOpacity
            style={[
              styles.riskLevelButton,
              riskLevel === 'low' && {
                backgroundColor: theme.success + '20',
                borderColor: theme.success,
              },
            ]}
            onPress={() => setRiskLevel('low')}
          >
            <Text
              style={[
                styles.riskLevelText,
                {
                  color: riskLevel === 'low' ? theme.success : theme.text + '99',
                  fontWeight: riskLevel === 'low' ? 'bold' : 'normal',
                },
              ]}
            >
              Low
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.riskLevelButton,
              riskLevel === 'medium' && {
                backgroundColor: theme.warning + '20',
                borderColor: theme.warning,
              },
            ]}
            onPress={() => setRiskLevel('medium')}
          >
            <Text
              style={[
                styles.riskLevelText,
                {
                  color: riskLevel === 'medium' ? theme.warning : theme.text + '99',
                  fontWeight: riskLevel === 'medium' ? 'bold' : 'normal',
                },
              ]}
            >
              Medium
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.riskLevelButton,
              riskLevel === 'high' && {
                backgroundColor: theme.error + '20',
                borderColor: theme.error,
              },
            ]}
            onPress={() => setRiskLevel('high')}
          >
            <Text
              style={[
                styles.riskLevelText,
                {
                  color: riskLevel === 'high' ? theme.error : theme.text + '99',
                  fontWeight: riskLevel === 'high' ? 'bold' : 'normal',
                },
              ]}
            >
              High
            </Text>
          </TouchableOpacity>
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
        <Text style={[styles.headerTitle, { color: theme.text }]}>Settings</Text>
      </Animated.View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animated.View
          style={{
            opacity: fadeAnim,
            transform: [{ translateY }],
          }}
        >
          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Appearance
            </Text>
            {renderSettingSwitch(
              'Dark Mode',
              'Enable dark mode for the app',
              isDarkMode,
              toggleTheme
            )}
          </View>

          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Notifications
            </Text>
            {renderSettingSwitch(
              'Push Notifications',
              'Receive alerts and updates',
              notificationsEnabled,
              setNotificationsEnabled
            )}
          </View>

          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Security
            </Text>
            {renderSettingSwitch(
              'Biometric Authentication',
              'Use Face ID or Touch ID to log in',
              biometricEnabled,
              setBiometricEnabled
            )}
            {renderSettingSwitch(
              'Auto-Lock',
              'Automatically lock the app when inactive',
              autoLockEnabled,
              setAutoLockEnabled
            )}
          </View>

          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Trading Preferences
            </Text>
            {renderRiskLevelSelector()}
          </View>

          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              About
            </Text>
            <TouchableOpacity
              style={[styles.linkItem, { borderBottomColor: theme.border }]}
              onPress={() => {
                // In a real app, this would navigate to the terms screen
                alert('Would navigate to Terms of Service');
              }}
            >
              <Text style={[styles.linkText, { color: theme.text }]}>
                Terms of Service
              </Text>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.linkItem, { borderBottomColor: theme.border }]}
              onPress={() => {
                // In a real app, this would navigate to the privacy policy screen
                alert('Would navigate to Privacy Policy');
              }}
            >
              <Text style={[styles.linkText, { color: theme.text }]}>
                Privacy Policy
              </Text>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>

            <View style={styles.versionContainer}>
              <Text style={[styles.versionText, { color: theme.text + '99' }]}>
                Version 1.0.0
              </Text>
            </View>
          </View>

          <TouchableOpacity
            style={[styles.logoutButton, { backgroundColor: theme.error }]}
            onPress={handleLogout}
          >
            <Icon name="logout" size={20} color="#FFFFFF" />
            <Text style={styles.logoutButtonText}>Log Out</Text>
          </TouchableOpacity>
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
  section: {
    borderRadius: 12,
    marginBottom: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    padding: 16,
    paddingBottom: 8,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
  },
  settingTextContainer: {
    flex: 1,
    marginRight: 16,
  },
  settingTitle: {
    fontSize: 16,
    marginBottom: 4,
  },
  settingDescription: {
    fontSize: 12,
  },
  riskLevelContainer: {
    flexDirection: 'row',
  },
  riskLevelButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.1)',
    marginLeft: 8,
  },
  riskLevelText: {
    fontSize: 12,
  },
  linkItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
  },
  linkText: {
    fontSize: 16,
  },
  versionContainer: {
    padding: 16,
    alignItems: 'center',
  },
  versionText: {
    fontSize: 14,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    marginTop: 8,
    marginBottom: 20,
  },
  logoutButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default SettingsScreen;
