import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {Avatar, Badge, FormGroup, Grid, styled, FormControl, TextField} from '@mui/material';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import Button from '@mui/material/Button';
import {Form} from "antd";
import {useDispatch, useSelector} from "react-redux";
import Typography from "@mui/material/Typography";
import Autocomplete from "@mui/material/Autocomplete";
import actions from "src/actions";


export default () => {

  const navigate = useNavigate();

  const [nameColor, setNameColor] = React.useState(null);
  const [regionColor, setRegionColor] = React.useState(null);
  const [currencyColor, setCurrencyColor] = React.useState(null);

  const handleChange = (event) => {
    switch (event.target.name) {
      case "name":
        if (event.target.value !== userInfo.name) {
          setNameColor("success");
        } else {
          setNameColor(null);
        }
        break;
      case "region":
        if (event.target.value !== userInfo.region) {
          setRegionColor("success");
        } else {
          setRegionColor(null);
        }
        break;
      case "currency":
        if (event.target.value !== userInfo.currency_type) {
            setCurrencyColor("success");
        } else {
          setCurrencyColor(null);
        }
        break;
    };
  };


  const dispatch = useDispatch();

  const {userInfo} = useSelector(state => state.user);
  const { regionList, currencyList } = useSelector(state => state.global);

  const currencyCode = currencyList.map(item => item.value);

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  const Input = styled('input')({
    display: 'none',
  });

  return (
    <Grid container rowSpacing={5}>
      <Grid item xs={12}>
        <Badge
          overlap="circular"
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          badgeContent={
            <Stack direction="row" alignItems="center" spacing={2}>
              <label htmlFor="icon-button-file">
                <Input accept="image/*" id="icon-button-file" type="file" />
                <IconButton color="primary" aria-label="upload picture" component="span">
                  <PhotoCameraIcon variant="contained" fontSize="large"/>
                </IconButton>
              </label>
            </Stack>
          }>
          <Avatar sx={{ width: 300, height: 300 }}/>
        </Badge>
      </Grid>

      <Grid item xs={12}>
        <Typography textAlign="left" >{userInfo.name}</Typography>
      </Grid>


      <Grid item xs={12}>
        <Button variant="contained" >
          Edit profile
        </Button>
      </Grid>

      <Grid item xs={3} visibility="true" >
        <div>
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
              <Autocomplete
                defaultValue={userInfo.region}
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
                  color={regionColor}
                  focused
                />}
              />
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
                  color={currencyColor}
                  focused
                />}
              />
            </Grid>
          </Grid>
        </div>
      </Grid>
    </Grid>
  );
};