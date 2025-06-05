import React, { createContext, useState, useContext } from 'react';
import { useColorScheme } from 'react-native';

// Define theme colors
const lightTheme = {
  primary: '#1aff92',
  secondary: '#0066cc',
  background: '#f8f9fa',
  card: '#ffffff',
  text: '#121212',
  border: '#e1e1e1',
  notification: '#ff3b30',
  error: '#ff4d4d',
  success: '#34c759',
  warning: '#ffcc00',
  info: '#0066cc',
  chartBackground: '#ffffff',
  chartBackgroundGradientFrom: '#ffffff',
  chartBackgroundGradientTo: '#f8f9fa',
};

const darkTheme = {
  primary: '#1aff92',
  secondary: '#0a84ff',
  background: '#121212',
  card: '#1e1e1e',
  text: '#ffffff',
  border: '#2c2c2c',
  notification: '#ff453a',
  error: '#ff4d4d',
  success: '#32d74b',
  warning: '#ffd60a',
  info: '#0a84ff',
  chartBackground: '#1e1e1e',
  chartBackgroundGradientFrom: '#1e1e1e',
  chartBackgroundGradientTo: '#1e1e1e',
};

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
  const deviceTheme = useColorScheme();
  const [isDarkMode, setIsDarkMode] = useState(deviceTheme === 'dark');
  
  const theme = isDarkMode ? darkTheme : lightTheme;
  
  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };
  
  return (
    <ThemeContext.Provider
      value={{
        theme,
        isDarkMode,
        toggleTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};
