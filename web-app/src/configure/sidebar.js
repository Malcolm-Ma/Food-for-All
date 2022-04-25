/**
 * @file sidebar config
 * @author Mingze Ma
 */

import { UserOutlined, UnorderedListOutlined, LineChartOutlined } from "@ant-design/icons";

export default [
  {
    title: 'Project',
    icon: <UnorderedListOutlined />,
    child: [
      {
        title: 'Project List',
        url: '/charity/project/list',
      },
      {
        title: 'Create Project',
        url: '/charity/project/create',
      }
    ],
  },
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
    icon: <LineChartOutlined />,
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
];
