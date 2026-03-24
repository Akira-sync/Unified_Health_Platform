import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';

// Components
import Navigation from './components/Navigation';
import Home from './components/Home';
import PatientLogin from './components/auth/PatientLogin';
import PatientRegister from './components/auth/PatientRegister';
import HospitalLogin from './components/auth/HospitalLogin';
import PatientDashboard from './components/patient/PatientDashboard';
import HospitalDashboard from './components/hospital/HospitalDashboard';
import BedSearch from './components/beds/BedSearch';
import EmergencyServices from './components/emergency/EmergencyServices';
import MedicalRecords from './components/records/MedicalRecords';

// Theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navigation />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              
              {/* Authentication Routes */}
              <Route path="/patient/login" element={<PatientLogin />} />
              <Route path="/patient/register" element={<PatientRegister />} />
              <Route path="/hospital/login" element={<HospitalLogin />} />
              
              {/* Dashboard Routes */}
              <Route path="/patient/dashboard" element={<PatientDashboard />} />
              <Route path="/hospital/dashboard" element={<HospitalDashboard />} />
              
              {/* Feature Routes */}
              <Route path="/beds/search" element={<BedSearch />} />
              <Route path="/emergency" element={<EmergencyServices />} />
              <Route path="/records" element={<MedicalRecords />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;