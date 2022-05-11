/**
 * @file sidebar config
 * @author Mingze Ma
 */

import { UserOutlined, UnorderedListOutlined, LineChartOutlined } from "@ant-design/icons";
import actions from "src/actions";

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
        title: 'Donation History',
        url: '/income/donation',
      },
      {
        title: 'Download Report',
        onCLick: async () => {
          try {
            await actions.getReport();
          } catch (e) {
            console.error(e.name);
          }
        },
      },
      {
        title: 'Income Summary',
        url: '/income/summary',
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
