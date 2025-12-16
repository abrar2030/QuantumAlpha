import NetInfo, { NetInfoState } from "@react-native-community/netinfo";

export interface NetworkState {
  isConnected: boolean;
  isInternetReachable: boolean | null;
  type: string;
}

/**
 * Get current network state
 */
export const getNetworkState = async (): Promise<NetworkState> => {
  try {
    const state = await NetInfo.fetch();
    return {
      isConnected: state.isConnected ?? false,
      isInternetReachable: state.isInternetReachable,
      type: state.type,
    };
  } catch (error) {
    console.error("Error getting network state:", error);
    return {
      isConnected: false,
      isInternetReachable: null,
      type: "unknown",
    };
  }
};

/**
 * Subscribe to network state changes
 */
export const subscribeToNetworkChanges = (
  callback: (state: NetworkState) => void,
): (() => void) => {
  const unsubscribe = NetInfo.addEventListener((state: NetInfoState) => {
    callback({
      isConnected: state.isConnected ?? false,
      isInternetReachable: state.isInternetReachable,
      type: state.type,
    });
  });

  return unsubscribe;
};

/**
 * Check if device is online
 */
export const isOnline = async (): Promise<boolean> => {
  try {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  } catch (error) {
    console.error("Error checking online status:", error);
    return false;
  }
};

export default {
  getNetworkState,
  subscribeToNetworkChanges,
  isOnline,
};
