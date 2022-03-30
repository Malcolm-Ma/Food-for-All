import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { useSelector } from "react-redux";

import Avatar from 'src/layout/Avatar';

const Header = (props) => {
  const {} = props;

  const userInfo = useSelector(state => state.user.userInfo);

  const navigate = useNavigate();

  return (
    <AppBar className="frame-nav" position="fixed">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Food For All
        </Typography>
        {
          !userInfo.isLoggedIn
            ? <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
            : <Avatar />
        }
      </Toolbar>
    </AppBar>
  );
};

export default Header;
