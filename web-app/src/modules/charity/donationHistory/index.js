import _ from "lodash";
import {Table} from "antd";

const columnsConfig = [
  {
    title: 'Project Title',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: 'Time',
    dataIndex: 'time',
    key: 'time',
  },
  {
    title: 'Donor',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Number of Meals',
    dataIndex: 'donate_num',
    key: 'donate_num',
  }
  ]

export default () => {
  return (
    <Table
      columns={columnsConfig}
      rowKey={record => record.pid}
      // dataSource={}
    />
  )
}