import React from 'react';
import { Snackbar, Alert, Slide } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { removeNotification } from '../../store/slices/uiSlice';

const NotificationPanel = () => {
  const dispatch = useDispatch();
  const notifications = useSelector((state) => state.ui.notifications);

  const handleClose = (id) => {
    dispatch(removeNotification(id));
  };

  return (
    <>
      {notifications.map((notification) => (
        <Snackbar
          key={notification.id}
          open={true}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          TransitionComponent={Slide}
          autoHideDuration={notification.duration || 6000}
          onClose={() => handleClose(notification.id)}
          sx={{ mb: notifications.indexOf(notification) * 8 }}
        >
          <Alert
            onClose={() => handleClose(notification.id)}
            severity={notification.type || 'info'}
            variant="filled"
            elevation={6}
            sx={{ width: '100%' }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      ))}
    </>
  );
};

export default NotificationPanel;
