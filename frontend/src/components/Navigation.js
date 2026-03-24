import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';
import IconSet from './IconSet'; // Adjust path if needed
import { useNavigate } from 'react-router-dom';

function Navigation() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNavigation = (path) => {
    navigate(path);
    handleClose();
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconSet type="hospital" sx={{ mr: 2 }} />
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Unified Health Platform
        </Typography>
        
        {/* Desktop Menu */}
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <Button color="inherit" startIcon={<IconSet type="home" /> } onClick={() => navigate('/')}>
            Home
          </Button>
          <Button color="inherit" startIcon={<IconSet type="seat" />} onClick={() => navigate('/beds/search')}>
            Find Beds
          </Button>
          <Button color="inherit" startIcon={<IconSet type="emergency" />} onClick={() => navigate('/emergency')}>
            Emergency
          </Button>
          <Button color="inherit" startIcon={<IconSet type="patient" />} onClick={() => navigate('/patient/login')}>
            Patient Login
          </Button>
          <Button color="inherit" onClick={() => navigate('/hospital/login')}>
            Hospital Login
          </Button>
        </Box>

        {/* Mobile Menu */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            size="large"
            aria-label="navigation menu"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem onClick={() => handleNavigation('/')}>Home</MenuItem>
            <MenuItem onClick={() => handleNavigation('/beds/search')}>Find Beds</MenuItem>
            <MenuItem onClick={() => handleNavigation('/emergency')}>Emergency</MenuItem>
            <MenuItem onClick={() => handleNavigation('/patient/login')}>Patient Login</MenuItem>
            <MenuItem onClick={() => handleNavigation('/hospital/login')}>Hospital Login</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navigation;
