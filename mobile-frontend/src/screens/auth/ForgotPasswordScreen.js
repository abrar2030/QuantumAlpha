import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Image,
  KeyboardAvoidingView,
  Platform,
  Animated,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useTheme } from '../../context/ThemeContext';

const ForgotPasswordScreen = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [step, setStep] = useState('email'); // 'email', 'code', 'newPassword'
  const [verificationCode, setVerificationCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  // Animation values
  const fadeAnim = new Animated.Value(0);
  const slideAnim = new Animated.Value(0);
  
  React.useEffect(() => {
    // Start animations when component mounts
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);
  
  const validateEmail = (email) => {
    return /\S+@\S+\.\S+/.test(email);
  };
  
  const handleSendResetCode = async () => {
    if (!email.trim()) {
      setError('Email address is required');
      return;
    }
    
    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    try {
      setLoading(true);
      setError('');
      
      // Simulate API call to send reset code
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // In a real app, this would make an API call to send the reset code
      console.log('Sending password reset code to:', email);
      
      setStep('code');
      setSuccess(true);
    } catch (err) {
      setError('Failed to send reset code. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleVerifyCode = async () => {
    if (!verificationCode.trim()) {
      setError('Verification code is required');
      return;
    }
    
    if (verificationCode.length !== 6) {
      setError('Please enter the complete 6-digit code');
      return;
    }
    
    try {
      setLoading(true);
      setError('');
      
      // Simulate API call to verify code
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // In a real app, this would verify the code with the backend
      console.log('Verifying code:', verificationCode);
      
      setStep('newPassword');
    } catch (err) {
      setError('Invalid verification code. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleResetPassword = async () => {
    if (!newPassword) {
      setError('New password is required');
      return;
    }
    
    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    try {
      setLoading(true);
      setError('');
      
      // Simulate API call to reset password
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // In a real app, this would reset the password via API
      console.log('Resetting password for:', email);
      
      // Show success and navigate back to login
      alert('Password reset successfully! You can now log in with your new password.');
      navigation.navigate('Login');
    } catch (err) {
      setError('Failed to reset password. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleResendCode = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Simulate API call to resend code
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      alert('Verification code sent again!');
    } catch (err) {
      setError('Failed to resend code. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const renderEmailStep = () => (
    <Animated.View
      style={[
        styles.stepContainer,
        {
          opacity: fadeAnim,
          transform: [
            {
              translateY: slideAnim.interpolate({
                inputRange: [0, 1],
                outputRange: [50, 0],
              }),
            },
          ],
        },
      ]}
    >
      <View style={styles.iconContainer}>
        <Icon name="email-outline" size={60} color={theme.primary} />
      </View>
      
      <Text style={[styles.title, { color: theme.text }]}>
        Reset Password
      </Text>
      
      <Text style={[styles.subtitle, { color: theme.text + 'CC' }]}>
        Enter your email address and we'll send you a verification code to reset your password.
      </Text>
      
      {error ? (
        <View style={styles.errorContainer}>
          <Icon name="alert-circle" size={20} color={theme.error} />
          <Text style={[styles.errorText, { color: theme.error }]}>{error}</Text>
        </View>
      ) : null}
      
      <View style={styles.inputGroup}>
        <Icon name="email" size={20} color={theme.text} style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="Enter your email address"
          placeholderTextColor={theme.text + '80'}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          editable={!loading}
        />
      </View>
      
      <TouchableOpacity
        style={[
          styles.primaryButton,
          { backgroundColor: theme.primary },
          loading && styles.disabledButton
        ]}
        onPress={handleSendResetCode}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#ffffff" size="small" />
        ) : (
          <Text style={styles.primaryButtonText}>Send Reset Code</Text>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
  
  const renderCodeStep = () => (
    <Animated.View
      style={[
        styles.stepContainer,
        {
          opacity: fadeAnim,
          transform: [
            {
              translateY: slideAnim.interpolate({
                inputRange: [0, 1],
                outputRange: [50, 0],
              }),
            },
          ],
        },
      ]}
    >
      <View style={styles.iconContainer}>
        <Icon name="shield-check-outline" size={60} color={theme.success} />
      </View>
      
      <Text style={[styles.title, { color: theme.text }]}>
        Check Your Email
      </Text>
      
      <Text style={[styles.subtitle, { color: theme.text + 'CC' }]}>
        We've sent a 6-digit verification code to{'\n'}
        <Text style={{ fontWeight: 'bold' }}>{email}</Text>
      </Text>
      
      {error ? (
        <View style={styles.errorContainer}>
          <Icon name="alert-circle" size={20} color={theme.error} />
          <Text style={[styles.errorText, { color: theme.error }]}>{error}</Text>
        </View>
      ) : null}
      
      <View style={styles.inputGroup}>
        <Icon name="lock-outline" size={20} color={theme.text} style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="Enter 6-digit code"
          placeholderTextColor={theme.text + '80'}
          value={verificationCode}
          onChangeText={setVerificationCode}
          keyboardType="number-pad"
          maxLength={6}
          editable={!loading}
        />
      </View>
      
      <TouchableOpacity
        style={[
          styles.primaryButton,
          { backgroundColor: theme.primary },
          loading && styles.disabledButton
        ]}
        onPress={handleVerifyCode}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#ffffff" size="small" />
        ) : (
          <Text style={styles.primaryButtonText}>Verify Code</Text>
        )}
      </TouchableOpacity>
      
      <View style={styles.resendContainer}>
        <Text style={[styles.resendText, { color: theme.text + 'CC' }]}>
          Didn't receive the code?
        </Text>
        <TouchableOpacity onPress={handleResendCode} disabled={loading}>
          <Text style={[styles.resendLink, { color: theme.primary }]}>
            Resend Code
          </Text>
        </TouchableOpacity>
      </View>
    </Animated.View>
  );
  
  const renderNewPasswordStep = () => (
    <Animated.View
      style={[
        styles.stepContainer,
        {
          opacity: fadeAnim,
          transform: [
            {
              translateY: slideAnim.interpolate({
                inputRange: [0, 1],
                outputRange: [50, 0],
              }),
            },
          ],
        },
      ]}
    >
      <View style={styles.iconContainer}>
        <Icon name="lock-reset" size={60} color={theme.primary} />
      </View>
      
      <Text style={[styles.title, { color: theme.text }]}>
        Create New Password
      </Text>
      
      <Text style={[styles.subtitle, { color: theme.text + 'CC' }]}>
        Your new password must be different from your previous password.
      </Text>
      
      {error ? (
        <View style={styles.errorContainer}>
          <Icon name="alert-circle" size={20} color={theme.error} />
          <Text style={[styles.errorText, { color: theme.error }]}>{error}</Text>
        </View>
      ) : null}
      
      <View style={styles.inputGroup}>
        <Icon name="lock" size={20} color={theme.text} style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="New Password"
          placeholderTextColor={theme.text + '80'}
          value={newPassword}
          onChangeText={setNewPassword}
          secureTextEntry={!showPassword}
          editable={!loading}
        />
        <TouchableOpacity
          style={styles.passwordToggle}
          onPress={() => setShowPassword(!showPassword)}
        >
          <Icon
            name={showPassword ? 'eye-off' : 'eye'}
            size={20}
            color={theme.text}
          />
        </TouchableOpacity>
      </View>
      
      <View style={styles.inputGroup}>
        <Icon name="lock-check" size={20} color={theme.text} style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="Confirm New Password"
          placeholderTextColor={theme.text + '80'}
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry={!showConfirmPassword}
          editable={!loading}
        />
        <TouchableOpacity
          style={styles.passwordToggle}
          onPress={() => setShowConfirmPassword(!showConfirmPassword)}
        >
          <Icon
            name={showConfirmPassword ? 'eye-off' : 'eye'}
            size={20}
            color={theme.text}
          />
        </TouchableOpacity>
      </View>
      
      <View style={styles.passwordRequirements}>
        <Text style={[styles.requirementText, { color: theme.text + 'CC' }]}>
          • Password must be at least 8 characters long
        </Text>
        <Text style={[styles.requirementText, { color: theme.text + 'CC' }]}>
          • Include both uppercase and lowercase letters
        </Text>
        <Text style={[styles.requirementText, { color: theme.text + 'CC' }]}>
          • Include at least one number or special character
        </Text>
      </View>
      
      <TouchableOpacity
        style={[
          styles.primaryButton,
          { backgroundColor: theme.primary },
          loading && styles.disabledButton
        ]}
        onPress={handleResetPassword}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#ffffff" size="small" />
        ) : (
          <Text style={styles.primaryButtonText}>Reset Password</Text>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
  
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={[styles.container, { backgroundColor: theme.background }]}
    >
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Icon name="arrow-left" size={24} color={theme.text} />
        </TouchableOpacity>
      </View>
      
      <View style={styles.content}>
        {step === 'email' && renderEmailStep()}
        {step === 'code' && renderCodeStep()}
        {step === 'newPassword' && renderNewPasswordStep()}
      </View>
      
      <View style={styles.footer}>
        <TouchableOpacity
          style={styles.loginButton}
          onPress={() => navigation.navigate('Login')}
        >
          <Text style={[styles.loginButtonText, { color: theme.text }]}>
            Remember your password?{' '}
            <Text style={[styles.linkText, { color: theme.primary }]}>
              Sign In
            </Text>
          </Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 20,
  },
  backButton: {
    padding: 8,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  stepContainer: {
    alignItems: 'center',
    maxWidth: 400,
    alignSelf: 'center',
    width: '100%',
  },
  iconContainer: {
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
    lineHeight: 22,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 0, 0, 0.1)',
    padding: 12,
    borderRadius: 8,
    marginBottom: 20,
    width: '100%',
  },
  errorText: {
    marginLeft: 10,
    fontSize: 14,
    flex: 1,
  },
  inputGroup: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    position: 'relative',
    width: '100%',
  },
  inputIcon: {
    position: 'absolute',
    left: 15,
    zIndex: 1,
  },
  input: {
    flex: 1,
    height: 50,
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 45,
    fontSize: 16,
  },
  passwordToggle: {
    position: 'absolute',
    right: 15,
    zIndex: 1,
  },
  passwordRequirements: {
    alignSelf: 'flex-start',
    marginBottom: 20,
    width: '100%',
  },
  requirementText: {
    fontSize: 12,
    marginBottom: 4,
  },
  primaryButton: {
    height: 50,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    marginBottom: 20,
  },
  disabledButton: {
    opacity: 0.7,
  },
  primaryButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  resendContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  resendText: {
    fontSize: 14,
    marginRight: 5,
  },
  resendLink: {
    fontSize: 14,
    fontWeight: 'bold',
    textDecorationLine: 'underline',
  },
  footer: {
    paddingHorizontal: 20,
    paddingBottom: 30,
  },
  loginButton: {
    alignSelf: 'center',
    padding: 10,
  },
  loginButtonText: {
    fontSize: 14,
    textAlign: 'center',
  },
  linkText: {
    fontWeight: 'bold',
    textDecorationLine: 'underline',
  },
});

export default ForgotPasswordScreen;

