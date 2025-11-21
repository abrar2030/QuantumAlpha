import React, { createContext, useState, useContext } from "react";

const AlertContext = createContext();

export const useAlert = () => useContext(AlertContext);

export const AlertProvider = ({ children }) => {
  const [alerts, setAlerts] = useState([]);

  const addAlert = (alert) => {
    const id = Date.now().toString();
    const newAlert = {
      id,
      ...alert,
      timestamp: new Date(),
      read: false,
    };

    setAlerts((prevAlerts) => [newAlert, ...prevAlerts]);
    return id;
  };

  const markAsRead = (id) => {
    setAlerts((prevAlerts) =>
      prevAlerts.map((alert) =>
        alert.id === id ? { ...alert, read: true } : alert,
      ),
    );
  };

  const markAllAsRead = () => {
    setAlerts((prevAlerts) =>
      prevAlerts.map((alert) => ({ ...alert, read: true })),
    );
  };

  const removeAlert = (id) => {
    setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
  };

  const clearAlerts = () => {
    setAlerts([]);
  };

  return (
    <AlertContext.Provider
      value={{
        alerts,
        addAlert,
        markAsRead,
        markAllAsRead,
        removeAlert,
        clearAlerts,
        unreadCount: alerts.filter((alert) => !alert.read).length,
      }}
    >
      {children}
    </AlertContext.Provider>
  );
};
