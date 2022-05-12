/**
 * @file Hero Part
 * @author Mingze Ma
 */

import Button from '@mui/material/Button';
import Typography from './Typography';
import HeroLayout from './HeroLayout';

import homeImage1 from 'src/assets/home1.jpeg';
import homeImage2 from 'src/assets/home2.png';
import moment from "moment";

export default () => {
  const imageUrl = moment().millisecond() % 2 === 1 ? homeImage1 : homeImage2;

  return (
    <HeroLayout
      sxBackground={{
        backgroundImage: `url(${imageUrl})`,
        backgroundColor: '#7fc7d9', // Average color of the background image.
        backgroundPosition: 'center',
      }}
    >
      {/* Increase the network loading priority of the background image. */}
      <img
        style={{ display: 'none' }}
        src={imageUrl}
        alt="increase priority"
      />
      <Typography color="inherit" align="center" variant="h2" marked="center">
        APEX - FOOD FOR ALL
      </Typography>
      <Typography
        color="inherit"
        align="center"
        variant="h5"
        sx={{ mb: 4, mt: { sx: 4, sm: 10 } }}
      >
        Please help end hunger for good together
      </Typography>
      <Button
        color="secondary"
        variant="contained"
        size="large"
        component="a"
        href="/project"
        sx={{ minWidth: 200 }}
      >
        Donate Now
      </Button>
      <Typography variant="body2" color="inherit" sx={{ mt: 2 }}>
        Food Assistance
      </Typography>
    </HeroLayout>
  );
}
