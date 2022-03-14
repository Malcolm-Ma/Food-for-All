import React from 'react';
import { Layout as AntdLayout } from 'antd';

import Header from './Header';
import Sidebar from "./Sidebar";
import Main from "./Main";

import 'antd/dist/antd.less';
import './index.less';

const Layout = (props) => {
  const {} = props;

  return (
    <AntdLayout className="ffa-frame">
      <Header/>
      <AntdLayout>
        <Sidebar/>
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
