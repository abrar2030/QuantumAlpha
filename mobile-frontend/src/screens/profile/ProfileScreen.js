import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Image,
  ActivityIndicator,
  Animated,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

const ProfileScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  const { user, updateProfile } = useAuth();
  
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userData, setUserData] = useState({
    name: user?.name || 'Demo User',
    email: user?.email || 'demo@example.com',
    phone: user?.phone || '+1 (555) 123-4567',
    location: user?.location || 'New York, USA',
    bio: user?.bio || 'Algorithmic trader with 5+ years of experience in quantitative finance.',
  });
  
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
  
  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      await updateProfile(userData);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      // In a real app, you would handle errors appropriately
    } finally {
      setLoading(false);
    }
  };
  
  const renderProfileField = (label, value, field) => {
    return (
      <View style={styles.fieldContainer}>
        <Text style={[styles.fieldLabel, { color: theme.text + 'CC' }]}>{label}</Text>
        {isEditing ? (
          <TextInput
            style={[
              styles.fieldInput,
              { color: theme.text, borderColor: theme.border },
            ]}
            value={value}
            onChangeText={(text) => setUserData({ ...userData, [field]: text })}
          />
        ) : (
          <Text style={[styles.fieldValue, { color: theme.text }]}>{value}</Text>
        )}
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
        <Text style={[styles.headerTitle, { color: theme.text }]}>Profile</Text>
        <TouchableOpacity
          style={styles.editButton}
          onPress={() => {
            if (isEditing) {
              handleSaveProfile();
            } else {
              setIsEditing(true);
            }
          }}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator size="small" color={theme.primary} />
          ) : (
            <Text style={[styles.editButtonText, { color: theme.primary }]}>
              {isEditing ? 'Save' : 'Edit'}
            </Text>
          )}
        </TouchableOpacity>
      </Animated.View>
      
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animated.View
          style={{
            opacity: fadeAnim,
            transform: [{ translateY }],
          }}
        >
          <View style={[styles.profileCard, { backgroundColor: theme.card }]}>
            <View style={styles.profileHeader}>
              <View style={styles.avatarContainer}>
                <Image
                  source={require('../../assets/avatar.png')}
                  style={styles.avatar}
                />
                {isEditing && (
                  <TouchableOpacity
                    style={[styles.changeAvatarButton, { backgroundColor: theme.primary }]}
                    onPress={() => {
                      // In a real app, this would open image picker
                      alert('Would open image picker');
                    }}
                  >
                    <Icon name="camera" size={16} color="#FFFFFF" />
                  </TouchableOpacity>
                )}
              </View>
              <View style={styles.profileInfo}>
                <Text style={[styles.profileName, { color: theme.text }]}>
                  {userData.name}
                </Text>
                <Text style={[styles.profileEmail, { color: theme.text + 'CC' }]}>
                  {userData.email}
                </Text>
                <View style={styles.membershipBadge}>
                  <Icon name="star" size={14} color="#FFD700" />
                  <Text style={styles.membershipText}>Premium Member</Text>
                </View>
              </View>
            </View>
            
            <View style={[styles.divider, { backgroundColor: theme.border }]} />
            
            {renderProfileField('Full Name', userData.name, 'name')}
            {renderProfileField('Email', userData.email, 'email')}
            {renderProfileField('Phone', userData.phone, 'phone')}
            {renderProfileField('Location', userData.location, 'location')}
            {renderProfileField('Bio', userData.bio, 'bio')}
          </View>
          
          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Account Statistics
            </Text>
            
            <View style={styles.statsContainer}>
              <View style={styles.statItem}>
                <Text style={[styles.statValue, { color: theme.text }]}>42</Text>
                <Text style={[styles.statLabel, { color: theme.text + 'CC' }]}>
                  Trades
                </Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={[styles.statValue, { color: theme.text }]}>8.3%</Text>
                <Text style={[styles.statLabel, { color: theme.text + 'CC' }]}>
                  Return
                </Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={[styles.statValue, { color: theme.text }]}>5</Text>
                <Text style={[styles.statLabel, { color: theme.text + 'CC' }]}>
                  Strategies
                </Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={[styles.statValue, { color: theme.text }]}>68%</Text>
                <Text style={[styles.statLabel, { color: theme.text + 'CC' }]}>
                  Win Rate
                </Text>
              </View>
            </View>
          </View>
          
          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Account Security
            </Text>
            
            <TouchableOpacity
              style={[styles.securityItem, { borderBottomColor: theme.border }]}
              onPress={() => {
                // In a real app, this would navigate to change password screen
                alert('Would navigate to change password screen');
              }}
            >
              <View style={styles.securityItemContent}>
                <Icon name="lock" size={24} color={theme.primary} />
                <View style={styles.securityItemText}>
                  <Text style={[styles.securityItemTitle, { color: theme.text }]}>
                    Change Password
                  </Text>
                  <Text style={[styles.securityItemDescription, { color: theme.text + 'CC' }]}>
                    Last changed 30 days ago
                  </Text>
                </View>
              </View>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.securityItem, { borderBottomColor: theme.border }]}
              onPress={() => {
                // In a real app, this would navigate to 2FA setup screen
                alert('Would navigate to 2FA setup screen');
              }}
            >
              <View style={styles.securityItemContent}>
                <Icon name="shield-check" size={24} color={theme.primary} />
                <View style={styles.securityItemText}>
                  <Text style={[styles.securityItemTitle, { color: theme.text }]}>
                    Two-Factor Authentication
                  </Text>
                  <Text style={[styles.securityItemDescription, { color: theme.text + 'CC' }]}>
                    Enabled
                  </Text>
                </View>
              </View>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.securityItem}
              onPress={() => {
                // In a real app, this would navigate to device management screen
                alert('Would navigate to device management screen');
              }}
            >
              <View style={styles.securityItemContent}>
                <Icon name="devices" size={24} color={theme.primary} />
                <View style={styles.securityItemText}>
                  <Text style={[styles.securityItemTitle, { color: theme.text }]}>
                    Manage Devices
                  </Text>
                  <Text style={[styles.securityItemDescription, { color: theme.text + 'CC' }]}>
                    2 active devices
                  </Text>
                </View>
              </View>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>
          </View>
          
          <View style={[styles.section, { backgroundColor: theme.card }]}>
            <Text style={[styles.sectionTitle, { color: theme.text }]}>
              Preferences
            </Text>
            
            <TouchableOpacity
              style={styles.preferenceItem}
              onPress={() => {
                navigation.navigate('SettingsScreen');
              }}
            >
              <View style={styles.preferenceItemContent}>
                <Icon name="cog" size={24} color={theme.primary} />
                <Text style={[styles.preferenceItemTitle, { color: theme.text }]}>
                  Settings
                </Text>
              </View>
              <Icon name="chevron-right" size={20} color={theme.text + '99'} />
            </TouchableOpacity>
          </View>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  editButton: {
    padding: 8,
  },
  editButtonText: {
    fontSize: 16,
    fontWeight: '500',
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  profileCard: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  profileHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarContainer: {
    position: 'relative',
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
  },
  changeAvatarButton: {
    position: 'absolute',
    right: 0,
    bottom: 0,
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
  },
  profileInfo: {
    marginLeft: 16,
    flex: 1,
  },
  profileName: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  profileEmail: {
    fontSize: 14,
    marginTop: 2,
  },
  membershipBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 215, 0, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginTop: 8,
  },
  membershipText: {
    fontSize: 12,
    color: '#FFD700',
    marginLeft: 4,
    fontWeight: '500',
  },
  divider: {
    height: 1,
    marginVertical: 16,
  },
  fieldContainer: {
    marginBottom: 16,
  },
  fieldLabel: {
    fontSize: 12,
    marginBottom: 4,
  },
  fieldValue: {
    fontSize: 16,
  },
  fieldInput: {
    fontSize: 16,
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 8,
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
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 16,
    paddingTop: 8,
  },
  statItem: {
    width: '50%',
    paddingVertical: 8,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  statLabel: {
    fontSize: 12,
    marginTop: 2,
  },
  securityItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
  },
  securityItemContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  securityItemText: {
    marginLeft: 16,
    flex: 1,
  },
  securityItemTitle: {
    fontSize: 16,
  },
  securityItemDescription: {
    fontSize: 12,
    marginTop: 2,
  },
  preferenceItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
  },
  preferenceItemContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  preferenceItemTitle: {
    fontSize: 16,
    marginLeft: 16,
  },
});

export default ProfileScreen;
