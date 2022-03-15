import { UserOutlined } from "@ant-design/icons";
import React from "react";

/**
 * @file sidebar config
 * @author Mingze Ma
 */

export default [
  {
    title: 'Account',
    icon: <UserOutlined />,
    child: [
      {
        title: 'Profile',
        url: '/account/profile',
      },
    ],
  },
  {
    title: 'Income',
    icon: <UserOutlined />,
    child: [
      {
        title: 'Income Management',
        url: '/income/manage',
      },
      {
        title: 'Income Summary',
        url: '/income/summary',
      }
    ],
  },
  {
    title: 'Project',
    icon: <UserOutlined />,
    child: [
      {
        title: 'Project List',
        url: '/project/list',
      },
      {
        title: 'Create Project',
        url: '/project/create',
      }
    ],
  },
];
