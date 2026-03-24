import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Grid,
  MenuItem,
  Link,
  Divider
} from '@mui/material';
import { PersonAdd } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function PatientRegister() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    aadhaar_id: '',
    name: '',
    age: '',
    gender: '',
    phone: '',
    email: '',
    address: '',
    blood_group: '',
    emergency_contact_name: '',
    emergency_contact_phone: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
  const genders = ['Male', 'Female', 'Other'];

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

    // Basic validations
    if (formData.aadhaar_id.length !== 12) {
      setError('Aadhaar ID must be 12 digits.');
      setLoading(false);
      return;
    }
    if (formData.age < 0 || formData.age > 120) {
      setError('Please enter a valid age.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('/api/auth/register', formData);
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user_type', 'patient');
        localStorage.setItem('patient_data', JSON.stringify(response.data.patient));
        
        setSuccess('Registration successful! Redirecting...');
        setTimeout(() => {
          navigate('/patient/dashboard');
        }, 1500);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 2 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <PersonAdd color="primary" sx={{ fontSize: 60, mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom>
            Patient Registration
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Create your unified health profile with Aadhaar integration
          </Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                name="aadhaar_id"
                label="Aadhaar ID"
                value={formData.aadhaar_id}
                onChange={handleChange}
                placeholder="xxxx xxxx xxxx"
                helperText="12-digit Aadhaar number"
                inputProps={{ maxLength: 12, pattern: '[0-9]{12}' }}
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                name="name"
                label="Full Name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Your full name"
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                required
                name="age"
                label="Age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                inputProps={{ min: 0, max: 120 }}
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                required
                select
                name="gender"
                label="Gender"
                value={formData.gender}
                onChange={handleChange}
                disabled={loading}
              >
                {genders.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                select
                name="blood_group"
                label="Blood Group"
                value={formData.blood_group}
                onChange={handleChange}
                disabled={loading}
              >
                <MenuItem value="">Select Blood Group</MenuItem>
                {bloodGroups.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                name="phone"
                label="Phone Number"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+91 9876543210"
                helperText="Enter valid phone number"
                inputProps={{ maxLength: 15 }}
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                name="email"
                label="Email (Optional)"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="example@mail.com"
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                required
                multiline
                rows={2}
                name="address"
                label="Address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Street, City, State, Pincode"
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                name="emergency_contact_name"
                label="Emergency Contact Name"
                value={formData.emergency_contact_name}
                onChange={handleChange}
                placeholder="Full name of emergency contact"
                disabled={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                name="emergency_contact_phone"
                label="Emergency Contact Phone"
                value={formData.emergency_contact_phone}
                onChange={handleChange}
                placeholder="+91 9876543210"
                inputProps={{ maxLength: 15 }}
                disabled={loading}
              />
            </Grid>
          </Grid>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={
              loading ||
              !formData.aadhaar_id ||
              !formData.name ||
              !formData.age ||
              !formData.gender ||
              !formData.phone
            }
            sx={{ mt: 3, mb: 2 }}
          >
            {loading ? 'Registering...' : 'Register'}
          </Button>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Already have an account?{' '}
            <Link
              component="button"
              variant="body2"
              onClick={(e) => {
                e.preventDefault();
                navigate('/patient/login');
              }}
            >
              Login here
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default PatientRegister;
