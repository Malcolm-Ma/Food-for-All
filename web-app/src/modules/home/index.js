/**
 * @file home page index
 * @author Mingze Ma
 */

import {} from 'react';
import { ThemeProvider } from '@mui/material/styles';

import Hero from "./Hero";
import theme from "./theme";

import './index.less';

export default (props) => {
  const {} = props;

  return (
    <ThemeProvider theme={theme}>
      <div className="ffa-home">
        <Hero />
      </div>
    </ThemeProvider>
  );
};
