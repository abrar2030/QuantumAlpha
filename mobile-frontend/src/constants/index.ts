// API Configuration
export const API_CONFIG = {
  BASE_URL: __DEV__ 
    ? 'https://api-dev.quantumalpha.com/v1' 
    : 'https://api.quantumalpha.com/v1',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
};

// WebSocket Configuration
export const WS_CONFIG = {
  URL: __DEV__ 
    ? 'wss://ws-dev.quantumalpha.com' 
    : 'wss://ws.quantumalpha.com',
  RECONNECT_INTERVAL: 5000,
  MAX_RECONNECT_ATTEMPTS: 5,
  HEARTBEAT_INTERVAL: 30000,
};

// App Configuration
export const APP_CONFIG = {
  NAME: 'QuantumAlpha',
  VERSION: '2.0.0',
  BUILD_NUMBER: '1',
  BUNDLE_ID: 'com.quantumalpha.mobile',
  DEEP_LINK_SCHEME: 'quantumalpha',
  SUPPORT_EMAIL: 'support@quantumalpha.com',
  PRIVACY_POLICY_URL: 'https://quantumalpha.com/privacy',
  TERMS_OF_SERVICE_URL: 'https://quantumalpha.com/terms',
};

// Storage Keys
export const STORAGE_KEYS = {
  USER_TOKEN: 'user_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  THEME_PREFERENCE: 'theme_preference',
  BIOMETRIC_ENABLED: 'biometric_enabled',
  NOTIFICATIONS_ENABLED: 'notifications_enabled',
  LANGUAGE_PREFERENCE: 'language_preference',
  ONBOARDING_COMPLETED: 'onboarding_completed',
  PORTFOLIO_CACHE: 'portfolio_cache',
  MARKET_DATA_CACHE: 'market_data_cache',
};

// Navigation Routes
export const ROUTES = {
  // Auth Stack
  LOGIN: 'Login',
  REGISTER: 'Register',
  FORGOT_PASSWORD: 'ForgotPassword',
  VERIFY_EMAIL: 'VerifyEmail',
  RESET_PASSWORD: 'ResetPassword',
  
  // Main Stack
  DASHBOARD: 'Dashboard',
  PORTFOLIO: 'Portfolio',
  STRATEGIES: 'Strategies',
  STRATEGY_DETAIL: 'StrategyDetail',
  TRADE: 'Trade',
  ALERTS: 'Alerts',
  PROFILE: 'Profile',
  SETTINGS: 'Settings',
  NOTIFICATIONS: 'Notifications',
  HELP: 'Help',
  
  // Additional Screens
  MARKET_OVERVIEW: 'MarketOverview',
  ASSET_DETAIL: 'AssetDetail',
  TRANSACTION_HISTORY: 'TransactionHistory',
  RISK_ANALYSIS: 'RiskAnalysis',
  NEWS: 'News',
  EDUCATION: 'Education',
  SOCIAL_TRADING: 'SocialTrading',
  WATCHLIST: 'Watchlist',
  SCANNER: 'Scanner',
  CALCULATOR: 'Calculator',
};

// Theme Colors
export const COLORS = {
  PRIMARY: '#1aff92',
  SECONDARY: '#0066cc',
  SUCCESS: '#34c759',
  WARNING: '#ffcc00',
  ERROR: '#ff4d4d',
  INFO: '#0066cc',
  
  // Light Theme
  LIGHT: {
    BACKGROUND: '#f8f9fa',
    SURFACE: '#ffffff',
    TEXT_PRIMARY: '#121212',
    TEXT_SECONDARY: '#666666',
    BORDER: '#e1e1e1',
    SHADOW: '#000000',
  },
  
  // Dark Theme
  DARK: {
    BACKGROUND: '#121212',
    SURFACE: '#1e1e1e',
    TEXT_PRIMARY: '#ffffff',
    TEXT_SECONDARY: '#cccccc',
    BORDER: '#2c2c2c',
    SHADOW: '#000000',
  },
  
  // Chart Colors
  CHART: {
    POSITIVE: '#34c759',
    NEGATIVE: '#ff453a',
    NEUTRAL: '#8e8e93',
    VOLUME: '#007aff',
    MA_SHORT: '#ff9500',
    MA_LONG: '#af52de',
    RSI: '#5856d6',
    MACD: '#ff2d92',
  },
};

