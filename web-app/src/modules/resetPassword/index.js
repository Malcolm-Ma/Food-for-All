/**
 * @file index - reset password
 * @author Mingze Ma
 */

import { createTheme, ThemeProvider } from '@mui/material/styles';
import Container from "@mui/material/Container";
import {
  Avatar,
  Collapse,
  CssBaseline,
  FormControl,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  TextField
} from "@mui/material";
import Box from "@mui/material/Box";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from "@mui/material/Typography";
import { useCallback, useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import LoadingButton from "@mui/lab/LoadingButton";
import { message } from "antd";
import useCountDown from 'react-countdown-hook';
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import { Visibility, VisibilityOff } from "@mui/icons-material";

import actions from "src/actions";

const theme = createTheme();

const INITIAL_TIME = 60 * 1000; // initial time in milliseconds, defaults to 60000
const INTERVAL = 1000; // interval to change remaining time amount, defaults to 1000

export default (props) => {

  const [timeLeft, { start, pause, resume, reset }] = useCountDown(INITIAL_TIME, INTERVAL);
  const navigate = useNavigate();

  // api action
  const [action, setAction] = useState(0);
  // submit state
  const [submitLoading, setSubmitLoading] = useState(false);
  const [disabledSubmit, setDisabledSubmit] = useState(true);
  const [sendCodeLoading, setSendCodeLoading] = useState(false);
  const [passwordField, setPasswordField] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  // email
  const [email, setEmail] = useState('');

  const handleEmailChange = useCallback((e) => {
    console.log('--value--\n', e.target.value);
    setEmail(e.target.value);
  }, []);

  const handleSubmit = useCallback(async (event, sendingCode = false) => {
    event.preventDefault();
    let formData;
    if (!sendingCode) {
      formData = new FormData(event.currentTarget);
      console.log('--event.currentTarget--\n', formData.get('email'));
    }
    try {
      // set loading first if action = 0
      if (action === 0) {
        setSendCodeLoading(true);
        start();
      }
      const res = await actions.resetPassword({
        action: !sendingCode ? action : 0,
        username: email,
        ...!sendingCode ? {
          code: formData.get('code'),
          password: formData.get('password'),
        } : {},
      });
      console.log('--res--\n', res);
      if (action === 0) {
        setSendCodeLoading(true);
        setDisabledSubmit(false);
      }
      if (action === 1) {
        setPasswordField(true);
      }
      if (action === 2) {
        message.success('Reset password successfully!');
        navigate('/login');
      }
      setAction(prevState => prevState + 1);
    } catch (e) {
      if (action === 0) {
        setSendCodeLoading(false);
        setDisabledSubmit(true);
        reset();
        return;
      }
      if (action === 1) {
        message.error('Invalid verifying code, please try agian.');
        return;
      }
      message.error(e.name);
    }
  }, [action, email, navigate, reset, start]);

  useEffect(() => {
    if (timeLeft === 0) {
      setSendCodeLoading(false);
      reset();
    }
  }, [timeLeft]);

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
                  fullWidth
                  id="code"
                  label="Verify Code"
                  name="code"
                />
              </Grid>
              <Grid item xs={4}>
                <Button
                  disabled={sendCodeLoading}
                  fullWidth
                  variant="outlined"
                  onClick={(e) => handleSubmit(e, true)}
                >
                  {!sendCodeLoading ? 'Send Code' : `Resend in ${timeLeft / 1000} s`}
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Collapse in={passwordField}>
                  <FormControl fullWidth variant="outlined">
                    <InputLabel>Password</InputLabel>
                    <OutlinedInput
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      endAdornment={
                        <InputAdornment position="end">
                          <IconButton
                            aria-label="toggle password visibility"
                            onClick={() => setShowPassword(prevState => !prevState)}
                            onMouseDown={(e) => e.preventDefault()}
                            edge="end"
                          >
                            {showPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      }
                      label="Password"
                    />
                  </FormControl>
                </Collapse>
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
              {action === 2 ? 'Submit' : 'Verify'}
            </LoadingButton>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
