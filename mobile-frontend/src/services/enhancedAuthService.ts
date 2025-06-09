import AsyncStorage from '@react-native-async-storage/async-storage';
import ReactNativeBiometrics from 'react-native-biometrics';
import DeviceInfo from 'react-native-device-info';
import api from './api';
import { secureStorage } from '../utils';
import { STORAGE_KEYS, ERROR_CODES } from '../constants';
import { 
  User, 
  LoginCredentials, 
  RegisterData, 
  ApiResponse,
  ApiError 
} from '../types';

class EnhancedAuthService {
  private biometrics: ReactNativeBiometrics;
  private deviceId: string | null = null;

  constructor() {
    this.biometrics = new ReactNativeBiometrics({
      allowDeviceCredentials: true,
    });
    this.initializeDeviceId();
  }

  private async initializeDeviceId() {
    try {
      this.deviceId = await DeviceInfo.getUniqueId();
    } catch (error) {
      console.error('Failed to get device ID:', error);
    }
  }

  // Check if biometric authentication is available
  async isBiometricAvailable(): Promise<boolean> {
    try {
      const { available } = await this.biometrics.isSensorAvailable();
      return available;
    } catch (error) {
      console.error('Error checking biometric availability:', error);
      return false;
    }
  }

  // Get available biometric types
  async getBiometricType(): Promise<string | null> {
    try {
      const { biometryType } = await this.biometrics.isSensorAvailable();
      return biometryType;
    } catch (error) {
      console.error('Error getting biometric type:', error);
      return null;
    }
  }

  // Enable biometric authentication
  async enableBiometricAuth(password: string): Promise<boolean> {
    try {
      const isAvailable = await this.isBiometricAvailable();
      if (!isAvailable) {
        throw new Error('Biometric authentication is not available');
      }

      // Create biometric key
      const { keysExist } = await this.biometrics.keysExist();
      if (!keysExist) {
        await this.biometrics.createKeys();
      }

      // Store encrypted credentials
      await secureStorage.setItem(STORAGE_KEYS.BIOMETRIC_ENABLED, 'true');
      await secureStorage.setItem('biometric_password', password);

      return true;
    } catch (error) {
      console.error('Error enabling biometric auth:', error);
      throw new Error(ERROR_CODES.BIOMETRIC_ERROR);
    }
  }

  // Disable biometric authentication
  async disableBiometricAuth(): Promise<void> {
    try {
      await this.biometrics.deleteKeys();
      await secureStorage.removeItem(STORAGE_KEYS.BIOMETRIC_ENABLED);
      await secureStorage.removeItem('biometric_password');
    } catch (error) {
      console.error('Error disabling biometric auth:', error);
    }
  }

  // Authenticate with biometrics
  async authenticateWithBiometrics(): Promise<string> {
    try {
      const isEnabled = await secureStorage.getItem(STORAGE_KEYS.BIOMETRIC_ENABLED);
      if (isEnabled !== 'true') {
        throw new Error('Biometric authentication is not enabled');
      }

      const { success } = await this.biometrics.simplePrompt({
        promptMessage: 'Authenticate to access QuantumAlpha',
        cancelButtonText: 'Cancel',
      });

      if (!success) {
        throw new Error('Biometric authentication failed');
      }

      const password = await secureStorage.getItem('biometric_password');
      if (!password) {
        throw new Error('Stored credentials not found');
      }

      return password;
    } catch (error) {
      console.error('Biometric authentication error:', error);
      throw new Error(ERROR_CODES.BIOMETRIC_ERROR);
    }
  }

