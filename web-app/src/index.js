import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import ReactDOM from 'react-dom';

import Layout from "src/layout";

import 'antd/dist/antd.less';

const App = () => {
  return (
    <BrowserRouter basename="/">
      <Layout/>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
