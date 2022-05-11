/**
 * @file form of register detail
 * @author Mingze Ma
 */

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Autocomplete from '@mui/material/Autocomplete';
import _ from "lodash";
import { Upload } from "antd";
import { UploadOutlined } from "@mui/icons-material";
import Button from "@mui/material/Button";

import actions from "src/actions";
import { SERVICE_BASE_URL } from "src/constants/constants";

export default (props) => {
  const { username, type, setAvatar } = props;

  const dispatch = useDispatch();
  const { regionList, currencyList } = useSelector(state => state.global);
  console.log('--currencyList--\n', currencyList);

  const [formattedCurrencyList, setFormattedCurrencyList] = useState([]);

  const handleUpload = useCallback((info) => {
    if (info.file.status === "done") {
      setAvatar(info.file.response.url);
    }
  }, [setAvatar]);

  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  useEffect(() => {
    if (!_.isEmpty(currencyList)) {
      const thisList = _.map(currencyList, ({ label, value }) => {
        return { label: `${value} (${label})` };
      });
      setFormattedCurrencyList(thisList);
    }
  }, [currencyList]);

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
          options={regionList}
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
          options={formattedCurrencyList}
          renderInput={(params) => <TextField
            {...params}
            label="Select Currency"
            name="currency"
          />}
        />
      </Grid>
      <Grid item xs={12}>
        <Upload
          maxCount={1}
          name="files"
          action={SERVICE_BASE_URL + 'upload_img/'}
          onChange={handleUpload}
        >
          <Button
            variant="outlined"
            startIcon={<UploadOutlined />}
          >Click to Upload Avatar</Button>
        </Upload>
      </Grid>
    </Grid>
  );
};
