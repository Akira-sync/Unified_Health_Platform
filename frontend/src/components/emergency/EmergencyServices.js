import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import IconSet from '../IconSet'; // default import from IconSet.js

function EmergencyServices() {
  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        {/* Use IconSet and pass type="emergency" */}
        <IconSet type="emergency" size="large" color="secondary" sx={{ mb: 2 }} />
        <Typography variant="h4" gutterBottom>Emergency Services</Typography>
        <Typography variant="body1" color="text.secondary">
          Quick emergency bed discovery and priority booking for critical patients.
        </Typography>
        <Box sx={{ mt: 2, p: 2, bgcolor: 'warning.50', borderRadius: 1 }}>
          <Typography variant="body2">
            🚨 This feature is under development for the prototype demo.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default EmergencyServices;
