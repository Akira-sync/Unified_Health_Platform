import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert
} from '@mui/material';
import IconSet from '../IconSet'; // ✅ Import your reusable IconSet
import { useNavigate } from 'react-router-dom';

function HospitalLogin() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    registration_number: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    // ⚡ Fake login for hackathon demo
    setTimeout(() => {
      if (formData.registration_number.trim() && formData.password.trim()) {
        localStorage.setItem('user_type', 'hospital');
        setSuccess(true);
        setTimeout(() => navigate('/hospital/dashboard'), 1200); // redirect after showing success
      } else {
        setError('Invalid credentials. Please try again.');
      }
      setLoading(false);
    }, 1000);
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <IconSet type="hospital" color="primary" size="large" />
          <Typography variant="h4" component="h1" gutterBottom>
            Hospital Login
          </Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Login successful!</Alert>}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            required
            name="registration_number"
            label="Hospital Registration Number"
            value={formData.registration_number}
            onChange={handleChange}
            sx={{ mb: 3 }}
            disabled={loading}
          />

          <TextField
            fullWidth
            required
            type="password"
            name="password"
            label="Password"
            value={formData.password}
            onChange={handleChange}
            sx={{ mb: 3 }}
            disabled={loading}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default HospitalLogin;
