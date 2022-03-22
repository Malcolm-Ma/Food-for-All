/**
 * @file form of verifying email
 * @author Mingze Ma
 */

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

export default (props) => {
  const { username } = props;
  console.log('--username--\n', username);

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
          id="verify-code"
          label="Verify Code"
          name="code"
        />
      </Grid>
    </Grid>
  );
};
