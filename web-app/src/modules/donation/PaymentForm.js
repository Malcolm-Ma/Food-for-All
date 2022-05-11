/**
 * @file Donation payment form
 * @author Mingze Ma
 */

import { InputAdornment, Paper, TextField, Divider, FormControlLabel, Checkbox, Button } from "@mui/material";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ToggleButton from '@mui/material/ToggleButton';
import React, { useCallback, useEffect, useState } from "react";
import Typography from "@mui/material/Typography";
import _ from 'lodash';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';
import Box from "@mui/material/Box";
import moment from "moment";
import CryptoJS from 'crypto-js';
import { SECRET_KEY } from "src/constants/constants";
import actions from "src/actions";
import { message } from "antd";
import Alert from "@mui/material/Alert";
import Autocomplete from "@mui/material/Autocomplete";

const SAMPLE_DONATION = [4, 12, 24];

export default (props) => {
  const { projectDetail: originalProjectDetail, currency } = props;

  const { regionInfo, currencyList } = useSelector(state => state.global);
  const { userInfo } = useSelector(state => state.user);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [projectDetail, setProjectDetail] = useState(originalProjectDetail);
  const [donationType, setDonationType] = useState('monthly');
  const [donationCount, setDonationCount] = useState(SAMPLE_DONATION[0]);
  const [donationPrice, setDonationPrice] = useState(donationCount * projectDetail.price);
  const [customCount, setCustomCount] = useState('');
  const [formattedCurrencyList, setFormattedCurrencyList] = useState([]);
  const [currentCurrency, setCurrentCurrency] = useState({ label: '', value: '' });

  const [alert, setAlert] = useState(false);

  const handleDonationPrice = useCallback((e, value) => {
    if (value) {
      setDonationCount(value);
      setDonationPrice(_.ceil(value * projectDetail.price, 2));
    }
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

  const handlePlanChoose = useCallback((e, value) => {
    if (value) {
      setDonationType(value);
    }
  }, []);

  const handlePayment = useCallback(async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let plan = 0;
    if (donationType === 'monthly')
      plan = 1;
    // encode search params
    const params = {
      pid: _.get(projectDetail, 'pid'),
      first_name: data.get('first_name'),
      last_name: data.get('last_name'),
      email: data.get('email'),
      ttl: moment().add(3, 'h').toDate(),
      donation_count: donationCount,
      plan: plan,
    };

    // encode for share
    const secretStr = CryptoJS.AES.encrypt(JSON.stringify(params), SECRET_KEY);
    // also set token in local storage
    window.localStorage.setItem('pid', _.get(projectDetail, 'pid'));

    //encode for payment
    const returnUrl = window.location.origin + `/share?token=${encodeURIComponent(secretStr)}`;
    const cancelURL = window.location.origin + `/donation/${_.get(projectDetail, 'pid')}/?tips=1`;
    try {
      const payDetail = await actions.payByDonator({
        "pid": _.get(projectDetail, 'pid'),
        "num": _.toNumber(donationCount),
        "currency_type": currentCurrency.value,
        "plan": plan,
        "return_url": returnUrl,
        "cancel_url": cancelURL,
      });
      window.localStorage.setItem('p_id', _.get(payDetail, 'payment_id'));
      window.location.href = _.get(payDetail, 'payment_url');
    } catch (e) {
      message.error(e.name);
    }
  }, [currentCurrency.value, donationCount, donationType, projectDetail]);

  useEffect(() => {
    if (!_.isEmpty(currentCurrency.value)) {
      (async () => {
        const { project_info: projectInfo } = await actions.getProjectInfo({
          pid: originalProjectDetail.pid,
          currency_type: currentCurrency.value,
        });
        setProjectDetail(projectInfo);
        setDonationPrice(_.ceil(donationCount * projectInfo.price, 2));
      })();
    }
  }, [currentCurrency, originalProjectDetail.pid]);

  useEffect(() => {
    if (!_.isEmpty(userInfo) && _.get(userInfo, 'type') === 1) {
      setAlert(true);
    }
  }, [userInfo]);

  useEffect(() => {
    if (!_.isEmpty(currencyList)) {
      const thisList = _.map(currencyList, ({ label, value }) => {
        return { label: `${value} (${label})`, value };
      });
      setFormattedCurrencyList(thisList);
      const currentObj = _.find(
        currencyList,
        (item) => item.value === (currency || _.get(userInfo, 'currency_type') || _.get(regionInfo, 'currencyType'))
      );
      setCurrentCurrency({ label: `${currentObj.value} (${currentObj.label})`, value: currentObj.value })
    }
  }, [currency, currencyList, regionInfo, userInfo]);

  useEffect(() => {
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  return (
    <Container
      component="div"
      maxWidth="sm"
      sx={{ mb: 4, p: { xs: 0, sm: 2 } }}
    >
      {
        alert && <Alert severity="warning" sx={{ mb: -2 }} onClose={() => setAlert(false)}>
          Sorry, charities can not donate to a project directly.
          Please logout or login as a donor if you wish to donate.
        </Alert>
      }
      {
        projectDetail.status === 0 && <Alert severity="info" sx={{ mb: -2, mt: 6 }}>
          The project is preparing. To publish it, please start this project in the charity system.
        </Alert>
      }
      {
        projectDetail.status === 2 && <Alert severity="success" sx={{ mb: -2, mt: 6 }}>
          This project has completed donating. You can no longer donate to it.
        </Alert>
      }
      <Paper
        variant="outlined"
        sx={{ my: { xs: 3, md: 6 }, p: { xs: 1, md: 3 } }}
      >
        <Box component="form" onSubmit={handlePayment} sx={{ mt: 1 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <ToggleButtonGroup
                color="primary"
                exclusive={true}
                fullWidth={true}
                value={donationType}
                onChange={handlePlanChoose}
              >
                <ToggleButton value="monthly">
                  GIVE MONTHLY
                </ToggleButton>
                <ToggleButton value="once">
                  GIVE ONCE
                </ToggleButton>
              </ToggleButtonGroup>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body1" align="center">
                You are about to {donationType === 'once' ? 'give once'
                : <span>become a monthly supporter, for <b>12 months</b></span>}
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Autocomplete
                disableClearable
                disablePortal
                fullWidth
                id="currency"
                options={formattedCurrencyList}
                value={currentCurrency}
                onChange={(e, value) => setCurrentCurrency(value)}
                renderInput={(params) => <TextField
                  {...params}
                  label="Select Currency"
                />}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography
                variant="h6"
                align="center"
                sx={{
                  padding: 2,
                  borderRadius: '4px',
                  backgroundColor: '#72b1dc',
                  color: '#fff',
                }}>
                Price Per Meal: {currentCurrency.value} {_.get(projectDetail, 'price')}<br />
              </Typography>
            </Grid>
            <Grid item xs={12}>
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
            <Grid item xs={12}>
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
            <Grid item xs={12}>
              <Typography variant="h6" align="center" color="rgba(0, 0, 0, 0.6)">
                Total Donation Price: <b>{currentCurrency.value} {donationPrice}</b>
              </Typography>
            </Grid>
          </Grid>
          <Divider sx={{ mt: 3, mb: 3, }} />
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h5" align="center">
                YOUR CONTACT DETAIL
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <TextField id="email" name="email" label="Email Address" variant="outlined" fullWidth={true} />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={<Checkbox value="anonymously" color="primary" />}
                label="Yes, I would like to donate anonymously."
              />
            </Grid>
            <Grid item xs={6}>
              <TextField id="first_name" name="first_name" label="First Name" variant="outlined" fullWidth={true} />
            </Grid>
            <Grid item xs={6}>
              <TextField id="last_name" name="last_name" label="Last Name" variant="outlined" fullWidth={true} />
            </Grid>
          </Grid>
          <Divider sx={{ mt: 3, mb: 3 }} />
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h5" align="center">
                CHOOSE YOUR PAYMENT METHOD
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Button
                disabled={(!_.isEmpty(userInfo) && _.get(userInfo, 'type') === 1) || projectDetail.status !== 1}
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
