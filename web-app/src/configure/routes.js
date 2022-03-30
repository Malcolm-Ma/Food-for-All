/**
 * @file route config
 * @author Mingze Ma
 */

import loadable from 'react-loadable';
import { Spin } from "antd";

const Loading = () => <Spin size="large"/>

export default [
  {
    path: '/',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'home' */ /* webpackMode: 'lazy' */ 'src/modules/home'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/charity',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'home' */ /* webpackMode: 'lazy' */ 'src/modules/home'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/login',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'login' */ /* webpackMode: 'lazy' */ 'src/modules/login'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/register',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'register' */ /* webpackMode: 'lazy' */ 'src/modules/register'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/charity/project/create',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'charity' */ /* webpackMode: 'lazy' */ 'src/modules/charity/project/create'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/charity/project/list',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'charity' */ /* webpackMode: 'lazy' */ 'src/modules/charity/project/list'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/account/profile',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'account' */ /* webpackMode: 'lazy' */ 'src/modules/account/profile'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/charity/project/create/result',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'charity' */ /* webpackMode: 'lazy' */ 'src/modules/charity/project/create/Result.js'),
      loading: Loading,
    }),
    exact: true,
  },
];
