/**
 * @file project card container as list
 * @author Mingze Ma
 */
/**
 export default (props) => {
  const {} = props;

  return (
    <div>
      See in /material-kit-react/src/sections/@dashboard/products/ProductList.js
    </div>
  );
}
 */
import PropTypes from 'prop-types';
// material
import { Grid } from '@mui/material';
import ShowProjectCard from './ProjectCard';
import { useState } from "react";

import './index.less';
// ----------------------------------------------------------------------

ProjectList.propTypes = {
  projects: PropTypes.array.isRequired
};
export default function ProjectList(props) {
  const { projects, currencyType } = props;
  return (
    <Grid container spacing={3}>
      {projects.map((project, index) => (
        <Grid key={index} item xs={12} sm={6} md={3} alignItems="flex-start" zeroMinWidth>
          <ShowProjectCard currencyType={currencyType} project={project} />
        </Grid>
      ))}
    </Grid>
  );
}
