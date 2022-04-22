// @Todo currency full name following the code in()
// @Todo turn to page after create, change title
// @Todo transform error info
import React, {useEffect, useState} from "react";
import {Avatar, Badge, Grid, styled, TextField} from '@mui/material';
import {useDispatch, useSelector} from "react-redux";
import Typography from "@mui/material/Typography";
import actions from "src/actions";
import {Tag} from 'antd';
import _ from 'lodash';
import {SERVICE_BASE_URL} from "src/constants/constants";

export default () => {

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

  function getRegionName(value) {
    // return regionList.filter(
    //   function(regionList){return regionList.value == value}
    // );
    return regionMap[value];
  }

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
        <Avatar sx={{ width: 200, height: 200 }} alt="Remy Sharp" src={SERVICE_BASE_URL + _.get(userInfo, 'avatar')}/>
      </Grid>

      <Grid item xs={12} display={editDisplay}>
        <Typography textAlign="left" >{name}</Typography>
        {userTypeTags()}
      </Grid>

    </Grid>
  );
};
