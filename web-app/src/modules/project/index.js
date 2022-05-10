/**
 * @file project list for donors and guests
 * @author Mingze Ma
 */

import { forwardRef, useCallback, useEffect, useState } from 'react';
// material
import {Container, Icon, Stack, Typography} from '@mui/material';
// components
import { ProjectList } from 'src/components/ProjectCardList';
//
import _ from "lodash";
// material
import { Box } from '@mui/material';

import actions from "src/actions";
import { useDispatch, useSelector } from "react-redux";
import { DEFAULT_CURRENCY } from "src/constants/constants";
import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import PeopleIcon from '@mui/icons-material/People';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import TitleIcon from '@mui/icons-material/Title';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
// ----------------------------------------------------------------------
const StyledMenu = styled((props) => (
    <Menu
        elevation={0}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        {...props}
    />
))(({ theme }) => ({
  '& .MuiPaper-root': {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color:
        theme.palette.mode === 'light' ? 'rgb(55, 65, 81)' : theme.palette.grey[300],
    boxShadow:
        'rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px',
    '& .MuiMenu-list': {
      padding: '4px 0',
    },
    '& .MuiMenuItem-root': {
      '& .MuiSvgIcon-root': {
        fontSize: 18,
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
      },
      '&:active': {
        backgroundColor: alpha(
            theme.palette.primary.main,
            theme.palette.action.selectedOpacity,
        ),
      },
    },
  },
}));

export default (props) => {

  const {} = props;
  const dispatch = useDispatch();
  const [projectInfo, setProjectInfo] = useState({});
  const [prepareMode, setPrepareMode] = useState(false);
  const { userInfo } = useSelector(state => state.user);
//Search
  const [searchItem, setSearchItem] = useState(' ');
//Menu
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const [sortItem, setSortItem] = React.useState('charity');
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = async (event) => {
    setAnchorEl(null);
    event.preventDefault();
    setSortItem(event.currentTarget.id);
  };
  const handleSearchProject = async (event) =>{
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log(data.get('search'));
    setSearchItem(data.get('search'));
  }
  const getProjectList = useCallback(async () => {
    try {
      let res = await actions.getProjectList({
        currency_type: userInfo.currency_type || DEFAULT_CURRENCY,
        page_info: {
          page_size: 10000,
          page: 1
        },
        search: searchItem,
        order: sortItem,
        uid: '',
        valid_only: 1,
      });
      const {
        project_info: rawProjectInfo,
        page_info: pageInfo,
        currency_type: currencyType,
        ...otherProps
      } = res;
      const projectInfo = _.values(rawProjectInfo);
      const result = {
        ...otherProps,
        projectInfo,
        pageInfo,
        currencyType,
      };
      setProjectInfo(result);
      console.log(projectInfo);
    } catch (e) {
      console.error(e);
    }
  }, [searchItem, sortItem, userInfo.currency_type]);

  useEffect(() => {
    getProjectList().catch(err => console.error(err));
  }, [dispatch, getProjectList]);

  return (
    <Container className="project">
      <Stack
        direction="row"
        justifyContent="space-between"
        sx={{ pb: 4 }}
      >
        <Typography variant="h4">Choose a Project</Typography>
        <Paper
          component="form"
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400 }}
          onSubmit={handleSearchProject}
        >
          <Icon aria-label="menu" sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', pl: 2, pr:1}}>
            <MenuIcon />
          </Icon>
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="Search Project"
            inputProps={{ 'aria-label': 'search project' , 'maxlength': 30}}
            id="search-item"
            name="search"
            label="search-item"

          />
          <IconButton sx={{ p: '10px' }} aria-label="search" type="submit" >
            <SearchIcon />
          </IconButton>
        </Paper>
        <Button
          id="demo-customized-button"
          aria-controls={open ? 'demo-customized-menu' : undefined}
          aria-haspopup="true"
          aria-expanded={open ? 'true' : undefined}
          variant="contained"
          disableElevation
          onClick={handleClick}
          endIcon={<KeyboardArrowDownIcon />}
        >
          Sort by
        </Button>
        <StyledMenu
          id="demo-customized-menu"
          MenuListProps={{
            'aria-labelledby': 'demo-customized-button',
          }}
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          onSubmit = {handleClose}
        >
          <MenuItem label="charity" id='charity' onClick={handleClose} disableRipple>
            <PeopleIcon />
            Charity
          </MenuItem>
          <MenuItem label="price" id='price' onClick={handleClose} disableRipple>
            <CheckCircleOutlineIcon />
            Price
          </MenuItem>
          <MenuItem label="start_time" id='start_time' onClick={handleClose} disableRipple>
            <AccessTimeIcon />
            Start Time
          </MenuItem>
          <MenuItem label="end_time" id='end_time' onClick={handleClose} disableRipple>
            <AccessAlarmIcon />
            End Time
          </MenuItem>
          <MenuItem label="title" id='title' onClick={handleClose} disableRipple>
            <TitleIcon />
            Title
          </MenuItem>
        </StyledMenu>
      </Stack>
      <Box>
        <ProjectList projects={_.get(projectInfo, 'projectInfo', [])} />
      </Box>
    </Container>
  );
}
