/**
 * @file Project list page
 * @author Mingze Ma
 */
import { useCallback, useEffect, useState } from "react";
import { Space, Table, Progress } from 'antd';

import actions from "src/actions";
import _ from "lodash";

// Column config of a table
// Using either dataIndex or key to point out unique props
const columnsConfig = (functions) => {

  const {
    onDelete,
  } = functions;

  return [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      render: text => <a key={'title'}>{text}</a>,
    },
    {
      title: 'Introduction',
      dataIndex: 'intro',
      ellipsis: true,
    },
    {
      title: 'Price',
      dataIndex: 'price',
    },
    {
      title: 'Progress',
      key: 'Progress',
      width: 160,
      render: (text, record) => {
        const { current_num: currentNum, total_num: totalNum } = record;
        const percent = _.floor((currentNum / totalNum) * 100, 0);
        return (
          <Progress percent={percent} />
        );
      }
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <a>Invite {record.name}</a>
          <a>Delete</a>
        </Space>
      ),
    },
  ];
}

export default () => {

  const [projectInfo, setProjectInfo] = useState({});

  const getProjectList = useCallback(async () => {
    try {
      const res = await actions.getProjectList();
      console.log('--res--\n', res);
      const {
        project_info: rawProjectInfo,
        page_info: pageInfo,
        currency_type: currencyType,
        ...otherProps
      } = res;
      const projectInfo = _.values(rawProjectInfo);
      console.log('--projectInfo--\n', projectInfo);
      const result = {
        ...otherProps,
        projectInfo,
        pageInfo,
        currencyType,
      };
      console.log('--result--\n', result);
      setProjectInfo(result);
    } catch (e) {
      console.error(e);
    }
  }, []);

  useEffect(() => {
    getProjectList().catch(err => console.error(err));
  }, [getProjectList]);

  const onDelete = () => {

  };

  const customFunctions = {
    onDelete
  };
  return (
    <div>
      <Table
        columns={columnsConfig(customFunctions)}
        rowKey={record => record.pid}
        dataSource={_.get(projectInfo, 'projectInfo', [])}
      />
    </div>
  );

};
