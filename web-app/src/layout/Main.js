/**
 * @file main container
 * @author Mingze Ma
 */

import React, { useEffect } from "react";
import { Routes ,Route } from 'react-router-dom';
import _ from "lodash";
import { Layout } from 'antd';

import routesConfig from "src/configure/routes";
import NoPermission from "src/components/NoPermission";

export default (props) => {
  const { userInfo } = props;

  return (
    <Layout className="frame-content-main">
      <Layout.Content className="ffa-main">
        <Routes>
          {
            _.map(routesConfig, (route) => {
              const { path, component: Component, charity = false, ...otherProps } = route;
              let component = <Component />;
              // When no access to charity admin system
              if (charity && _.get(userInfo, 'type', 2) !== 1) {
                component = <NoPermission key={path} />;
              }
              return (
                <Route
                  key={path}
                  path={path}
                  element={component}
                  {...otherProps}
                />
              );
            })
          }
        </Routes>
      </Layout.Content>
    </Layout>
  );
};
