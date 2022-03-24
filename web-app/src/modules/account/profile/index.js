import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {Avatar, Badge, FormGroup, Grid, styled, FormControl, TextField} from '@mui/material';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import Button from '@mui/material/Button';
import {useDispatch, useSelector} from "react-redux";
import Typography from "@mui/material/Typography";
import Autocomplete from "@mui/material/Autocomplete";
import actions from "src/actions";


export default () => {

  const dispatch = useDispatch();

  const {userInfo} = useSelector(state => state.user);
  const { regionList, currencyList } = useSelector(state => state.global);
  const currencyCode = currencyList.map(item => item.value);

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  const navigate = useNavigate();

  const [nameColor, setNameColor] = useState(null);
  const [regionColor, setRegionColor] = useState(null);
  const [currencyColor, setCurrencyColor] = useState(null);
  const [saveDisabled, setSaveDisabled] = useState(true);
  const [display, setDisplay] = useState("none");
  const [editDisplay, setEditDisplay] = useState(null);

  const handleDisplay = () => {
    setDisplay(null);
    setEditDisplay("none");
  };

  // @Todo refresh the Grid
  const handleCancel = () => {
    setDisplay("none");
    setEditDisplay(null);
  };

  const handleChange = async (event) => {
    switch (event.target.name) {
      case "name":
        if (event.target.value !== userInfo.name) {
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
        if (event.target.value !== userInfo.region) {
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
        if (event.target.value !== userInfo.currency_type) {
          setCurrencyColor("success");
          setSaveDisabled(false);
        } else if (regionColor === null && nameColor === null){
          setSaveDisabled(true);
          setCurrencyColor(null);
        } else {
          setCurrencyColor(null);
        }
        break;
    };
  };

  const Input = styled('input')({
    display: 'none',
  });

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
          <Avatar sx={{ width: 200, height: 200 }}/>
        </Badge>
      </Grid>

      <Grid item xs={12} display={editDisplay}>
        <Typography textAlign="left" >{userInfo.name}</Typography>
      </Grid>


      <Grid item xs={12} display={editDisplay}>
        <Button variant="contained" onClick={handleDisplay}>
          Edit profile
        </Button>
      </Grid>

      <Grid item xs={3} display={display}>
        <Grid container spacing={2}>
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
                onBlur={handleChange}
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
                onBlur={handleChange}
                color={currencyColor}
                focused
              />}
            />
          </Grid>
          <Grid item xs={5}>
            <Button disabled={saveDisabled} variant="contained">
              Save
            </Button>
          </Grid>
          <Grid item xs={7}>
            <Button variant="text" onClick={handleCancel}>
              Cancel
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};