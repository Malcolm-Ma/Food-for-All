/**
 * @file Avatar
 * @author Mingze Ma
 */
import { useNavigate } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import React, { useCallback, useMemo, useState } from "react";
import {useDispatch, useSelector} from "react-redux";
import actions from "src/actions";
import Typography from "@mui/material/Typography";
import {Avatar} from "@mui/material";
import {SERVICE_BASE_URL} from "src/constants/constants";
import _ from "lodash";

export default () => {

  const navigate = useNavigate();

  const dispatch = useDispatch();
  const {userInfo} = useSelector(state => state.user);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const settings = useMemo(() => {
    const curSetting = ['Profile', 'Logout'];
    if (_.get(userInfo, 'type') === 1) {
      return ['Admin', ...curSetting];
    }
    return curSetting;
  }, [userInfo]);


  async function handleClick(key) {
    switch (key) {
      case 'Admin':
        navigate('/charity/project/list');
        break;
      case 'Logout':
        await handleLogOut();
        break;
      case 'Profile':
        if ((_.get(userInfo, 'type') === 1)) {
          navigate('/charity/account/profile');
        } else {
          navigate('/account/profile');
        }
        break;
    }
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
        <Avatar alt="Remy Sharp" src={SERVICE_BASE_URL + _.get(userInfo, 'avatar')}/>
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
