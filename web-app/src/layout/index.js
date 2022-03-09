import React from 'react';
import { Layout as AntdLayout } from 'antd';

import Header from './Header';
import Sidebar from "./Sidebar";

import 'antd/dist/antd.less';
import './index.less';

const Layout = (props) => {
  const {} = props;

  return (
    <AntdLayout className="ffa-main">
      <Header />
      <AntdLayout>
        <Sidebar />
      </AntdLayout>
    </AntdLayout>
  );
};

export default Layout;
