import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import IconSet from '../IconSet'; // Make sure the path is correct

function HospitalDashboard() {
  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <IconSet type="hospital" sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          Hospital Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage hospital beds, view patient intake, and update facility information.
        </Typography>
        <Box sx={{ mt: 2, p: 2, bgcolor: 'info.50', borderRadius: 1 }}>
          <Typography variant="body2">
            🚧 This feature is under development for the prototype demo.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default HospitalDashboard;
