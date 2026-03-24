import React from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Box,
  Avatar,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import IconSet from '../IconSet'; // Make sure the path is correct

function PatientDashboard() {
  const navigate = useNavigate();
  
  // Get patient data from localStorage (in real app, this would be from API)
  const patientData = JSON.parse(localStorage.getItem('patient_data') || '{}');

  const quickActions = [
    {
      title: 'Find Beds',
      description: 'Search for available hospital beds',
      icon: 'seat',
      color: 'primary',
      action: () => navigate('/beds/search')
    },
    {
      title: 'Emergency',
      description: 'Quick emergency bed booking',
      icon: 'emergency',
      color: 'secondary',
      action: () => navigate('/emergency')
    },
    {
      title: 'Medical Records',
      description: 'View your health history',
      icon: 'assignment',
      color: 'info',
      action: () => navigate('/records')
    }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Patient Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome back, {patientData.name || 'Patient'}
        </Typography>
      </Box>

      {/* Patient Profile Card */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
              <IconSet type="patient" />
            </Avatar>
            <Box>
              <Typography variant="h6">{patientData.name || 'Patient Name'}</Typography>
              <Typography variant="body2" color="text.secondary">
                Aadhaar: {patientData.aadhaar_id || 'N/A'}
              </Typography>
            </Box>
          </Box>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Age</Typography>
              <Typography variant="body1">{patientData.age || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Gender</Typography>
              <Typography variant="body1">{patientData.gender || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Blood Group</Typography>
              <Chip 
                label={patientData.blood_group || 'Unknown'} 
                size="small" 
                color="primary" 
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Phone</Typography>
              <Typography variant="body1">{patientData.phone || 'N/A'}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Typography variant="h5" component="h2" gutterBottom>
        Quick Actions
      </Typography>
      <Grid container spacing={3}>
        {quickActions.map((action, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={action.action}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box sx={{ mb: 2, color: `${action.color}.main` }}>
                  <IconSet type={action.icon} sx={{ fontSize: 48 }} />
                </Box>
                <Typography variant="h6" gutterBottom>
                  {action.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {action.description}
                </Typography>
                <Button variant="contained" color={action.color} onClick={action.action}>
                  Go to {action.title}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default PatientDashboard;
