/**
 * @file project list for donors and guests
 * @author Mingze Ma
 */

import { forwardRef, useCallback, useEffect, useState } from 'react';
// material
import { ButtonGroup, Container, Grid, Icon, Stack, TextField, Typography } from '@mui/material';
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
import Autocomplete from "@mui/material/Autocomplete";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

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
  const [projectDetail, setProjectDetail] = useState({});
  const [prepareMode, setPrepareMode] = useState(false);
  const { userInfo } = useSelector(state => state.user);
  const { regionInfo, currencyList } = useSelector(state => state.global);

//Search
  const [searchItem, setSearchItem] = useState(' ');
//Menu
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const [sortItem, setSortItem] = React.useState('progress');

  const [formattedCurrencyList, setFormattedCurrencyList] = useState([]);
  const [currentCurrency, setCurrentCurrency] = useState({ label: '', value: '' });

  const [asc, setAsc] = useState(false);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = async (event) => {
    setAnchorEl(null);
    event.preventDefault();
    if (!!event.currentTarget.id) {
      setSortItem(event.currentTarget.id);
    }
  };
  const handleSearchProject = async (event) =>{
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setSearchItem(data.get('search'));
  }
  const getProjectList = useCallback(async () => {
    try {
      let res = await actions.getProjectList({
        currency_type: currentCurrency.value,
        page_info: {
          page_size: 10000,
          page: 1
        },
        search: searchItem,
        order: `${asc ? '' : '-'}${sortItem}`,
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
      setProjectDetail(result);
      console.log(projectInfo);
    } catch (e) {
      console.error(e);
    }
  }, [asc, currentCurrency.value, searchItem, sortItem]);

  useEffect(() => {
    if (!_.isEmpty(currentCurrency.value)) {
      getProjectList().catch(err => console.error(err));
    }
  }, [currentCurrency, dispatch, getProjectList]);

  useEffect(() => {
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  useEffect(() => {
    if (!_.isEmpty(currencyList)) {
      const thisList = _.map(currencyList, ({ label, value }) => {
        return { label: `${value} (${label})`, value };
      });
      setFormattedCurrencyList(thisList);
      // set current currency value obj
      const currentObj = _.find(
        currencyList,
        (item) => item.value === (_.get(userInfo, 'currency_type') || _.get(regionInfo, 'currencyType'))
      );
      setCurrentCurrency({ label: `${currentObj.value} (${currentObj.label})`, value: currentObj.value })
    }
  }, [currencyList, regionInfo, userInfo]);

  return (
    <Container className="project">
      <Typography variant="h4">Choose a Project</Typography>
      <Grid
        container
        sx={{ pb: 4, pt: 4 }}
        spacing={2}
        justifyContent="space-between"
        alignItems="center"
      >
        <Grid item xs={12} sm={4}>
          <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', mt: {xs: 2, sm: 0}, mb: {xs: 2, sm: 0} }}
            onSubmit={handleSearchProject}
          >
            <Icon aria-label="menu" sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', pl: 2, pr:1}}>
              <MenuIcon />
            </Icon>
            <InputBase
              sx={{ ml: 1, flex: 1 }}
              placeholder="Search Project"
              inputProps={{ 'aria-label': 'search project' , 'maxLength': 30}}
              id="search-item"
              name="search"
              label="search-item"

            />
            <IconButton sx={{ p: '10px' }} aria-label="search" type="submit" >
              <SearchIcon />
            </IconButton>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Autocomplete
            disableClearable
            disablePortal
            id="currency"
            options={formattedCurrencyList}
            value={currentCurrency}
            onChange={(e, value) => setCurrentCurrency(value)}
            renderInput={(params) => <TextField
              {...params}
              label="Select Currency"
            />}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <ButtonGroup variant="contained">
            <Button
              id="demo-customized-button"
              aria-controls={open ? 'demo-customized-menu' : undefined}
              aria-haspopup="true"
              aria-expanded={open ? 'true' : undefined}
              variant="contained"
              disableElevation
              onClick={() => setAsc(prevState => !prevState)}
              startIcon={asc ? <ArrowUpwardIcon /> : <ArrowDownwardIcon />}
            >
              { asc ? 'ASC' : 'DESC' }
            </Button>
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
          </ButtonGroup>
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
            <MenuItem label="pregress" id='progress' onClick={handleClose} disableRipple>
              <PeopleIcon />
              Progress
            </MenuItem>
          </StyledMenu>
        </Grid>
      </Grid>
      <Box>
        <ProjectList currencyType={currentCurrency.value} projects={_.get(projectDetail, 'projectInfo', [])} />
      </Box>
    </Container>
  );
}
