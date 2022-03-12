import React from 'react';
import ReactDOM from 'react-dom';

import Layout from "./layout";

import 'antd/dist/antd.less';

const App = () => {
  return (
    <Layout />
  );
}

ReactDOM.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>,
  document.getElementById('root')
);
