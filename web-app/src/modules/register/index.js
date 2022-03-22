/**
 * @file register
 * @author Mingze Ma
 */

import React, { useCallback, useEffect, useRef } from "react";
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Skeleton from '@mui/material/Skeleton';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';

import { useMemo, useState } from "react";
import _ from 'lodash';

import EmailForm from "./EmailForm";
import VerifyForm from "./VerifyForm";
import DetailForm from './DetailForm'

import './index.less';
import api from "../../api";
import actions from "../../actions";

const STEP_CONFIG = [
  {
    name: 'Enter Email',
    submitLabel: 'Next',
    Component: EmailForm,
  },
  {
    name: 'Verify Email',
    submitLabel: 'Verify',
    Component: VerifyForm,
  },
  {
    name: 'Enter Details',
    submitLabel: 'Submit',
    Component: DetailForm,
  }
];

const theme = createTheme();

export default () => {

  const [activeStep, setActiveStep] = useState(0);
  const [signUpInfo, setSignUpInfo] = useState({});
  const [loading, setLoading] = useState(true);

  const formRef = useRef(null);

  const ActiveComponent = useMemo(() => {
    return STEP_CONFIG[activeStep].Component;
  }, [activeStep]);

  const handleSubmit = useCallback(async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    if (activeStep === 0) {
      try {
        const res = await actions.register({
          username: _.get(data, 'email'),
          action: activeStep,
        });
        console.log('--res--\n', res);
        setActiveStep(1);
      } catch (e) {
        console.error(e);
      }
    }
    setSignUpInfo(prevState => ({
      ...prevState,
      ...data,
    }));
  }, [activeStep]);

  const handleActiveComponentChange = useCallback((e, data) => {
    setSignUpInfo(prevState => ({
      ...prevState,
      ...data,
    }))
  }, []);

  useEffect(() => {
    console.log('--signUpInfo--\n', signUpInfo);
  }, [signUpInfo]);

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="sm">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Box sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}>
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
          </Box>
          <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 3 }}>
            {_.map(STEP_CONFIG, ({ name }) => (
              <Step key={name}>
                <StepLabel>{name}</StepLabel>
              </Step>
            ))}
          </Stepper>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }} ref={formRef}>
            {
              !loading
                ? <ActiveComponent btnLabel="account_type" onChange={handleActiveComponentChange} />
                : <>
                  <Skeleton className="loading" />
                  <Skeleton className="loading" animation="wave" />
                  <Skeleton className="loading" animation={false} />
                </>
            }
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              {STEP_CONFIG[activeStep].submitLabel}
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="#" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
