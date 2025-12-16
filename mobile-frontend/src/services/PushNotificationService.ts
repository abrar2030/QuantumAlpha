import messaging, {
  FirebaseMessagingTypes,
} from "@react-native-firebase/messaging";
import { Platform, PermissionsAndroid, Alert } from "react-native";
import PushNotification, { Importance } from "react-native-push-notification";
import AsyncStorage from "@react-native-async-storage/async-storage";

const DEVICE_TOKEN_KEY = "@device_push_token";
const NOTIFICATION_PERMISSION_KEY = "@notification_permission_requested";

/**
 * Configure local push notifications
 */
export const configurePushNotifications = (): void => {
  PushNotification.configure({
    // Called when a remote or local notification is opened or received
    onNotification: function (notification) {
      console.log("NOTIFICATION:", notification);

      // Handle notification tap
      if (notification.userInteraction) {
        handleNotificationTap(notification);
      }
    },

    // Called when the user fails to register for remote notifications
    onRegistrationError: function (err) {
      console.error("Push notification registration error:", err.message, err);
    },

    // IOS ONLY: called when a remote notification is received while app is in foreground
    onAction: function (notification) {
      console.log("NOTIFICATION ACTION:", notification.action);
    },

    // Should the initial notification be popped automatically
    popInitialNotification: true,

    // Permission request
    requestPermissions: Platform.OS === "ios",
  });

  // Create default notification channels for Android
  if (Platform.OS === "android") {
    createNotificationChannels();
  }
};

/**
 * Create notification channels for Android
 */
const createNotificationChannels = (): void => {
  PushNotification.createChannel(
    {
      channelId: "default-channel",
      channelName: "Default Notifications",
      channelDescription: "Default notification channel",
      playSound: true,
      soundName: "default",
      importance: Importance.HIGH,
      vibrate: true,
    },
    (created) => console.log(`Default channel created: ${created}`),
  );

  PushNotification.createChannel(
    {
      channelId: "alerts-channel",
      channelName: "Trading Alerts",
      channelDescription: "Important trading alerts and price notifications",
      playSound: true,
      soundName: "default",
      importance: Importance.HIGH,
      vibrate: true,
    },
    (created) => console.log(`Alerts channel created: ${created}`),
  );

  PushNotification.createChannel(
    {
      channelId: "updates-channel",
      channelName: "Updates",
      channelDescription: "General updates and news",
      playSound: false,
      importance: Importance.DEFAULT,
      vibrate: false,
    },
    (created) => console.log(`Updates channel created: ${created}`),
  );
};

/**
 * Request notification permissions
 */
export const requestNotificationPermissions = async (): Promise<{
  success: boolean;
  token?: string;
  error?: string;
}> => {
  try {
    // Check if we've already requested permission
    const alreadyRequested = await AsyncStorage.getItem(
      NOTIFICATION_PERMISSION_KEY,
    );

    if (Platform.OS === "android") {
      if (Platform.Version >= 33) {
        // Android 13+ requires runtime permission
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
        );

        if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
          console.log("Notification permission denied");
          return { success: false, error: "Permission denied" };
        }
      }
    } else if (Platform.OS === "ios") {
      const authStatus = await messaging().requestPermission();
      const enabled =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL;

      if (!enabled) {
        console.log("Notification permission denied on iOS");
        return { success: false, error: "Permission denied" };
      }
    }

    // Mark that we've requested permission
    await AsyncStorage.setItem(NOTIFICATION_PERMISSION_KEY, "true");

    // Get the device token
    const token = await getDeviceToken();
    return { success: true, token };
  } catch (error) {
    console.error("Error requesting notification permissions:", error);
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Permission request error",
    };
  }
};

/**
 * Register for push notifications and get device token
 */
export const registerForPushNotifications = async (): Promise<
  string | null
> => {
  try {
    // Request permissions
    const permissionResult = await requestNotificationPermissions();

    if (!permissionResult.success) {
      console.log("Failed to get notification permissions");
      return null;
    }

    // Get and store the device token
    const token = await getDeviceToken();

    if (token) {
      await AsyncStorage.setItem(DEVICE_TOKEN_KEY, token);
      console.log("Device token registered:", token);
      return token;
    }

    return null;
  } catch (error) {
    console.error("Error registering for push notifications:", error);
    return null;
  }
};

/**
 * Get the device FCM token
 */
export const getDeviceToken = async (): Promise<string | null> => {
  try {
    // Check if we have a cached token
    const cachedToken = await AsyncStorage.getItem(DEVICE_TOKEN_KEY);

    if (cachedToken) {
      console.log("Using cached device token");
      return cachedToken;
    }

    // Register the device with Firebase
    await messaging().registerDeviceForRemoteMessages();

    // Get the token
    const token = await messaging().getToken();

    if (token) {
      await AsyncStorage.setItem(DEVICE_TOKEN_KEY, token);
      console.log("New device token obtained:", token);
      return token;
    }

    return null;
  } catch (error) {
    console.error("Error getting device token:", error);
    return null;
  }
};

