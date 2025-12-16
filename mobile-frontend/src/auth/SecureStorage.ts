import * as Keychain from "react-native-keychain";
import { Platform } from "react-native";

/**
 * Securely store a key-value pair using the device's keychain/keystore
 */
export const storeSecurely = async (
  key: string,
  value: string,
): Promise<{ success: boolean; error?: string }> => {
  try {
    const options: Keychain.Options = {
      service: `com.quantumalpha.${key}`,
      accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED,
      ...(Platform.OS === "ios" && {
        accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY,
      }),
    };

    await Keychain.setGenericPassword(key, value, options);

    console.log(`Stored ${key} securely in keychain`);
    return { success: true };
  } catch (error) {
    console.error(`Error storing ${key} securely:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Storage error",
    };
  }
};

/**
 * Retrieve a securely stored value
 */
export const retrieveSecurely = async (
  key: string,
): Promise<{ success: boolean; value?: string; error?: string }> => {
  try {
    const options: Keychain.Options = {
      service: `com.quantumalpha.${key}`,
    };

    const credentials = await Keychain.getGenericPassword(options);

    if (credentials && credentials.password) {
      console.log(`Retrieved ${key} securely from keychain`);
      return { success: true, value: credentials.password };
    } else {
      return {
        success: false,
        error: "No data found for this key",
      };
    }
  } catch (error) {
    console.error(`Error retrieving ${key} securely:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Retrieval error",
    };
  }
};

/**
 * Delete a securely stored value
 */
export const deleteSecurely = async (
  key: string,
): Promise<{ success: boolean; error?: string }> => {
  try {
    const options: Keychain.Options = {
      service: `com.quantumalpha.${key}`,
    };

    const result = await Keychain.resetGenericPassword(options);

    if (result) {
      console.log(`Deleted ${key} securely from keychain`);
      return { success: true };
    } else {
      return {
        success: false,
        error: "Failed to delete data",
      };
    }
  } catch (error) {
    console.error(`Error deleting ${key} securely:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Deletion error",
    };
  }
};

/**
 * Check if a key exists in secure storage
 */
export const keyExists = async (key: string): Promise<boolean> => {
  try {
    const options: Keychain.Options = {
      service: `com.quantumalpha.${key}`,
    };

    const credentials = await Keychain.getGenericPassword(options);
    return !!credentials;
  } catch (error) {
    console.error(`Error checking if ${key} exists:`, error);
    return false;
  }
};

/**
 * Store user credentials securely
 */
export const storeCredentials = async (
  username: string,
  password: string,
): Promise<{ success: boolean; error?: string }> => {
  try {
    const options: Keychain.Options = {
      service: "com.quantumalpha.userCredentials",
      accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
      ...(Platform.OS === "ios" && {
        accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY_OR_DEVICE_PASSCODE,
      }),
    };

    await Keychain.setGenericPassword(username, password, options);

    console.log("Stored user credentials securely");
    return { success: true };
  } catch (error) {
    console.error("Error storing credentials:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Storage error",
    };
  }
};

/**
 * Retrieve user credentials securely
 */
export const retrieveCredentials = async (): Promise<{
  success: boolean;
  username?: string;
  password?: string;
  error?: string;
}> => {
  try {
    const options: Keychain.Options = {
      service: "com.quantumalpha.userCredentials",
    };

    const credentials = await Keychain.getGenericPassword(options);

    if (credentials) {
      console.log("Retrieved user credentials securely");
      return {
        success: true,
        username: credentials.username,
        password: credentials.password,
      };
    } else {
      return {
        success: false,
        error: "No credentials found",
      };
    }
  } catch (error) {
    console.error("Error retrieving credentials:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Retrieval error",
    };
  }
};

/**
 * Delete user credentials
 */
export const deleteCredentials = async (): Promise<{
  success: boolean;
  error?: string;
}> => {
  try {
    const options: Keychain.Options = {
      service: "com.quantumalpha.userCredentials",
    };

    const result = await Keychain.resetGenericPassword(options);

    if (result) {
      console.log("Deleted user credentials securely");
      return { success: true };
    } else {
      return {
        success: false,
        error: "Failed to delete credentials",
      };
    }
  } catch (error) {
    console.error("Error deleting credentials:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Deletion error",
    };
  }
};

/**
 * Clear all secure storage
 */
export const clearAllSecureStorage = async (): Promise<{
  success: boolean;
  error?: string;
}> => {
  try {
    // Note: This only clears credentials, not all keychain items
    // Individual items need to be deleted separately
    await deleteCredentials();

    console.log("Cleared all secure storage");
    return { success: true };
  } catch (error) {
    console.error("Error clearing secure storage:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Clear error",
    };
  }
};

export default {
  storeSecurely,
  retrieveSecurely,
  deleteSecurely,
  keyExists,
  storeCredentials,
  retrieveCredentials,
  deleteCredentials,
  clearAllSecureStorage,
};
