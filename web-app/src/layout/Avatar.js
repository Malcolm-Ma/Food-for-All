/**
 * @file Avatar
 * @author Mingze Ma
 */
import { useNavigate } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import { useCallback, useState } from "react";
import { useDispatch } from "react-redux";
import actions from "src/actions";

export default () => {

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogOut = useCallback(async () => {
    try {
      await actions.logout();
      navigate('/');
      dispatch(actions.getUserInfo());
    } catch (e) {
      console.error(e);
    }
  }, [dispatch, navigate]);

  return (
    <div>
      <IconButton
        size="large"
        aria-label="account of current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleMenu}
        color="inherit"
      >
        <AccountCircle />
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
          vertical: 'bottom',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleLogOut}>Log Out</MenuItem>
      </Menu>
    </div>
  );
};
