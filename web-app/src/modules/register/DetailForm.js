/**
 * @file form of register detail
 * @author Mingze Ma
 */

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import MenuItem from '@mui/material/MenuItem';
import Autocomplete from '@mui/material/Autocomplete';
import _ from "lodash";

import actions from "src/actions";

export default (props) => {

  const { username, type } = props;

  const dispatch = useDispatch();
  const { regionList, currencyList } = useSelector(state => state.global);

  const [regionOptions, setRegionOptions] = useState([]);
  const [currencyOptions, setCurrencyOptions] = useState([]);

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  useEffect(() => {
    // reformat region & currency options
    setRegionOptions(_.map(regionList, (item) => ({label: item, value: item})));
    setCurrencyOptions(_.map(currencyList, (item) => ({label: item, value: item})));
  }, [currencyList, regionList]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <TextField
          disabled={true}
          value={username}
          fullWidth
          label="Email Address"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          required
          fullWidth
          id="name"
          label={type === 1 ? "Company Name" : "Full Name"}
          name="name"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          required
          fullWidth
          name="password"
          label="Password"
          type="password"
          id="password"
          autoComplete="new-password"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          required
          fullWidth
          name="confirm-password"
          label="Confirm Password"
          type="password"
          id="confirm-password"
          autoComplete="new-password"
        />
      </Grid>
      <Grid item xs={12}>
        <Autocomplete
          disablePortal
          fullWidth
          id="region"
          options={regionOptions}
          renderInput={(params) => <TextField
            {...params}
            label="Select Region"
            name="region"
          />}
        />
      </Grid>
      <Grid item xs={12}>
        <Autocomplete
          disablePortal
          fullWidth
          id="currency"
          options={currencyOptions}
          renderInput={(params) => <TextField
            {...params}
            label="Select Currency"
            name="currency"
          />}
        />
      </Grid>
    </Grid>
  );
};