// Typography
export const TYPOGRAPHY = {
  FONT_FAMILY: {
    REGULAR: 'System',
    MEDIUM: 'System',
    BOLD: 'System',
    LIGHT: 'System',
  },
  
  FONT_SIZE: {
    XS: 10,
    SM: 12,
    MD: 14,
    LG: 16,
    XL: 18,
    XXL: 20,
    XXXL: 24,
    TITLE: 28,
    HEADING: 32,
  },
  
  LINE_HEIGHT: {
    XS: 14,
    SM: 16,
    MD: 20,
    LG: 24,
    XL: 28,
    XXL: 32,
    XXXL: 36,
    TITLE: 40,
    HEADING: 44,
  },
};

// Spacing
export const SPACING = {
  XS: 4,
  SM: 8,
  MD: 16,
  LG: 24,
  XL: 32,
  XXL: 48,
  XXXL: 64,
};

// Border Radius
export const BORDER_RADIUS = {
  SM: 4,
  MD: 8,
  LG: 12,
  XL: 16,
  XXL: 24,
  ROUND: 50,
};

// Animation Durations
export const ANIMATION = {
  FAST: 200,
  NORMAL: 300,
  SLOW: 500,
  VERY_SLOW: 1000,
};

// Market Data
export const MARKET_CONFIG = {
  UPDATE_INTERVAL: 5000, // 5 seconds
  CHART_INTERVALS: ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'],
  DEFAULT_INTERVAL: '1h',
  MAX_WATCHLIST_ITEMS: 50,
  POPULAR_ASSETS: ['BTC', 'ETH', 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA'],
};

// Trading Configuration
export const TRADING_CONFIG = {
  MIN_ORDER_AMOUNT: 10,
  MAX_ORDER_AMOUNT: 1000000,
  DEFAULT_LEVERAGE: 1,
  MAX_LEVERAGE: 100,
  STOP_LOSS_RANGE: [0.01, 0.5], // 1% to 50%
  TAKE_PROFIT_RANGE: [0.01, 10], // 1% to 1000%
  ORDER_TYPES: ['market', 'limit', 'stop', 'stop_limit'],
  TIME_IN_FORCE: ['GTC', 'IOC', 'FOK', 'DAY'],
};

// Notification Types
export const NOTIFICATION_TYPES = {
  PRICE_ALERT: 'price_alert',
  TRADE_EXECUTED: 'trade_executed',
  STRATEGY_UPDATE: 'strategy_update',
  PORTFOLIO_UPDATE: 'portfolio_update',
  NEWS_UPDATE: 'news_update',
  SYSTEM_MAINTENANCE: 'system_maintenance',
  SECURITY_ALERT: 'security_alert',
  PROMOTION: 'promotion',
};

// Error Codes
export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTHENTICATION_ERROR: 'AUTHENTICATION_ERROR',
  AUTHORIZATION_ERROR: 'AUTHORIZATION_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR',
  BIOMETRIC_ERROR: 'BIOMETRIC_ERROR',
  INSUFFICIENT_FUNDS: 'INSUFFICIENT_FUNDS',
  MARKET_CLOSED: 'MARKET_CLOSED',
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
};

// Feature Flags
export const FEATURE_FLAGS = {
  BIOMETRIC_AUTH: true,
  SOCIAL_TRADING: true,
  ADVANCED_CHARTS: true,
  NEWS_FEED: true,
  PUSH_NOTIFICATIONS: true,
  DARK_MODE: true,
  OFFLINE_MODE: false,
  BETA_FEATURES: __DEV__,
  ANALYTICS: !__DEV__,
  CRASH_REPORTING: !__DEV__,
};

// Regex Patterns
export const REGEX_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^\+?[\d\s\-\(\)]+$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
  USERNAME: /^[a-zA-Z0-9_]{3,20}$/,
  NUMERIC: /^\d+$/,
  DECIMAL: /^\d+\.?\d*$/,
  ALPHANUMERIC: /^[a-zA-Z0-9]+$/,
};

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  DISPLAY_WITH_TIME: 'MMM dd, yyyy HH:mm',
  ISO: "yyyy-MM-dd'T'HH:mm:ss.SSSxxx",
  SHORT: 'MM/dd/yyyy',
  LONG: 'MMMM dd, yyyy',
  TIME_ONLY: 'HH:mm',
  TIME_WITH_SECONDS: 'HH:mm:ss',
};

// Chart Configuration
export const CHART_CONFIG = {
  DEFAULT_HEIGHT: 220,
  COLORS: {
    POSITIVE: '#34c759',
    NEGATIVE: '#ff453a',
    NEUTRAL: '#8e8e93',
    GRID: '#e1e1e1',
    AXIS: '#666666',
  },
  ANIMATION_DURATION: 1000,
  REFRESH_INTERVAL: 30000, // 30 seconds
};

