import React, { useEffect, useMemo } from 'react';
import { Layout as AntdLayout } from 'antd';
import { useLocation } from 'react-router-dom';
import _ from 'lodash';
import { useDispatch, useSelector } from "react-redux";

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
  const userInfo = useSelector(state => state.user.userInfo);

  const { pathname } = location;

  const sidebarHidingStatus = useMemo(() => _.some(
    layoutConfig.hideSidebar,
    item => item.test(pathname)
  ), [pathname]);

  useEffect(() => {
    dispatch(actions.getUserInfo()).catch(err => console.error(err));
  }, [dispatch]);

  const initStatus = useMemo(() => {
    return !_.isNil(_.get(userInfo, 'isLoggedIn'));
  }, [userInfo]);

  return (
    <div className="ffa-frame">
      {
        initStatus
          ? <>
            <Header />
            <AntdLayout>
              {!sidebarHidingStatus && <Sidebar />}
              <AntdLayout className="frame-content">
                <Main />
              </AntdLayout>
            </AntdLayout>
          </>
          : <div></div>
      }
    </div>
  );
};

export default Layout;
