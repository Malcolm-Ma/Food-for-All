/**
 * @file register
 * @author Mingze Ma
 */

import React, { useCallback, useEffect, useRef } from "react";
import { useNavigate } from 'react-router-dom';
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
import LoadingButton from '@mui/lab/LoadingButton';
import { message } from 'antd';
import { DEFAULT_CURRENCY } from 'src/constants/constants';
import { useMemo, useState } from "react";
import _ from 'lodash';

import EmailForm from "./EmailForm";
import VerifyForm from "./VerifyForm";
import DetailForm from './DetailForm'

import './index.less';
import actions from "../../actions";
import { encode } from "src/utils/encodePassword";
import { validateEmail } from "src/utils/utils";

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
  const navigate = useNavigate();

  const [activeStep, setActiveStep] = useState(0);
  const [signUpInfo, setSignUpInfo] = useState({});

  const [loading, setLoading] = useState(false);
  const [validEmail, setValidEmail] = useState(true);
  const [avatar, setAvatar] = useState('');

  const ActiveComponent = useMemo(() => {
    return STEP_CONFIG[activeStep].Component;
  }, [activeStep]);

  const handleSubmit = useCallback(async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    console.log('--data--\n', data);
    if (activeStep === 0 && !validateEmail(_.get(data, 'username'))) {
      setValidEmail(false);
      return;
    } else {
      setValidEmail(true);
    }
    setLoading(true);
    try {
      if (activeStep === 0) {
        const res = await actions.register({
          username: _.get(data, 'username'),
          action: activeStep,
        });
        setActiveStep(1);
      } else if (activeStep === 1) {
        const res = await actions.register({
          ...signUpInfo,
          action: activeStep,
          code: _.toUpper(_.get(data, 'code')),
        });
        setActiveStep(2);
      } else if (activeStep === 2) {
        await actions.register({
          ...signUpInfo,
          code: _.toUpper(_.get(signUpInfo, 'code')),
          action: activeStep,
          password: encode(_.get(data, 'password')),
          region: _.get(data, 'region'),
          currency_type: _.get(_.split(_.get(data, 'currency'), ' ('), '0', DEFAULT_CURRENCY),
          name: _.get(data, 'name'),
          avatar,
          hide: 0,
        });
        message.success('Welcome to Apex - Food For ALl!');
        navigate('/login');
      }
      setSignUpInfo(prevState => ({
        ...prevState,
        ...data,
      }));
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }, [activeStep, avatar, navigate, signUpInfo]);

  const handleActiveComponentChange = useCallback((e, data) => {
    setSignUpInfo(prevState => ({
      ...prevState,
      ...data,
    }))
  }, []);

  const activeComponentProps = useMemo(() => ({
    ...(activeStep === 0 && { btnLabel: "type", validEmail }),
    ...(activeStep === 2 && { setAvatar }),
    onChange: handleActiveComponentChange,
    username: _.get(signUpInfo, 'username', ''),
  }), [activeStep, handleActiveComponentChange, signUpInfo, validEmail]);
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
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
            {
              !loading
                ? <ActiveComponent {...activeComponentProps} />
                : <>
                  <Skeleton className="loading" />
                  <Skeleton className="loading" animation="wave" />
                  <Skeleton className="loading" animation={false} />
                </>
            }
            <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              {activeStep !== 0 && (
                <Button
                  onClick={() => setActiveStep(prevState => (prevState - 1))}
                  sx={{ mt: 3, mb: 2 }}
                >
                  Back
                </Button>
              )}
              <LoadingButton
                type="submit"
                variant="contained"
                loading={loading}
                sx={{ mt: 3, mb: 2 }}
              >
                {STEP_CONFIG[activeStep].submitLabel}
              </LoadingButton>
            </Box>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
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
