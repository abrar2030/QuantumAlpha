import api from './api';

class AuthService {
  constructor() {
    this.token = null;
  }

  setToken(token) {
    this.token = token;
  }

  async login(email, password) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful login
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              user: {
                id: '12345',
                email,
                name: 'Demo User',
                profileImage: null,
              },
              token: 'demo-token-12345',
              refreshToken: 'demo-refresh-token-12345',
            },
          });
        }, 1000);
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  async register(userData) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful registration
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              user: {
                id: '12345',
                email: userData.email,
                name: userData.name,
                profileImage: null,
              },
              token: 'demo-token-12345',
              refreshToken: 'demo-refresh-token-12345',
            },
          });
        }, 1000);
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  async logout() {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful logout
      await new Promise((resolve) => {
        setTimeout(resolve, 500);
      });

      this.token = null;
      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Logout failed');
    }
  }

  async updateProfile(userData) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful profile update
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              ...userData,
              id: '12345',
            },
          });
        }, 1000);
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Profile update failed');
    }
  }

  async forgotPassword(email) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful password reset request
      await new Promise((resolve) => {
        setTimeout(resolve, 1000);
      });

      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Password reset request failed');
    }
  }

  async resetPassword(token, newPassword) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful password reset
      await new Promise((resolve) => {
        setTimeout(resolve, 1000);
      });

      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Password reset failed');
    }
  }

  async verifyEmail(token) {
    try {
      // In a real app, this would be an API call
      // For demo purposes, we'll simulate a successful email verification
      await new Promise((resolve) => {
        setTimeout(resolve, 1000);
      });

      return true;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Email verification failed');
    }
  }
}

export const authService = new AuthService();
