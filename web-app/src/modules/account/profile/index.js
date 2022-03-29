// @Todo currency full name following the code in()
// @Todo turn to page after create, change title
// @Todo transform error info
import React, {useEffect, useState} from "react";
import {Avatar, Badge, Grid, styled, TextField} from '@mui/material';
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

export default () => {

  const key = 'MessageKey';

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  const {userInfo} = useSelector(state => state.user);
  const { regionList, currencyList, regionMap } = useSelector(state => state.global);
  const currencyCode = currencyList.map(item => item.value);

  const [nameColor, setNameColor] = useState(null);
  const [regionColor, setRegionColor] = useState(null);
  const [currencyColor, setCurrencyColor] = useState(null);
  const [saveDisabled, setSaveDisabled] = useState(true);
  const [display, setDisplay] = useState("none");
  const [editDisplay, setEditDisplay] = useState(null);
  const [name, setName] = useState(userInfo.name);
  const [region, setRegion] = useState(userInfo.region);
  const [currency, setCurrency] = useState(userInfo.currency_type);

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
    if (userType === 0) {
      return (
        <Tag color="warning">
          Donor
        </Tag>
      );
    }
  }

  return (
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
  );
};
