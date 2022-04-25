/**
 * @file home page index
 * @author Mingze Ma
 */

import { ThemeProvider } from '@mui/material/styles';

import theme from "./theme";
import Hero from "./Hero";
import Instruction from "./Instruction";

import './index.less';

export default (props) => {
  const {} = props;

  return (
    <ThemeProvider theme={theme}>
      <div className="ffa-home">
        <Hero />
        <Instruction />
      </div>
    </ThemeProvider>
  );
};
