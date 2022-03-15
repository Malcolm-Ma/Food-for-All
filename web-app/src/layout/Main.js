/**
 * @file main container
 * @author Mingze Ma
 */

import React from "react";
import { Routes ,Route } from 'react-router-dom';
import _ from "lodash";
import { Form, Input, Button, Checkbox } from 'antd';

import actions from "src/actions";
import routesConfig from "src/configure/routes";

export default (props) => {
  const {} = props;

  return (
    <div className="ffa-main">
    <Routes>
        {
          _.map(routesConfig, (route) => {
            const { path, component: Component, ...otherProps } = route;
            return (
              <Route
                key={path}
                path={path}
                element={<Component />}
                {...otherProps}
              />
            );
          })
        }
      </Routes>
    </div>
  );
};
