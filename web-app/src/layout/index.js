import React, { useEffect, useMemo } from 'react';
import { Layout as AntdLayout, message } from 'antd';
import { useLocation } from 'react-router-dom';
import _ from 'lodash';
import { useDispatch, useSelector } from "react-redux";
import classNames from "classnames";

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
  const regionInfo = useSelector(state => state.global.regionInfo);

  const { pathname } = location;

  const sidebarShowingStatus = useMemo(() => _.some(
    layoutConfig.showSidebar,
    item => item.test(pathname)
  ), [pathname]);

  useEffect(() => {
    dispatch(actions.getRegionInfo()).catch(err => console.error(err));
    dispatch(actions.getUserInfo()).catch(err => console.error(err));
  }, [dispatch]);

  const initStatus = useMemo(() => {
    return !_.isNil(_.get(userInfo, 'isLoggedIn')) && !_.isEmpty(regionInfo);
  }, [regionInfo, userInfo]);

  return (
    <div className="ffa-frame">
      {
        initStatus
          ? <>
            <Header />
            <AntdLayout className={
              classNames({
                'frame-content-with-sidebar': (sidebarShowingStatus && _.get(userInfo, 'type', 2) === 1),
              })
            }>
              {(sidebarShowingStatus && _.get(userInfo, 'type', 2) === 1) && <Sidebar />}
              <Main userInfo={userInfo} />
            </AntdLayout>
          </>
          : <div></div>
      }
    </div>
  );
};

export default Layout;
