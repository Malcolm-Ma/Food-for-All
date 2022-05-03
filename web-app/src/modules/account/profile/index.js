// @Todo currency full name following the code in()
// @Todo turn to page after create, change title
// @Todo transform error info
import {useEffect, useRef, useState} from "react";
import {Avatar, Badge, Collapse, Divider, Grid, styled, TextField} from '@mui/material';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import Button from '@mui/material/Button';
import {useDispatch, useSelector} from "react-redux";
import Typography from "@mui/material/Typography";
import Autocomplete from "@mui/material/Autocomplete";
import actions from "src/actions";
import {Image, message, Tag} from 'antd';
import _ from 'lodash';
import {CheckCircleOutlined} from "@ant-design/icons";
import {SERVICE_BASE_URL} from "src/constants/constants";
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import * as React from 'react';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import Box from "@mui/material/Box";
import log from "tailwindcss/lib/util/log";
import moment from "moment";
import ReactEcharts from "echarts-for-react"
import option from "src/configure/ChartConfigDemo";

export default () => {

  const key = 'MessageKey';

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  const {userInfo} = useSelector(state => state.user);
  const { regionList, currencyList, regionMap } = useSelector(state => state.global);
  const currencyCode = currencyList.map(item => item.label+" ("+item.value+")");

  const [nameColor, setNameColor] = useState(null);
  const [regionColor, setRegionColor] = useState(null);
  const [currencyColor, setCurrencyColor] = useState(null);
  const [saveDisabled, setSaveDisabled] = useState(true);
  const [display, setDisplay] = useState("none");
  const [editDisplay, setEditDisplay] = useState(null);
  const [name, setName] = useState(userInfo.name);
  const [region, setRegion] = useState(userInfo.region);
  const [currency, setCurrency] = useState(userInfo.currency_type);
  const [history, setHistory] = useState([]);
  const [lock, setLock] = useState(false);

  function getRegionName(value) {
    // return regionList.filter(
    //   function(regionList){return regionList.value == value}
    // );
    return regionMap[value];
  }

  const handleDisplay = () => {
    setNameColor(null);
    setRegionColor(null);
    setCurrencyColor(null);
    setSaveDisabled(true);
    setDisplay(null);
    setEditDisplay("none");
  };

  // @Todo refresh the Grid
  const handleCancel = () => {
    setDisplay("none");
    setEditDisplay(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    console.log(data);
    try {
      const editUserRes = await actions.editUser({
        name: data.name,
        region: data.region,
        currency_type: data.currency,
        avatar: userInfo.avatar,
      });
      if (editUserRes !== null) {
        setName(data.name);
        setRegion(data.region);
        setCurrency(data.currency);
        handleCancel();
        dispatch(actions.getUserInfo());
        message.success({content: 'Saved!', key});
      }
    } catch (e) {
      await message.error({content: 'Edit Error! ERROR INFO: '+e.name, key});
    }
  };

  const handleChange = async (event) => {
    switch (event.target.name) {
      case "name":
        if (event.target.value !== name) {
          setNameColor("success");
          setSaveDisabled(false);
        } else if (regionColor === null && currencyColor === null){
          setSaveDisabled(true);
          setNameColor(null);
        } else {
          setNameColor(null);
        }
        break;
      case "region":
        if (event.target.value !== region) {
          setRegionColor("success");
          setSaveDisabled(false);
        } else if (nameColor === null && currencyColor === null){
          setSaveDisabled(true);
          setRegionColor(null);
        } else {
          setRegionColor(null);
        }
        break;
      case "currency":
        if (event.target.value !== currency) {
          setCurrencyColor("success");
          setSaveDisabled(false);
        } else if (regionColor === null && nameColor === null){
          setSaveDisabled(true);
          setCurrencyColor(null);
        } else {
          setCurrencyColor(null);
        }
        break;
    }
  };


  const Input = styled('input')({
    display: 'none',
  });

  const userTypeTags = () => {
    const userType = _.get(userInfo, 'type');

    if (userType === 1) {
      return (
        <Tag color="success">
          Charity
        </Tag>
      );
    }
    if (userType === 2) {
      return (
        <Tag color="warning">
          Donor
        </Tag>
      );
    }
  }

  const switchHide = () => {
    if(lock) {
      setLock(false);
    } else {
      setLock(true);
    }
  }

  const donate_history = _.get(userInfo, 'donate_history');

  function createData(title, price, num, sum, pid) {
    const obj = donate_history[pid];
    var his = [];
    for(var key in obj) {
      var temp = {};
      temp.date = moment(key * 1000).format('YYYY-MM-DD HH:mm:ss').toString();
      temp.value = obj[key];
      his.push(temp);
    }
    return {
      title,
      price,
      num,
      sum,
      history: his
    }
  }

  function Row(props) {
    const { row } = props;
    const [open, setOpen] = useState(false);

    return (
      <React.Fragment>
        <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
          <TableCell>
            <IconButton
              aria-label="expand row"
              size="small"
              onClick={() => setOpen(!open)}
            >
              {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          </TableCell>
          <TableCell component="th" scope="row">
            {row.title}
          </TableCell>
          <TableCell align="right">{row.num}</TableCell>
          <TableCell align="right">{row.price}</TableCell>
          <TableCell align="right">{row.sum}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
            <Collapse in={open} timeout="auto" unmountOnExit>
              <Box sx={{ margin: 1}}>
                <Typography variant="h6" gutterBottom component="div">
                  Donate History
                </Typography>
                <Table size="small" aria-label="purchases">
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell>Amount</TableCell>
                      <TableCell>Total price</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {row.history.map((historyRow) => (
                      <TableRow key={historyRow.date}>
                        <TableCell component="th" scope="row">
                          {historyRow.date}
                        </TableCell>
                        <TableCell>{historyRow.value}</TableCell>
                        <TableCell>{historyRow.value*row.price}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
      </React.Fragment>
    );
  }

  function getSumNum(pid) {
    let sum = 0;
    for(var key in _.get(userInfo, 'donate_history')[pid]) {
      sum = sum + _.get(userInfo, 'donate_history')[pid][key];
    };
    return sum;
  }

  useEffect(async () => {
    async function setRows() {
      const rows = []
      for (var pid in _.get(userInfo, 'donate_history')) {
        let pj = await actions.getProjectInfo({
          'pid': pid,
          'currency_type': userInfo.currency_type
        });
        pj = pj['project_info'];
        const sumNum = getSumNum(pid);
        rows.push(createData(pj['title'], pj['price'], sumNum, pj['price'] * sumNum, pid));
      }
      console.log(rows);
      return rows;
    }
    setHistory(await setRows());
  }, []);




  // async function test() {
  //   for(var i in _.get(userInfo, 'donate_history')) {
  //     console.log(i);
  //     const p = await actions.getProjectInfo({
  //       'pid': i,
  //       'currency_type': userInfo.currency_type
  //     })
  //     console.log(p['project_info']);
  //   }
  //
  // }
  // test();
  // const rows = []
  // rows.push(createData("123",1,2,3, '0a1605393836a7babeaa3d9afdcd9280'));
  // console.log(rows);


  return (
    <Grid container>
      <Grid item xs={3}>
        <Grid container rowSpacing={2}>
          <Grid item xs={12}>
            <Badge
              overlap="circular"
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
              badgeContent={
                <Stack direction="row" alignItems="center" spacing={2}>
                  <label htmlFor="icon-button-file">
                    <Input accept="image/*" id="icon-button-file" type="file"/>
                    <IconButton color="primary" aria-label="upload picture" component="span" >
                      <PhotoCameraIcon variant="contained" fontSize="large"/>
                    </IconButton>
                  </label>
                </Stack>
              }>
              <Avatar sx={{ width: 200, height: 200 }} alt="Remy Sharp" src={SERVICE_BASE_URL + _.get(userInfo, 'avatar')}/>
            </Badge>
          </Grid>

          <Grid item xs={12} display={editDisplay}>
            <Typography textAlign="left" >{name}</Typography>
            {userTypeTags()}
          </Grid>


          <Grid item xs={12} display={editDisplay}>
            <Button variant="contained" onClick={handleDisplay}>
              Edit profile
            </Button>
          </Grid>


          {display !== 'none' && <Grid item xs={6}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={4}>
                <Grid item xs={12}>
                  <TextField
                    defaultValue={userInfo.name}
                    required
                    fullWidth
                    id="name"
                    label="Name"
                    name="name"
                    onChange={handleChange}
                    color={nameColor}
                    focused
                  />
                </Grid>

                <Grid item xs={12}>
                  {!_.isEmpty(regionList) && <Autocomplete
                    defaultValue={getRegionName(userInfo.region)}
                    disablePortal
                    fullWidth
                    id="region"
                    options={regionList}
                    renderInput={(params) => <TextField
                      {...params}
                      label="Select Region"
                      name="region"
                      onSelect={handleChange}
                      onClick={handleChange}
                      onInput={handleChange}
                      onChange={handleChange}
                      onBlur={handleChange}
                      color={regionColor}
                      focused
                    />}
                  />}
                </Grid>

                <Grid item xs={12}>
                  <Autocomplete
                    defaultValue={userInfo.currency_type}
                    disablePortal
                    fullWidth
                    id="currency"
                    options={currencyCode}
                    renderInput={(params) => <TextField
                      {...params}
                      label="Select Currency"
                      name="currency"
                      onSelect={handleChange}
                      onClick={handleChange}
                      onInput={handleChange}
                      onChange={handleChange}
                      onBlur={handleChange}
                      color={currencyColor}
                      focused
                    />}
                  />
                </Grid>
                <Grid item xs={5}>
                  <Button disabled={saveDisabled} variant="contained" type="submit">
                    Save
                  </Button>
                </Grid>
                <Grid item xs={7}>
                  <Button variant="text" onClick={handleCancel}>
                    Cancel
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Grid>}
        </Grid>
      </Grid>

      <Divider orientation="vertical" flexItem onClick={switchHide}>
          {lock && <IconButton><LockOpenIcon/></IconButton>}
          {!lock && <IconButton><LockIcon/></IconButton>}
        </Divider>

      <Grid item xs={8} rowSpacing={2}>
        {/*Donor*/}
        {lock && _.get(userInfo, 'type') !== 1 && <Grid item xs={12}>
          <TableContainer sx={{ maxHeight: 1000 }} component={Paper}>
            <Table stickyHeader aria-label="sticky table" aria-label="collapsible table">
              <TableHead>
                <TableRow>
                  <TableCell />
                  <TableCell>Project Title</TableCell>
                  <TableCell align="right">Total number</TableCell>
                  <TableCell align="right">Price</TableCell>
                  <TableCell align="right">Total price</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {history.map((row) => (
                  <Row key={row.title} row={row} />
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>}

        {/*Charity*/}
        {lock && _.get(userInfo, 'type') === 1 && <Grid item xs={12}>
          <ReactEcharts
            option={option}
          />
        </Grid>}


      </Grid>

    </Grid>
  );
};
