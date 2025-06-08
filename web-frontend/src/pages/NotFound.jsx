import React from 'react';
import { Box, Typography, Container } from '@mui/material';

const NotFound = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <Typography variant="h1" component="h1" gutterBottom>
          404
        </Typography>
        <Typography variant="h4" component="h2" gutterBottom>
          Page Not Found
        </Typography>
        <Typography variant="body1">
          The page you are looking for does not exist.
        </Typography>
      </Box>
    </Container>
  );
};

export default NotFound;

