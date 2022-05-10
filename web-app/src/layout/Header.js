import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { useSelector } from "react-redux";
import { createTheme, ThemeProvider } from '@mui/material/styles';

import Avatar from 'src/layout/Avatar';

const theme = createTheme({
  status: {
    danger: '#e53e3e',
  },
  palette: {
    primary: {
      main: '#0971f1',
      darker: '#053e85',
    },
    secondary: {
      main: '#e7f7fe',
      contrastText: 'rgba(0, 0, 0, 0.65)',
    },
    neutral: {
      main: '#64748B',
      contrastText: '#fff',
    },
  },
});

const Header = (props) => {
  const { toC } = props;

  const userInfo = useSelector(state => state.user.userInfo);

  const navigate = useNavigate();

  return (
    <ThemeProvider theme={theme}>
      <AppBar className="frame-nav" position="sticky" color={toC ? 'secondary' : 'primary'}>
        <Toolbar>
          <Typography
            variant="h6"
            component="span"
            sx={{ flexGrow: 1, cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            Apex - Food For All
          </Typography>
          {
            !userInfo.isLoggedIn
              ? <>
                <Button
                  color="inherit"
                  onClick={() => navigate('/register')}
                  sx={{ mr: 1 }}
                >Sign Up</Button>
                <Button
                  variant="outlined"
                  color="inherit"
                  onClick={() => navigate('/login')}
                >Login</Button>
              </>
              : <Avatar />
          }
        </Toolbar>
      </AppBar>
    </ThemeProvider>
  );
};

export default Header;
