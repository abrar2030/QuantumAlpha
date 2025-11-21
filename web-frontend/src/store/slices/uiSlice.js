import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  drawerOpen: false,
  darkMode: true,
  notifications: [],
  currentView: "dashboard",
  loading: {
    global: false,
    portfolio: false,
    strategies: false,
    trades: false,
  },
  errors: {
    global: null,
    portfolio: null,
    strategies: null,
    trades: null,
  },
  modals: {
    settings: false,
    createStrategy: false,
    strategyDetails: false,
    deposit: false,
    withdraw: false,
  },
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleDrawer: (state) => {
      state.drawerOpen = !state.drawerOpen;
    },
    setDrawerOpen: (state, action) => {
      state.drawerOpen = action.payload;
    },
    toggleDarkMode: (state) => {
      state.darkMode = !state.darkMode;
    },
    setDarkMode: (state, action) => {
      state.darkMode = action.payload;
    },
    addNotification: (state, action) => {
      state.notifications.push({
        id: Date.now(),
        ...action.payload,
      });
    },
    removeNotification: (state, action) => {
      state.notifications = state.notifications.filter(
        (notification) => notification.id !== action.payload,
      );
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    setCurrentView: (state, action) => {
      state.currentView = action.payload;
    },
    setLoading: (state, action) => {
      const { key, value } = action.payload;
      state.loading[key] = value;
    },
    setError: (state, action) => {
      const { key, value } = action.payload;
      state.errors[key] = value;
    },
    clearErrors: (state) => {
      Object.keys(state.errors).forEach((key) => {
        state.errors[key] = null;
      });
    },
    toggleModal: (state, action) => {
      const { modal, value } = action.payload;
      state.modals[modal] = value !== undefined ? value : !state.modals[modal];
    },
  },
});

export const {
  toggleDrawer,
  setDrawerOpen,
  toggleDarkMode,
  setDarkMode,
  addNotification,
  removeNotification,
  clearNotifications,
  setCurrentView,
  setLoading,
  setError,
  clearErrors,
  toggleModal,
} = uiSlice.actions;

export default uiSlice.reducer;
