/**
 * @file form of entering email
 * @author Mingze Ma
 */

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import FormGroup from '@mui/material/FormGroup';
import { useEffect, useState } from "react";
import _ from "lodash";

const ACCOUNT_TYPE = [
  { label: 'Donor', value: 0 },
  { label: 'Charity', value: 1 },
];

export default (props) => {
  const { btnLabel, onChange: customOnChange } = props;

  const [accountType, setAccountType] = useState(ACCOUNT_TYPE[0].value);

  const handleButtonChange = (_e, data) => {
    setAccountType(data);
  }

  useEffect(() => {
    customOnChange({}, { [btnLabel]: accountType });
  }, [accountType, btnLabel, customOnChange]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <FormControlLabel
          required
          label="Account Type *"
          labelPlacement="start"
          value={accountType}
          control={
            <ToggleButtonGroup
              className="account-type"
              color="primary"
              value={accountType}
              exclusive
              onChange={handleButtonChange}
            >
              {
                _.map(ACCOUNT_TYPE, ({ label, value }) => (
                  <ToggleButton key={value} value={value}>{label}</ToggleButton>
                ))
              }
            </ToggleButtonGroup>
          }
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          required
          fullWidth
          id="username"
          label="Email Address"
          name="username"
          autoComplete="email"
        />
      </Grid>
      <Grid item xs={12}>
        <FormControlLabel
          name="allow_extra_mails"
          control={<Checkbox value="allowExtraEmails" color="primary"/>}
          label="I want to receive inspiration, marketing promotions and updates via email."
        />
      </Grid>
    </Grid>
  );
};
