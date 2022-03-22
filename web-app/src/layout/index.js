import React, { useEffect, useMemo } from 'react';
import { Layout as AntdLayout } from 'antd';
import { useLocation } from 'react-router-dom';
import _ from 'lodash';
import { useDispatch } from "react-redux";

import layoutConfig from 'src/configure/layout';
import actions from "src/actions";

import Header from './Header';
import Sidebar from "./Sidebar";
import Main from "./Main";

import './index.less';

const Layout = (props) => {
  const {} = props;

  const dispatch = useDispatch();
  const location = useLocation();

  const { pathname } = location;

  const sidebarHidingStatus = useMemo(() => _.some(
    layoutConfig.hideSidebar,
    item => item.test(pathname)
  ), [pathname]);

  useEffect(() => {
    dispatch(actions.getUserInfo()).catch(err => console.error(err));
  }, [dispatch]);


  return (
    <AntdLayout className="ffa-frame">
      <Header />
      <AntdLayout>
        {!sidebarHidingStatus && <Sidebar/>}
        <AntdLayout className="frame-content">
          <Main/>
        </AntdLayout>
      </AntdLayout>
    </AntdLayout>
  );
};

export default Layout;
