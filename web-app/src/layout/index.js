import React, { useMemo } from 'react';
import { Layout as AntdLayout } from 'antd';
import { useLocation } from 'react-router-dom';
import _ from 'lodash';

import Header from './Header';
import Sidebar from "./Sidebar";
import Main from "./Main";

import layoutConfig from 'src/configure/layout';

import 'antd/dist/antd.less';
import './index.less';

const Layout = (props) => {
  const {} = props;

  const location = useLocation();

  const { pathname } = location;

  const sidebarHidingStatus = useMemo(() => _.some(
    layoutConfig.hideSidebar,
    item => item.test(pathname)
  ), [pathname])

  return (
    <AntdLayout className="ffa-frame">
      <Header/>
      <AntdLayout>
        {!sidebarHidingStatus && <Sidebar/>}
        <AntdLayout style={{ padding: '24px' }}>
          <AntdLayout.Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: '#ffffff',
            }}
          >
            <Main/>
          </AntdLayout.Content>
        </AntdLayout>
      </AntdLayout>
    </AntdLayout>
  );
};

export default Layout;
