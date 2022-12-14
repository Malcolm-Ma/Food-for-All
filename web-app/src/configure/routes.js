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
    path: '/home',
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
    charity: true,
    exact: true,
  },
  {
    path: '/charity/project/list',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'charity' */ /* webpackMode: 'lazy' */ 'src/modules/charity/project/list'),
      loading: Loading,
    }),
    charity: true,
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
    charity: true,
    exact: true,
  },
  {
    path: '/project',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'project' */ /* webpackMode: 'lazy' */ 'src/modules/project/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/share',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'share' */ /* webpackMode: 'lazy' */ 'src/modules/share/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/payFailed',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'payFiled' */ /* webpackMode: 'lazy' */ 'src/modules/payFailed/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/donation/:pid',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'donation' */ /* webpackMode: 'lazy' */ 'src/modules/donation/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/donation/:pid/:currency',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'donation' */ /* webpackMode: 'lazy' */ 'src/modules/donation/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/account/charity_profile/:uid',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'account' */ /* webpackMode: 'lazy' */ 'src/modules/account/charityProfile/index.js'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/income/summary',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'income' */ /* webpackMode: 'lazy' */ 'src/modules/dashboard/incomeSummary/index.js'),
      loading: Loading,
    }),
    charity: true,
    exact: true,
  },
  {
    path: '/charity/account/profile',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'account' */ /* webpackMode: 'lazy' */ 'src/modules/account/profile'),
      loading: Loading,
    }),
    charity: true,
    exact: true,
  },
  {
    path: '/reset-password',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'reset-password' */ /* webpackMode: 'lazy' */ 'src/modules/resetPassword'),
      loading: Loading,
    }),
    exact: true,
  },
  {
    path: '/income/donation',
    component: loadable({
      loader: () => import(/* webpackChunkName: 'income' */ /* webpackMode: 'lazy' */ 'src/modules/charity/donationHistory/index.js'),
      loading: Loading,
    }),
    charity: true,
    exact: true,
  },
];
