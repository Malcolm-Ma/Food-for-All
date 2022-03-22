/**
 * @file Main entrance
 * @author Mingze Ma
 */

import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import ReactDOM from 'react-dom';
import thunk from 'redux-thunk';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';

import Layout from "src/layout";
import rootReducer from 'src/reducers';

import 'antd/dist/antd.less';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const composeEnhancers = typeof window === 'object' && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
  ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
    // Specify extension’s options like name, actionsBlacklist, actionsCreators, serialize...
  }) : compose;

const store = createStore(rootReducer, composeEnhancers(applyMiddleware(thunk)));

const App = () => {
  return (
    <Provider store={store}>
      <BrowserRouter basename="/">
        <Layout/>
      </BrowserRouter>
    </Provider>
  );
}

ReactDOM.render(<App/>, document.getElementById('root'));
