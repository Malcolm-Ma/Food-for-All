/**
 * @file Donation payment form
 * @author Mingze Ma
 */

import { InputAdornment, Paper, TextField, Divider, FormControlLabel, Checkbox, Button } from "@mui/material";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ToggleButton from '@mui/material/ToggleButton';
import { useCallback, useState } from "react";
import Typography from "@mui/material/Typography";
import _ from 'lodash';
import { useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';
import Box from "@mui/material/Box";
import moment from "moment";
import CryptoJS from 'crypto-js';
import { SECRET_KEY } from "src/constants/constants";
import actions from "src/actions";
import {message} from "antd";

const SAMPLE_DONATION = [4, 12, 24];

export default (props) => {
  const { projectDetail } = props;

  const { regionInfo } = useSelector(state => state.global);

  const navigate = useNavigate();

  const [donationType, setDonationType] = useState('monthly');
  const [donationCount, setDonationCount] = useState(SAMPLE_DONATION[0]);
  const [donationPrice, setDonationPrice] = useState(donationCount * projectDetail.price);
  const [customCount, setCustomCount] = useState('');

  const handleDonationPrice = useCallback((e, value) => {
    setDonationCount(value);
    setDonationPrice(_.ceil(value * projectDetail.price, 2));
  }, [projectDetail.price]);

  const handleCustomCountChange = useCallback((e) => {
    const { value } = e.target
    setCustomCount(value);
    if (_.isEmpty(value)) {
      handleDonationPrice(null, SAMPLE_DONATION[0]);
    } else {
      handleDonationPrice(null, value);
    }
  }, [handleDonationPrice]);

  const handlePayment = useCallback(async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let plan = 0;
    if (donationType === 'monthly')
      plan = 1;
    console.log('--data--\n', {
      email: data.get('email'),
      first_name: data.get('first_name'),
      last_name: data.get('last_name'),
      plan: plan,
      donation_count: donationCount,
    });
    // encode search params
    const params = {
      pid: _.get(projectDetail, 'pid'),
      first_name: data.get('first_name'),
      last_name: data.get('last_name'),
      email: data.get('email'),
      ttl: moment().add(5, 'm').toDate(),
    };

    // encode for share
    const secretStr = CryptoJS.AES.encrypt(JSON.stringify(params), SECRET_KEY);
    // also set token in local storage
    window.localStorage.setItem('share_pid', _.get(projectDetail, 'pid'));

    //navigate(`/share?token=${encodeURIComponent(secretStr)}`);

    //encode for payment
    try {
      const payDetail = await actions.payByDonator({
        "pid": _.get(projectDetail, 'pid'),
        "num": donationCount,
        "currency_type": regionInfo.currencyType,
        "plan": plan,
        "return_url": window.location.origin + `/share?token=${encodeURIComponent(secretStr)}`,
        "cancel_url": window.location.origin + `/share?token=${encodeURIComponent(secretStr)}`,
      });
      console.log(payDetail);

      navigate('/'+'/'+_.get(payDetail,'payment_url'));

      //encode for payment check
      const payResult = await actions.capturePayment({
        "pid": _.get(projectDetail, 'pid'),
        "num": donationCount,
        "payment_id": _.get(payDetail, 'payment_id'),
        "plan": plan,
      })
    } catch (e) {
      message.error(e);
    }
  }, [donationCount, donationType, navigate, projectDetail]);

  return (
    <Container
      component="div"
      maxWidth="sm"
      sx={{ mb: 4, paddingRight: '0 !important' }}
    >
      <Paper
        variant="outlined"
        sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}
      >
        <Box component="form" onSubmit={handlePayment} sx={{ mt: 1 }}>
        <Grid container spacing={3}>
          <Grid item sm={12}>
            <ToggleButtonGroup
              color="primary"
              exclusive={true}
              fullWidth={true}
              value={donationType}
              onChange={(e, value) => setDonationType(value)}
            >
              <ToggleButton value="monthly">
                GIVE MONTHLY
              </ToggleButton>
              <ToggleButton value="once">
                GIVE ONCE
              </ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          <Grid item sm={12}>
            <Typography variant="body1" align="center">
              You are about to {donationType === 'once' ? 'give once'
              : <span>become a monthly supporter, for <b>12 months</b></span>}
            </Typography>
          </Grid>
          <Grid item sm={12}>
            <Typography
              variant="h6"
              align="center"
              sx={{
                padding: 2,
                borderRadius: '4px',
                backgroundColor: '#72b1dc',
                color: '#fff',
              }}>
              Price Per Meal: {regionInfo.currencyType} {_.get(projectDetail, 'price')}<br/>
            </Typography>
          </Grid>
          <Grid item sm={12}>
            <ToggleButtonGroup
              className="price-group"
              color="primary"
              exclusive={true}
              fullWidth={true}
              value={donationCount}
              onChange={handleDonationPrice}
            >
              {_.map(SAMPLE_DONATION, (value) => {
                return (
                  <ToggleButton key={value} value={value}>
                    <Typography variant="body1" fontWeight="bold">{value} MEALS</Typography>
                  </ToggleButton>
                )
              })}
            </ToggleButtonGroup>
          </Grid>
          <Grid item sm={12}>
            <TextField
              value={customCount}
              onChange={handleCustomCountChange}
              name="amount"
              fullWidth
              label="Other Amount"
              InputProps={{
                endAdornment: <InputAdornment position="end">MEAL(S)</InputAdornment>,
              }}
            />
          </Grid>
          <Grid item sm={12}>
            <Typography variant="h6" align="center" color="rgba(0, 0, 0, 0.6)">
              Total Donation Price: <b>{regionInfo.currencyType} {donationPrice}</b>
            </Typography>
          </Grid>
        </Grid>
        <Divider sx={{ mt: 3, mb: 3, }} />
        <Grid container spacing={2}>
          <Grid item sm={12}>
            <Typography variant="h5" align="center">
              YOUR CONTACT DETAIL
            </Typography>
          </Grid>
          <Grid item sm={12}>
            <TextField id="email" name="email" label="Email Address" variant="outlined" fullWidth={true} />
          </Grid>
          <Grid item xs={12}>
            <FormControlLabel
              control={<Checkbox value="anonymously" color="primary" />}
              label="Yes, I would like to donate anonymously."
            />
          </Grid>
          <Grid item sm={6}>
            <TextField id="first_name" name="first_name" label="First Name" variant="outlined" fullWidth={true} />
          </Grid>
          <Grid item sm={6}>
            <TextField id="last_name" name="last_name" label="Last Name" variant="outlined" fullWidth={true} />
          </Grid>
        </Grid>
        <Divider sx={{ mt: 3, mb: 3 }} />
        <Grid container spacing={2}>
          <Grid item sm={12}>
            <Typography variant="h5" align="center">
              CHOOSE YOUR PAYMENT METHOD
            </Typography>
          </Grid>
          <Grid item sm={12}>
            <Button
              variant="outlined"
              fullWidth
              endIcon={
                <img
                  src="https://libs.iraiser.eu/images/pictos/logo_paypal.png"
                  alt="paypal"
                  height="24px"
                />
              }
              type="submit"
            >
              DONATE BY PAYPAL
            </Button>
          </Grid>
        </Grid>
        </Box>
      </Paper>
    </Container>
  );
}
