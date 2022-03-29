import React, { useCallback, useEffect, useState } from "react";
import { Layout, Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import _ from 'lodash';

import sidebarConfig from 'src/configure/sidebar';

const { SubMenu } = Menu;
const { Sider } = Layout;

const DEFAULT_SELECTED_KEYS = sidebarConfig[2].child[0].title;

const Sidebar = (props) => {
  const {} = props;

  const location = useLocation();
  const { pathname } = location;

  const [selectedKey, setSelectKey] = useState(DEFAULT_SELECTED_KEYS);

  useEffect(() => {
    setSelectKey(pathname);
  }, [pathname]);

  const handleClick = useCallback((e) => {
    setSelectKey(e.key);
  }, []);

  return (
    <Sider className="frame-sidebar" width={200}>
      <Menu
        mode="inline"
        defaultSelectedKeys={[DEFAULT_SELECTED_KEYS]}
        defaultOpenKeys={_.map(sidebarConfig, 'title')}
        selectedKeys={[selectedKey]}
        onClick={handleClick}
        style={{ height: '100%', borderRight: 0 }}
      >
        {
          _.map(sidebarConfig, (item) => {
            const { child, title, icon } = item;

            return (
              <SubMenu
                key={title}
                title={title}
                icon={icon}
              >
                {
                  _.map(child, (childItem) => (
                    <Menu.Item key={childItem.url}>
                      <Link to={childItem.url} replace={true}>
                        <span>{childItem.title}</span>
                      </Link>
                    </Menu.Item>
                  ))
                }
              </SubMenu>
            );
          })
        }
      </Menu>
    </Sider>
  );
};

export default Sidebar;
