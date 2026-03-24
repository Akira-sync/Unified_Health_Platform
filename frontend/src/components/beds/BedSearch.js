import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import IconSet from '../IconSet';  // default import

function BedSearch() {
  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <IconSet type="search" size="large" color="primary" sx={{ mb: 2 }} />
        <Typography variant="h4" gutterBottom>Bed Search</Typography>
        <Typography variant="body1" color="text.secondary">
          Search for available hospital beds in real-time across all registered facilities.
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

export default BedSearch;
