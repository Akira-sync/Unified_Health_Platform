import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  Divider
} from '@mui/material';
import IconSet from '../IconSet'; // ✅ reusable icon
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function PatientLogin() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    aadhaar_id: '',
    password: '' // ✅ added password field
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    // ✅ Basic validation
    if (!formData.aadhaar_id.trim() || !formData.password.trim()) {
      setError('Please enter both Aadhaar ID and password.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('/api/auth/login', formData);
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user_type', 'patient');
        localStorage.setItem('patient_data', JSON.stringify(response.data.patient));
        
        setSuccess('Login successful! Redirecting...');
        setTimeout(() => {
          navigate('/patient/dashboard');
        }, 1000);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <IconSet type="patient" color="primary" size="large" /> {/* ✅ replaced icon */}
          <Typography variant="h4" component="h1" gutterBottom>
            Patient Login
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Access your unified health records using your Aadhaar ID
          </Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            required
            name="aadhaar_id"
            label="Aadhaar ID (12 digits)"
            value={formData.aadhaar_id}
            onChange={handleChange}
            placeholder="xxxx xxxx xxxx"
            inputProps={{ maxLength: 12, pattern: '[0-9]{12}' }}
            sx={{ mb: 3 }}
            disabled={loading}
            helperText="Enter your 12-digit Aadhaar number"
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
            helperText="Enter your password"
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={loading || formData.aadhaar_id.length !== 12}
            sx={{ mb: 3 }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Don't have an account?{' '}
            <Link
              component="button"
              variant="body2"
              onClick={(e) => {
                e.preventDefault();
                navigate('/patient/register');
              }}
            >
              Register here
            </Link>
          </Typography>
        </Box>

        <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <strong>Demo Credentials:</strong><br />
            For testing, use any 12-digit number as Aadhaar ID.<br />
            Example: 123456789012
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default PatientLogin;