  // Login with email and password
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string; refreshToken: string }> {
    try {
      const deviceInfo = await this.getDeviceInfo();
      
      const response = await api.post<ApiResponse<{
        user: User;
        token: string;
        refreshToken: string;
      }>>('/auth/login', {
        ...credentials,
        deviceInfo,
      });

      if (!response.data.success) {
        throw new Error(response.data.message || 'Login failed');
      }

      const { user, token, refreshToken } = response.data.data;

      // Store tokens securely
      await this.storeTokens(token, refreshToken);
      await this.storeUser(user);

      // Set token for API requests
      this.setToken(token);

      return { user, token, refreshToken };
    } catch (error: any) {
      console.error('Login error:', error);
      
      if (error.response?.status === 401) {
        throw new Error(ERROR_CODES.AUTHENTICATION_ERROR);
      } else if (error.response?.status === 429) {
        throw new Error(ERROR_CODES.RATE_LIMIT_EXCEEDED);
      } else if (!error.response) {
        throw new Error(ERROR_CODES.NETWORK_ERROR);
      }
      
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Login with biometrics
  async loginWithBiometrics(): Promise<{ user: User; token: string; refreshToken: string }> {
    try {
      const password = await this.authenticateWithBiometrics();
      const email = await secureStorage.getItem('user_email');
      
      if (!email) {
        throw new Error('User email not found');
      }

      return await this.login({ email, password });
    } catch (error) {
      console.error('Biometric login error:', error);
      throw error;
    }
  }

  // Register new user
  async register(userData: RegisterData): Promise<{ user: User; token: string; refreshToken: string }> {
    try {
      const deviceInfo = await this.getDeviceInfo();
      
      const response = await api.post<ApiResponse<{
        user: User;
        token: string;
        refreshToken: string;
      }>>('/auth/register', {
        ...userData,
        deviceInfo,
      });

      if (!response.data.success) {
        throw new Error(response.data.message || 'Registration failed');
      }

      const { user, token, refreshToken } = response.data.data;

      // Store tokens securely
      await this.storeTokens(token, refreshToken);
      await this.storeUser(user);

      // Set token for API requests
      this.setToken(token);

      return { user, token, refreshToken };
    } catch (error: any) {
      console.error('Registration error:', error);
      
      if (error.response?.status === 409) {
        throw new Error('User already exists');
      } else if (error.response?.status === 400) {
        throw new Error(ERROR_CODES.VALIDATION_ERROR);
      } else if (!error.response) {
        throw new Error(ERROR_CODES.NETWORK_ERROR);
      }
      
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Logout user
  async logout(): Promise<void> {
    try {
      const refreshToken = await secureStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      
      if (refreshToken) {
        await api.post('/auth/logout', { refreshToken });
      }
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      // Clear all stored data
      await this.clearStoredData();
      this.setToken(null);
    }
  }

  // Refresh access token
  async refreshToken(): Promise<string> {
    try {
      const refreshToken = await secureStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.post<ApiResponse<{
        token: string;
        refreshToken: string;
      }>>('/auth/refresh', { refreshToken });

      if (!response.data.success) {
        throw new Error('Token refresh failed');
      }

      const { token: newToken, refreshToken: newRefreshToken } = response.data.data;

      // Store new tokens
      await this.storeTokens(newToken, newRefreshToken);
      this.setToken(newToken);

      return newToken;
    } catch (error) {
      console.error('Token refresh error:', error);
      // If refresh fails, logout user
      await this.logout();
      throw new Error(ERROR_CODES.AUTHENTICATION_ERROR);
    }
  }

  // Forgot password
  async forgotPassword(email: string): Promise<void> {
    try {
      const response = await api.post<ApiResponse<void>>('/auth/forgot-password', { email });
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Failed to send reset email');
      }
    } catch (error: any) {
      console.error('Forgot password error:', error);
      
      if (error.response?.status === 404) {
        throw new Error('Email not found');
      } else if (!error.response) {
        throw new Error(ERROR_CODES.NETWORK_ERROR);
      }
      
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Reset password
  async resetPassword(token: string, newPassword: string): Promise<void> {
    try {
      const response = await api.post<ApiResponse<void>>('/auth/reset-password', {
        token,
        password: newPassword,
      });
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Password reset failed');
      }
    } catch (error: any) {
      console.error('Reset password error:', error);
      
      if (error.response?.status === 400) {
        throw new Error('Invalid or expired reset token');
      } else if (!error.response) {
        throw new Error(ERROR_CODES.NETWORK_ERROR);
      }
      
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Update user profile
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response = await api.put<ApiResponse<User>>('/auth/profile', userData);
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Profile update failed');
      }

      const updatedUser = response.data.data;
      await this.storeUser(updatedUser);

      return updatedUser;
    } catch (error: any) {
      console.error('Profile update error:', error);
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Change password
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      const response = await api.post<ApiResponse<void>>('/auth/change-password', {
        currentPassword,
        newPassword,
      });
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Password change failed');
      }
    } catch (error: any) {
      console.error('Change password error:', error);
      
      if (error.response?.status === 400) {
        throw new Error('Current password is incorrect');
      }
      
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Verify email
  async verifyEmail(token: string): Promise<void> {
    try {
      const response = await api.post<ApiResponse<void>>('/auth/verify-email', { token });
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Email verification failed');
      }
    } catch (error: any) {
      console.error('Email verification error:', error);
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Enable/disable two-factor authentication
  async toggleTwoFactor(enable: boolean, code?: string): Promise<{ qrCode?: string; backupCodes?: string[] }> {
    try {
      const response = await api.post<ApiResponse<{
        qrCode?: string;
        backupCodes?: string[];
      }>>('/auth/two-factor', { enable, code });
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'Two-factor authentication setup failed');
      }

      return response.data.data;
    } catch (error: any) {
      console.error('Two-factor auth error:', error);
      throw new Error(error.message || ERROR_CODES.UNKNOWN_ERROR);
    }
  }

  // Helper methods
  private async getDeviceInfo() {
    return {
      deviceId: this.deviceId,
      platform: await DeviceInfo.getSystemName(),
      version: await DeviceInfo.getSystemVersion(),
      model: await DeviceInfo.getModel(),
      brand: await DeviceInfo.getBrand(),
      appVersion: await DeviceInfo.getVersion(),
      buildNumber: await DeviceInfo.getBuildNumber(),
    };
  }

  private async storeTokens(token: string, refreshToken: string): Promise<void> {
    await secureStorage.setItem(STORAGE_KEYS.USER_TOKEN, token);
    await secureStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
  }

  private async storeUser(user: User): Promise<void> {
    await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
    await secureStorage.setItem('user_email', user.email);
  }

  private async clearStoredData(): Promise<void> {
    await secureStorage.removeItem(STORAGE_KEYS.USER_TOKEN);
    await secureStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    await AsyncStorage.removeItem(STORAGE_KEYS.USER_DATA);
    await secureStorage.removeItem('user_email');
  }

  setToken(token: string | null): void {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete api.defaults.headers.common['Authorization'];
    }
  }

  async getStoredToken(): Promise<string | null> {
    return await secureStorage.getItem(STORAGE_KEYS.USER_TOKEN);
  }

  async getStoredUser(): Promise<User | null> {
    try {
      const userJson = await AsyncStorage.getItem(STORAGE_KEYS.USER_DATA);
      return userJson ? JSON.parse(userJson) : null;
    } catch (error) {
      console.error('Error getting stored user:', error);
      return null;
    }
  }
}

export const enhancedAuthService = new EnhancedAuthService();
export default enhancedAuthService;

