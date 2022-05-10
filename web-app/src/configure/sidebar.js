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
    title: 'Income',
    icon: <LineChartOutlined />,
    child: [
      {
        title: 'Income Summary',
        url: '/income/summary',
      },
      {
        title: 'Download Report',
        url: '/income/report',
      },
    ],
  },
  {
    title: 'Account',
    icon: <UserOutlined />,
    child: [
      {
        title: 'Profile',
        url: '/charity/account/profile',
      },
    ],
  },
];
