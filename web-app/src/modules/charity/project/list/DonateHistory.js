/**
 * @file donate history
 * @author Mingze Ma
 */

import { useEffect, useMemo, useState } from 'react';
import {Drawer, Button, Space, message, Table} from 'antd';
import { useSelector } from "react-redux";
import _ from 'lodash';

import actions from "src/actions";
import moment from "moment";

const columnsConfig = [
  {
    title: 'Time',
    dataIndex: 'time',
  },
  {
    title: 'Donor',
    dataIndex: 'name',
  },
  {
    title: 'Number of Meals',
    dataIndex: 'donate_num',
  },
  {
    title: 'Price',
    dataIndex: 'donate_amount',
  },
  ]

export default (props) => {
  const { visible: visibleProps = false, pid = '', onClose: customOnClose } = props;

  const {userInfo} = useSelector(state => state.user);

  const regionInfo = useSelector(state => state.global.regionInfo);

  const [visible, setVisible] = useState(visibleProps);

  const [dataSource, setDataSource] = useState([]);

  const onClose = () => {
    customOnClose();
    setVisible(false);
  };

  useEffect(() => {
    setVisible(visibleProps);
  }, [visibleProps])

  useEffect(() => {
    if (!!pid) {
      (async () => {
        try {
          const {project_info: projectInfo} = await actions.getProjectInfo({
            pid,
            currency_type: regionInfo.currencyType,
          });
          const donationHistory = _.get(projectInfo, 'donate_history', []);
          let historyDetail = [];
          const promiseAll = _.map(donationHistory, async (value, uid) => {
            let result = {};
            if (_.isEqual(uid, 'Anonymous')) {
              _.set(result, 'name', 'Anonymous');
            } else {
              const { user_info: userRes } = await actions.getUserInfoById({ uid });
              /**
               * avatar: "static/JEZgyvgE.jpg"
               * donate_history: {}
               * mail: "davisgregory@example.net"
               * name: "Richard Long"
               * project: []
               * region: "YE"
               * type: 2
               * uid: "db88231346b5333a8314a4f72bd3f314"
               */
              const { donate_history, project, type, ...otherProps } = userRes;
              result = {
                ...result,
                ...otherProps,
              };
            }
            let key = 0;
            _.map(value, (num, time) => {
              historyDetail.push({
                ...result,
                key,
                timestamp: _.toNumber(time) * 1000,
                time: moment(_.toNumber(time) * 1000).format('MMMM Do YYYY, h:mm:ss a'),
                donate_num: _.toNumber(num),
                donate_amount: (_.toNumber(num) * projectInfo.price).toFixed(2) + ' ' + userInfo.currency_type,
              });
              key = key + 1;
            });
          });
          await Promise.all(promiseAll).then(() => {
            historyDetail = _.map(historyDetail, (item, key) => ({...item, key}))
            setDataSource(_.sortBy(historyDetail, (o) => -o.timestamp));
          })
        } catch (e) {
          message.error(e.name);
        }
      })();
    }
  }, [pid, regionInfo.currencyType]);

  useEffect(() => {
    console.log('--dataSource--\n', dataSource);
  }, [dataSource]);

  const loading = useMemo(() => (_.isEmpty(pid)), [pid]);
  return (
    <Drawer
      title="Donate Hostory"
      placement="right"
      width={800}
      onClose={onClose}
      visible={visible}
      extra={
        <Space>
          {/*<Button onClick={onClose}>Cancel</Button>*/}
          <Button type="primary" onClick={onClose}>
            OK
          </Button>
        </Space>
      }
    >
      <Table
        columns={columnsConfig}
        rowKey={record => record.key}
        dataSource={dataSource}
      />
    </Drawer>
  );
};
