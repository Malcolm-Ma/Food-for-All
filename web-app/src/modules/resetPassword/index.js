/**
 * @file index - reset password
 * @author Mingze Ma
 */

import { createTheme, ThemeProvider } from '@mui/material/styles';
import Container from "@mui/material/Container";
import { Avatar, CssBaseline, TextField } from "@mui/material";
import Box from "@mui/material/Box";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from "@mui/material/Typography";
import { useCallback, useEffect, useState } from "react";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import LoadingButton from "@mui/lab/LoadingButton";

const theme = createTheme();

export default (props) => {

  const [action, setAction] = useState(0);
  // submit state
  const [submitLoading, setSubmitLoading] = useState(false);
  const [disabledSubmit, setDisabledSubmit] = useState(true);
  const [sendCodeLoading, setSendCodeLoading] = useState(false);

  const handleEmailChange = useCallback((e) => {
    console.log('--value--\n', e.target.value);
  }, []);

  const handleSubmit = useCallback((event, sendingCode = false) => {
    event.preventDefault();
    console.log('--event.currentTarget--\n', new FormData(event.currentTarget).get('email'));
  }, []);

  useEffect(() => {
    setSubmitLoading(true);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Reset Your Password
          </Typography>
          <Box width="100%" component="form" onSubmit={handleSubmit} sx={{ pt: 6 }}>
            <Grid
              container
              spacing={3}
              rowSpacing={4}
              direction="row"
              justifyContent="center"
              alignItems="center"
            >
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  autoFocus
                  onChange={handleEmailChange}
                />
              </Grid>
              <Grid item xs={8}>
                <TextField
                  required
                  fullWidth
                  id="code"
                  label="Verify Code"
                  name="code"
                />
              </Grid>
              <Grid item xs={4}>
                <LoadingButton
                  loading={sendCodeLoading}
                  fullWidth
                  variant="outlined"
                  onClick={(e) => handleSubmit(e, true)}
                >
                  Send Code
                </LoadingButton>
              </Grid>
            </Grid>
            <LoadingButton
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              loading={submitLoading}
              disabled={disabledSubmit}
            >
              { action === 2 ? 'Submit' : 'Verify' }
            </LoadingButton>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
