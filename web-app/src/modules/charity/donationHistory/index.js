import _ from "lodash";
import { message, Table } from "antd";
import { useEffect, useState } from "react";
import actions from "src/actions";
import moment from "moment";
import { useSelector } from "react-redux";

const columnsConfig = [
  {
    title: 'Project Title (ID)',
    dataIndex: 'project_title',
    fixed: 'left',
    render: (text, record) => {
      const pid = record.pid;
      return (
        <>
          <a
            href={`/donation/${pid}`}
            target="_blank"
            style={{fontSize: '16px'}}
          >{text}</a>
          <p style={{color: "rgba(0, 0, 0, 0.3)", fontSize: '12px'}}>{pid}</p>
        </>
      );
    },
  },
  {
    title: 'Time',
    dataIndex: 'time',
  },
  {
    title: 'Donor',
    dataIndex: 'name',
  },
  {
    title: 'Donor Email',
    dataIndex: 'mail',
    render: (text) => {
      return (
        <p>{text || '-'}</p>
      );
    },
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

export default () => {

  const regionInfo = useSelector(state => state.global.regionInfo);
  const { userInfo } = useSelector(state => state.user);

  const [dataSource, setDataSource] = useState([]);
  const [loading, setLoading] = useState(true);

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
                  time: moment(_.toNumber(time) * 1000).format('MMMM Do YYYY, h:mm:ss a'),
                  donate_num: _.toNumber(num),
                  donate_amount: (_.toNumber(num) * projectInfo.price).toFixed(2) + ' ' + userInfo.currency_type,
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
    if (!_.isEmpty(dataSource)){
      setLoading(false);
    }
  }, [dataSource]);

  return (
    <div>
      <Table
        columns={columnsConfig}
        rowKey={record => record.key}
        dataSource={dataSource}
        loading={loading}
        scroll={{ x: 1500 }}
      />
    </div>

  )
}