/**
 * Delete the device token (unregister from push notifications)
 */
export const deleteDeviceToken = async (): Promise<boolean> => {
  try {
    await messaging().deleteToken();
    await AsyncStorage.removeItem(DEVICE_TOKEN_KEY);
    console.log("Device token deleted");
    return true;
  } catch (error) {
    console.error("Error deleting device token:", error);
    return false;
  }
};

/**
 * Show a local notification
 */
export const showLocalNotification = (
  title: string,
  message: string,
  data?: any,
  channelId: string = "default-channel",
): void => {
  PushNotification.localNotification({
    channelId,
    title,
    message,
    playSound: true,
    soundName: "default",
    userInfo: data,
    vibrate: true,
    vibration: 300,
  });
};

/**
 * Schedule a local notification
 */
export const scheduleLocalNotification = (
  title: string,
  message: string,
  date: Date,
  data?: any,
  channelId: string = "default-channel",
): void => {
  PushNotification.localNotificationSchedule({
    channelId,
    title,
    message,
    date,
    playSound: true,
    soundName: "default",
    userInfo: data,
    vibrate: true,
    vibration: 300,
    allowWhileIdle: true,
  });
};

/**
 * Cancel all local notifications
 */
export const cancelAllLocalNotifications = (): void => {
  PushNotification.cancelAllLocalNotifications();
  console.log("All local notifications cancelled");
};

/**
 * Handle notification tap
 */
const handleNotificationTap = (notification: any): void => {
  console.log("Notification tapped:", notification);

  // Here you can navigate to specific screens based on notification data
  // This will typically be handled by your navigation setup
  if (notification.data) {
    const { type, screen, params } = notification.data;
    // Navigation logic would go here
    console.log("Navigate to:", { type, screen, params });
  }
};

/**
 * Set up foreground notification handler
 */
export const setupForegroundNotificationHandler = (
  onNotification: (remoteMessage: FirebaseMessagingTypes.RemoteMessage) => void,
): (() => void) => {
  return messaging().onMessage(async (remoteMessage) => {
    console.log("Foreground notification received:", remoteMessage);

    // Show a local notification when app is in foreground
    if (remoteMessage.notification) {
      showLocalNotification(
        remoteMessage.notification.title || "Notification",
        remoteMessage.notification.body || "",
        remoteMessage.data,
        "alerts-channel",
      );
    }

    // Call custom handler
    onNotification(remoteMessage);
  });
};

/**
 * Set up background notification handler
 */
export const setupBackgroundNotificationHandler = (): void => {
  messaging().setBackgroundMessageHandler(async (remoteMessage) => {
    console.log("Background notification received:", remoteMessage);

    // Process the notification in the background
    // You can update local storage, trigger background tasks, etc.
  });
};

/**
 * Handle notification opened from quit state
 */
export const getInitialNotification =
  async (): Promise<FirebaseMessagingTypes.RemoteMessage | null> => {
    try {
      const remoteMessage = await messaging().getInitialNotification();

      if (remoteMessage) {
        console.log("App opened from notification:", remoteMessage);
        return remoteMessage;
      }

      return null;
    } catch (error) {
      console.error("Error getting initial notification:", error);
      return null;
    }
  };

/**
 * Set up notification opened handler
 */
export const setupNotificationOpenedHandler = (
  onNotificationOpened: (
    remoteMessage: FirebaseMessagingTypes.RemoteMessage,
  ) => void,
): (() => void) => {
  return messaging().onNotificationOpenedApp((remoteMessage) => {
    console.log("Notification opened app:", remoteMessage);
    onNotificationOpened(remoteMessage);
  });
};

/**
 * Check notification permissions status
 */
export const checkNotificationPermissions = async (): Promise<boolean> => {
  try {
    if (Platform.OS === "ios") {
      const authStatus = await messaging().hasPermission();
      return (
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL
      );
    } else {
      // For Android, check if we have the token
      const token = await AsyncStorage.getItem(DEVICE_TOKEN_KEY);
      return !!token;
    }
  } catch (error) {
    console.error("Error checking notification permissions:", error);
    return false;
  }
};

export default {
  configurePushNotifications,
  requestNotificationPermissions,
  registerForPushNotifications,
  getDeviceToken,
  deleteDeviceToken,
  showLocalNotification,
  scheduleLocalNotification,
  cancelAllLocalNotifications,
  setupForegroundNotificationHandler,
  setupBackgroundNotificationHandler,
  getInitialNotification,
  setupNotificationOpenedHandler,
  checkNotificationPermissions,
};
