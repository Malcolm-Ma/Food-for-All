import _ from "lodash";
import { message, Table } from "antd";
import { useEffect, useState } from "react";
import actions from "src/actions";
import moment from "moment";
import { useSelector } from "react-redux";

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

  const regionInfo = useSelector(state => state.global.regionInfo);
  const { userInfo } = useSelector(state => state.user);

  const [dataSource, setDataSource] = useState([]);

  useEffect(() => {
    if (!_.isEmpty(userInfo)) {
      const fetchData = async () => {
        try {
          const userDonateHistory = _.get(userInfo, 'donate_history');
          let projectHistoryDetail = [];
          const projectPromiseAll = _.map(userDonateHistory, async (history, pid) => {
            const { project_info: projectInfo } = await actions.getProjectInfo({
              pid,
              currency_type: regionInfo.currencyType,
            });
            const donationHistory = _.get(projectInfo, 'donate_history', []);
            const fetchUserPromise = _.map(donationHistory, async (value, uid) => {
              let result = {};
              if (_.isEqual(uid, 'Anonymous')) {
                _.set(result, 'name', 'Anonymous');
              } else {
                const { user_info: userRes } = await actions.getUserInfoById({ uid });
                const { donate_history, project, type, ...otherProps } = userRes;
                result = {
                  ...result,
                  ...otherProps,
                };
              }
              _.map(value, (num, time) => {
                projectHistoryDetail.push({
                  ...result,
                  timestamp: _.toNumber(time) * 1000,
                  time: moment(_.toNumber(time) * 1000).format(),
                  donate_num: _.toNumber(num),
                  donate_amount: _.toNumber(num) * projectInfo.price,
                  project_title: projectInfo.title,
                  project_per_price: projectInfo.price,
                  pid: projectInfo.pid,
                  project_status: projectInfo.status,
                  project_intro: projectInfo.intro,
                });
              });
            });
            await Promise.all(fetchUserPromise);
          });
          await Promise.all(projectPromiseAll).then(() => {
            projectHistoryDetail = _.map(projectHistoryDetail, (item, key) => ({ ...item, key }))
            setDataSource(_.sortBy(projectHistoryDetail, (o) => -o.timestamp));
          });
        } catch (e) {
          message.error(e.name);
        }
      };
      fetchData();
    }
  }, [userInfo, regionInfo.currencyType]);

  useEffect(() => {
    console.log('--dataSource--\n', dataSource);
  }, [dataSource]);

  return (
    <Table
      columns={columnsConfig}
      rowKey={record => record.pid}
      // dataSource={}
    />
  )
}

