import React from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Chip,
  Paper
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import IconSet from './IconSet'; // Make sure the path is correct

function Home() {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Real-time Bed Tracking',
      description: 'Find available hospital beds across facilities in real-time',
      iconType: 'hospital',
      color: 'primary',
      action: () => navigate('/beds/search'),
      actionText: 'Search Beds'
    },
    {
      title: 'Emergency Services',
      description: 'Quick ICU bed discovery and booking for emergency situations',
      iconType: 'emergency',
      color: 'secondary',
      action: () => navigate('/emergency'),
      actionText: 'Emergency Mode'
    },
    {
      title: 'Unified Medical Records',
      description: 'Access comprehensive health history across all hospitals',
      iconType: 'record',
      color: 'primary',
      action: () => navigate('/records'),
      actionText: 'View Records'
    }
  ];

  const benefits = [
    { label: 'Aadhaar Integration', iconType: 'verified' },
    { label: 'Real-time Updates', iconType: 'speed' },
    { label: 'Digital Prescriptions', iconType: 'assignment' },
    { label: 'Emergency Ready', iconType: 'alert' }
  ];

  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Paper 
        elevation={3} 
        sx={{ 
          p: 4, 
          mb: 4, 
          background: 'linear-gradient(45deg, #1976d2 30%, #21cbf3 90%)',
          color: 'white',
          textAlign: 'center'
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Unified Health Platform
        </Typography>
        <Typography variant="h6" component="p" sx={{ mb: 3 }}>
          Addressing India's healthcare system challenges with digital innovation
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, opacity: 0.9 }}>
          Reducing long queues, enabling real-time bed availability tracking, 
          and creating unified Aadhaar-linked patient records for better healthcare delivery.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button 
            variant="contained" 
            color="secondary" 
            size="large"
            onClick={() => navigate('/patient/register')}
          >
            Get Started as Patient
          </Button>
          <Button 
            variant="outlined" 
            color="inherit" 
            size="large"
            onClick={() => navigate('/hospital/login')}
          >
            Hospital Login
          </Button>
        </Box>
      </Paper>

      {/* Key Benefits */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom align="center">
          Key Features
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          {benefits.map((benefit, index) => (
            <Chip
              key={index}
              icon={<IconSet type={benefit.iconType} />}
              label={benefit.label}
              variant="outlined"
              size="medium"
              sx={{ p: 1 }}
            />
          ))}
        </Box>
      </Box>

      {/* Feature Cards */}
      <Typography variant="h5" component="h2" gutterBottom align="center" sx={{ mb: 3 }}>
        How We're Solving Healthcare Challenges
      </Typography>
      <Grid container spacing={3}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ textAlign: 'center', flexGrow: 1 }}>
                <Box sx={{ mb: 2, color: `${feature.color}.main` }}>
                  <IconSet type={feature.iconType} sx={{ fontSize: 40 }} />
                </Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button variant="contained" color={feature.color} onClick={feature.action}>
                  {feature.actionText}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Problem Statement */}
      <Paper elevation={1} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" component="h3" gutterBottom>
          The Healthcare Challenge We're Addressing
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="primary" gutterBottom>
              Current Problems:
            </Typography>
            <Typography variant="body2" component="ul" sx={{ ml: 2 }}>
              <li>Long queues and excessive wait times</li>
              <li>No real-time bed availability information</li>
              <li>Fragmented patient records across hospitals</li>
              <li>Emergency delays in finding ICU beds</li>
              <li>Difficulty accessing medical history during critical situations</li>
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="secondary" gutterBottom>
              Our Solutions:
            </Typography>
            <Typography variant="body2" component="ul" sx={{ ml: 2 }}>
              <li>Digital queue management and appointment booking</li>
              <li>Real-time bed availability tracking across hospitals</li>
              <li>Unified Aadhaar-linked patient records</li>
              <li>Priority emergency bed allocation system</li>
              <li>Instant access to complete medical history</li>
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
}

export default Home;
