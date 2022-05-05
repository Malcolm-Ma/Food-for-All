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

const SAMPLE_DONATION = [4, 12, 24];

export default (props) => {
  const { projectDetail } = props;

  const { regionInfo } = useSelector(state => state.global);

  const navigate = useNavigate();

  const [donationType, setDonationType] = useState('monthly');
  const [donationCount, setDonationCount] = useState(SAMPLE_DONATION[0]);
  const [donationPrice, setDonationPrice] = useState(0);
  const [manualPrice, setManualPrice] = useState(''); // Other amount

  const [showTips, setShowTips] = useState(true);

  const handleDonationPrice = useCallback((e, value) => {
    setDonationCount(value);
    setDonationPrice(_.ceil(value * projectDetail.price, 2));
    setManualPrice('');
    setShowTips(true);
  }, [projectDetail.price]);

  const handleManualPriceChange = useCallback((e) => {
    setManualPrice(e.target.value);
    if (_.isEmpty(e.target.value)) {
      setShowTips(true);
      setDonationCount(SAMPLE_DONATION[0]);
    } else {
      setShowTips(false);
      setDonationCount(0);
    }
  }, []);

  const handlePayment = useCallback((event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log('--data--\n', {
      email: data.get('email'),
      first_name: data.get('first_name'),
      last_name: data.get('last_name'),
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

    navigate(`/share?token=${encodeURIComponent(secretStr)}`);
  }, [navigate, projectDetail]);

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
              You are about to {donationType === 'once' ? 'give once' : 'become a monthly supporter'}
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
                const price = _.ceil(projectDetail.price * value, 2);
                return (
                  <ToggleButton key={value} value={value}>
                    <Typography variant="body1" fontWeight="bold">GBP {price}</Typography>
                  </ToggleButton>
                )
              })}
            </ToggleButtonGroup>
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
                display: !showTips && 'none',
              }}>
              Could provide vital emergency meals for {donationCount} hungry people, every month
            </Typography>
          </Grid>
          <Grid item sm={12}>
            <TextField
              name="amount"
              value={manualPrice}
              onChange={handleManualPriceChange}
              fullWidth
              label="Other Amount"
              InputProps={{
                startAdornment: <InputAdornment position="start">{regionInfo.currencyType}</InputAdornment>,
              }}
            />
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
