import ReactNativeBiometrics, { BiometryTypes } from "react-native-biometrics";
import { Platform } from "react-native";

const rnBiometrics = new ReactNativeBiometrics({
  allowDeviceCredentials: true,
});

export interface BiometricCapability {
  available: boolean;
  biometryType: BiometryTypes | null;
  error?: string;
}

/**
 * Check if biometric authentication is available on the device
 */
export const checkBiometricAvailability =
  async (): Promise<BiometricCapability> => {
    try {
      const { available, biometryType } =
        await rnBiometrics.isSensorAvailable();

      if (!available) {
        return {
          available: false,
          biometryType: null,
          error: "Biometric authentication is not available on this device",
        };
      }

      return {
        available: true,
        biometryType,
      };
    } catch (error) {
      console.error("Error checking biometric availability:", error);
      return {
        available: false,
        biometryType: null,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  };

/**
 * Get a human-readable name for the biometric type
 */
export const getBiometricTypeName = (
  biometryType: BiometryTypes | null,
): string => {
  if (!biometryType) return "Biometrics";

  switch (biometryType) {
    case BiometryTypes.FaceID:
      return "Face ID";
    case BiometryTypes.TouchID:
      return "Touch ID";
    case BiometryTypes.Biometrics:
      return Platform.OS === "android" ? "Fingerprint" : "Biometrics";
    default:
      return "Biometrics";
  }
};

/**
 * Authenticate user with biometrics
 */
export const authenticateWithBiometrics = async (
  promptMessage?: string,
): Promise<{ success: boolean; error?: string }> => {
  try {
    // First check if biometrics are available
    const capability = await checkBiometricAvailability();

    if (!capability.available) {
      return {
        success: false,
        error: capability.error || "Biometric authentication not available",
      };
    }

    const biometricTypeName = getBiometricTypeName(capability.biometryType);
    const defaultPrompt = `Authenticate with ${biometricTypeName}`;

    // Perform biometric authentication
    const { success, error } = await rnBiometrics.simplePrompt({
      promptMessage: promptMessage || defaultPrompt,
      cancelButtonText: "Cancel",
    });

    if (success) {
      console.log("Biometric authentication successful");
      return { success: true };
    } else {
      console.log("Biometric authentication failed or cancelled");
      return {
        success: false,
        error: error || "Authentication failed or cancelled",
      };
    }
  } catch (error) {
    console.error("Error during biometric authentication:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Authentication error",
    };
  }
};

/**
 * Create biometric keys for secure authentication
 * This is used for more secure scenarios where you need cryptographic signatures
 */
export const createBiometricKeys = async (): Promise<{
  success: boolean;
  publicKey?: string;
}> => {
  try {
    const { publicKey } = await rnBiometrics.createKeys();
    return { success: true, publicKey };
  } catch (error) {
    console.error("Error creating biometric keys:", error);
    return { success: false };
  }
};

/**
 * Delete biometric keys
 */
export const deleteBiometricKeys = async (): Promise<{ success: boolean }> => {
  try {
    await rnBiometrics.deleteKeys();
    return { success: true };
  } catch (error) {
    console.error("Error deleting biometric keys:", error);
    return { success: false };
  }
};

/**
 * Check if biometric keys exist
 */
export const biometricKeysExist = async (): Promise<boolean> => {
  try {
    const { keysExist } = await rnBiometrics.biometricKeysExist();
    return keysExist;
  } catch (error) {
    console.error("Error checking biometric keys:", error);
    return false;
  }
};

/**
 * Create a signature with biometric authentication
 * Useful for high-security operations
 */
export const createBiometricSignature = async (
  payload: string,
  promptMessage?: string,
): Promise<{ success: boolean; signature?: string; error?: string }> => {
  try {
    const keysExist = await biometricKeysExist();

    if (!keysExist) {
      const result = await createBiometricKeys();
      if (!result.success) {
        return { success: false, error: "Failed to create biometric keys" };
      }
    }

    const capability = await checkBiometricAvailability();
    const biometricTypeName = getBiometricTypeName(capability.biometryType);
    const defaultPrompt = `Sign with ${biometricTypeName}`;

    const { success, signature, error } = await rnBiometrics.createSignature({
      promptMessage: promptMessage || defaultPrompt,
      payload,
      cancelButtonText: "Cancel",
    });

    if (success && signature) {
      return { success: true, signature };
    } else {
      return {
        success: false,
        error: error || "Failed to create signature",
      };
    }
  } catch (error) {
    console.error("Error creating biometric signature:", error);
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Signature creation error",
    };
  }
};

export default {
  checkBiometricAvailability,
  getBiometricTypeName,
  authenticateWithBiometrics,
  createBiometricKeys,
  deleteBiometricKeys,
  biometricKeysExist,
  createBiometricSignature,
};
