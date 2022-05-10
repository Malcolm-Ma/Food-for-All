/**
 * @file donate history
 * @author Mingze Ma
 */

import { useEffect, useMemo, useState } from 'react';
import { Drawer, Button, Space } from 'antd';
import { useSelector } from "react-redux";
import _ from 'lodash';

import actions from "src/actions";
import moment from "moment";

export default (props) => {
  const { visible: visibleProps = false, pid = '', onClose: customOnClose } = props;

  const regionInfo = useSelector(state => state.global.regionInfo);

  const [visible, setVisible] = useState(visibleProps);

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
        const {project_info: projectInfo} = await actions.getProjectInfo({
          pid,
          currency_type: regionInfo.currencyType,
        });
        const donationHistory = _.get(projectInfo, 'donate_history', []);
        const historyDetail = [];
        _.map(donationHistory, async (value, uid) => {
          let result = {};
          console.log('--value, key--\n', value, uid);
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
            console.log('--res--\n', userRes);
            result = {
              ...result,
              ...otherProps,
            };
          }
          _.map(value, (num, time) => {
            historyDetail.push({
              ...result,
              time: moment(_.toNumber(time) * 1000).format(),
            });
          });
        })
      })();
    }
  }, [pid, regionInfo.currencyType]);

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
    </Drawer>
  );
};
