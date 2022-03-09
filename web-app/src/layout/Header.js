import React from 'react';
import { Layout } from 'antd';

const { Header: AntdHeader } = Layout;

const Header = (props) => {
  const {} = props;

  return (
    <AntdHeader className="ffa-nav">
      <div className="nav-logo">
        Food For All
      </div>
    </AntdHeader>
  );
};

export default Header;
