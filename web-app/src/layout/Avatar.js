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
import Typography from "@mui/material/Typography";

export default () => {

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [anchorEl, setAnchorEl] = useState(null);

  const settings = ['Profile', 'Account', 'Logout'];

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  async function handleClick(key) {
    switch (key) {
      case 'Logout':
        await handleLogOut();
        break;
      case 'Profile':
        navigate('/account/profile');
        break;
    };
  }

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
          vertical: 'bottom',
          horizontal: 'left',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {settings.map((setting) => (
          <MenuItem key={setting}  onClick={() => handleClick(setting)}>
            <Typography textAlign="center" >{setting}</Typography>
          </MenuItem>
        ))}
      </Menu>
    </div>
  );
};
