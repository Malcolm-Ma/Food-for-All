/**
 * @file Project list page
 * @author Mingze Ma
 */
import { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from 'react-redux';
import moment from "moment";
import {
  Button,
  Progress,
  Modal,
  Table,
  Space,
  Drawer,
  Tag,
  Switch,
  Tooltip,
  message,
  Menu,
  Dropdown,
} from "antd";
import _ from "lodash";
import { getProjectInfo, getProjectList } from "src/actions/projectActions";
import {
  CheckCircleOutlined,
  SyncOutlined,
  ClockCircleOutlined,
  MinusCircleOutlined,
  DownOutlined,
  SmileOutlined,
} from '@ant-design/icons';

import actions from "src/actions";
import { DEFAULT_CURRENCY } from "src/constants/constants";

import EditDetail from "./EditDetail";
import DrawerDetail from './ProjectDetail';

import './index.less';
import DonateHistory from "src/modules/charity/project/list/DonateHistory";

// Column config of a table
// Using either dataIndex or key to point out unique props
const columnsConfig = (payloads) => {

  const {
    projectInfo,
    showDrawer,
    showModal,
    regionMap,
    prepareMode,
    handleDonationHistoryClick,
    downloadReport,
  } = payloads;

  return _.compact([
    {
      title: 'Project Title (ID)',
      dataIndex: 'title',
      width: 200,
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
      title: 'Introduction',
      dataIndex: 'intro',
      ellipsis: true,
      width: 160,
      render: value =>
        <Tooltip title={value}>
          <div style={{ float: 'left', maxWidth: '100%', cursor: 'pointer' }}>
            {value.substring(0, 12) + '...'}
          </div>
        </Tooltip>
    },
    {
      title: 'Status',
      key: 'tags',
      render: (text, record) => {
        const { status: status } = record;
        switch (status) {
          case 0:
            return (
              <div>
                <Tag icon={<ClockCircleOutlined />} color="warning">
                  Prepare
                </Tag>
              </div>
            );
          case 1:
            return (
              <div>
                <Tag icon={<SyncOutlined spin />} color="processing">
                  Ongoing
                </Tag>
              </div>
            );
          case 2:
            return (
              <div>
                <Tag icon={<CheckCircleOutlined />} color="success">
                  Complete
                </Tag>
              </div>
            );
          case 3:
            return (
              <div>
                <Tag icon={<MinusCircleOutlined />} color="warning">
                  Pause
                </Tag>
              </div>
            );
        }
      }
    },
    {
      title: 'Price per Meal',
      key: 'price',
      render: (text, record) => {
        const { price: price } = record;
        const realPrice = String(_.floor(price, 2));
        return (realPrice + ' ' + _.get(projectInfo, 'currencyType'));
      }
    },
    {
      title: 'Donation Progress',
      key: 'Progress',
      render: (text, record) => {
        const { current_num: currentNum, total_num: totalNum } = record;
        const percent = _.floor((currentNum / totalNum) * 100, 0);
        return (
          <Progress percent={percent} type="circle" width={60} />
        );
      }
    },
    {
      title: 'Number of Meals Donated',
      dataIndex: 'current_num',
      render: (text, record) => {
        const { total_num: totalNum } = record;
        return `${text} / ${totalNum}`;
      }
    },
    {
      title: 'Amount of Meals Donated',
      key: 'total_price',
      render: (text, record) => {
        const { price: price, current_num: currentNum } = record;
        const realPrice = _.floor(price, 2);
        const totalPrice = String(_.floor(realPrice * currentNum, 2)) + ' ' + projectInfo.currencyType;
        return totalPrice;
      }
    },
    {
      title: 'Country / Region',
      dataIndex: 'region',
      render: (text, record) => {
        const fullRegionName = _.get(regionMap, text);
        if (fullRegionName) {
          return `${fullRegionName}`;
        }
        return text;
      },
    },
    // @Todo prepared project don't have start time
    (!prepareMode && {
      title: 'Start Time',
      key: 'start_time',
      width: 130,
      render: (text, record) => {
        const { start_time: startTime } = record;
        const timeOfStart = moment(startTime * 1000).format("MMM DD, YYYY");
        return timeOfStart;
      }
    }),
    {
      title: 'End Time',
      key: 'end_time',
      width: 130,
      render: (text, record) => {
        const { end_time: endTime } = record;
        const timeOfEnd = moment(endTime * 1000).format("MMM DD, YYYY");
        return timeOfEnd;
      }
    },
    {
      title: 'Operations',
      key: 'action',
      width: 230,
      align: 'center',
      fixed: 'right',
      render: (text, record) => {
        const prepareBtns = [
          <Button type="link" onClick={() => showModal(record.pid, record.status, 'Start')}>Start</Button>,
          <Button type="link" onClick={() => showModal(record.pid, record.status, 'Delete')}>Delete</Button>

        ];
        const onGoingBtns = [
          <Button type="link" onClick={() => showModal(record.pid, record.status, 'Pause')}>Pause</Button>,
          <Button type="link" onClick={() => showModal(record.pid, record.status, 'Stop')}>Stop</Button>
        ];
        const currentButtons = (() => {
          if (record.status === 0) {
            return prepareBtns;
          }
          if (record.status === 1) {
            return onGoingBtns;
          }
          if (record.status === 3) {
            return [
              <Button type="link" onClick={() => showModal(record.pid, record.status, 'Continue')}>
                Continue
              </Button>
            ];
          }
          return [];
        })();
        const dropDownMenu = (
          <Menu
            items={_.map(currentButtons, item => ({label: item}))}
          />
        );
        return (
          <Space size={0}>
            <Button
              type="link"
              size="small"
              onClick={() => downloadReport(record.pid)}
              disabled={record.status === 0}
            >
              Report
            </Button>
            <Button
              type="link"
              size="small"
              onClick={(e) => handleDonationHistoryClick(e, record.pid)}
              disabled={record.status === 0}
            >
              History
            </Button>
            {
              record.status === 0
                ? <Button
                  type="link"
                  size="small"
                  onClick={() => showDrawer('edit', record.pid)}
                  disabled={record.status !== 0}
                >
                  Edit
                </Button>
                : <Button
                  type="link"
                  size="small"
                  onClick={() => showDrawer('detail', record.pid)}
                >
                  Detail
                </Button>
            }
            {record.status !== 2 && <Dropdown overlay={dropDownMenu}>
              <a onClick={e => e.preventDefault()} style={{paddingLeft: '7px'}}>
                <Space>
                  Actions
                  <DownOutlined />
                </Space>
              </a>
            </Dropdown>}
          </Space>
        );
      },
    }
  ]);
}

export default () => {

  const dispatch = useDispatch();

  const { regionMap } = useSelector(state => state.global);
  const { currencyList } = useSelector(state => state.global);
  const { userInfo } = useSelector(state => state.user);

  const [projectInfo, setProjectInfo] = useState({});

  const [prepareMode, setPrepareMode] = useState(false);
  const [drawerType, setDrawerType] = useState('');

  // projectDetailInfo state
  const [projectDetailInfo, setProjectDetailInfo] = useState({});

  const [operatingProject, setOperatingProject] = useState([]);

  const [drawVisible, drawSetVisible] = useState(false);
  //Edit button
  const [modalVisible, modalSetVisible] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [modalText, setModalText] = useState('Are you sure you want to terminate the project. '
    + 'Terminated projects cannot be continued.');
  const [titleText, setTitleText] = useState('');

  const [historyDrawer, setHistoryDrawer] = useState('');

  const getProjectList = useCallback(async () => {
    try {
      let res = {};
      if (prepareMode) {
        res = await actions.getPrepareProject();
      } else {
        res = await actions.getProjectList({
          currency_type: userInfo.currency_type || DEFAULT_CURRENCY,
          page_info: {
            page_size: 10000,
            page: 1
          },
          search: '',
          order: '',
          uid: userInfo.uid,
          valid_only: '',
        });
      }
      const {
        project_info: rawProjectInfo,
        page_info: pageInfo,
        currency_type: currencyType,
        ...otherProps
      } = res;
      const projectInfo = _.values(rawProjectInfo);
      const result = {
        ...otherProps,
        projectInfo,
        pageInfo,
        currencyType,
      };
      setProjectInfo(result);// To set projectInfo you need to use this
    } catch (e) {
      console.error(e);
    }
  }, [prepareMode, userInfo.currency_type]);

  useEffect(() => {
    dispatch(actions.getCurrencyList());
  }, [dispatch]);

  useEffect(() => {
    getProjectList().catch(err => console.error(err));
    dispatch(actions.getRegionList());
  }, [dispatch, getProjectList]);

  //Edit popup window
  const showDrawer = async (source, projectId) => {
    setDrawerType(source);
    try {
      const res = await getProjectInfo({
        "pid": projectId,
        "currency_type": _.get(projectInfo, 'currencyType'),
      });
      setProjectDetailInfo({
        ..._.get(res, 'project_info'),
        currencyType: _.get(projectInfo, 'currencyType'),
      });
      drawSetVisible(true);
    } catch (error) {
      console.log(error);
    }
  }

  const onClose = () => {
    drawSetVisible(false);
  };
  //Below is the delete button pop-up warning box
  const showModal = (projectId, status, action) => {
    if (status === 0 && action === 'Start') {
      // prepare mode
      setModalText('Are you sure you want to start the project? Once the project starts, it can\'t be edited, it can only be suspended or stopped.');
      setTitleText('Start Project');
    } else if (status === 0 && action === 'Delete') {
      // prepare mode
      setModalText('Are you sure you want to delete the item? Deleted items are not recoverable.');
      setTitleText('Delete Project');
    } else if (status === 1 && action === 'Stop') {
      // ongoing mode
      setModalText('Are you sure you want to terminate the project? The project cannot continue after termination.');
      setTitleText('Stop Project');
    } else if (status === 1 && action === 'Pause') {
      setModalText('Are you sure you want to suspend your project? Suspended projects can be restarted afterwards.');
      setTitleText('Pause Project');
    } else if (status === 3 && action === 'Continue') {
      setModalText('Are you sure you want to continue the project.');
      setTitleText('Continue Project');
    }
    setOperatingProject([projectId, status, action]);
    modalSetVisible(true);
  };

  const handleOk = async () => {
    const [projectId, status, action] = operatingProject;
    if ((status === 0 && action === 'Start') || status === 3) {
      // prepare mode
      setModalText('Start project.');
      setConfirmLoading(true);
      // TODO change to start project
      await actions.startProject({
        "pid": projectId,
      });
    } else if (status === 1 && action === 'Stop') {
      // ongoing mode
      setModalText('Terminating project.');
      setConfirmLoading(true);
      // TODO change to start project
      try {
        await actions.stopProject({
          "pid": projectId,
        });
      } catch (error) {
        modalSetVisible(false);
        message.error(error.name)
      }
    } else if (status === 1 && action === 'Pause') {
      // ongoing mode
      setModalText('Pausing project.');
      setConfirmLoading(true);
      // TODO change to start project
      try {
        await actions.suspendProject({
          "pid": projectId,
        });
      } catch (error) {
        modalSetVisible(false);
        message.error(error.name)
      }
    } else if (status === 0 && action === 'Delete') {
      // ongoing mode
      setModalText('Delete project.');
      setConfirmLoading(true);
      // TODO change to start project
      try {
        await actions.deleteProject({
          "pid": projectId,
        });
      } catch (error) {
        modalSetVisible(false);
        message.error(error.name)
      }
    }
    setTimeout(() => {
      modalSetVisible(false);
      setConfirmLoading(false);
    }, 200);
    setOperatingProject([]);
    getProjectList();
  };

  const handleCancel = () => {
    console.log('Clicked cancel button');
    modalSetVisible(false);
  };

  const handleModeChange = (checked) => {
    setPrepareMode(checked);
  };

  const handleDonationHistoryClick = useCallback((_e, pid) => {
    setHistoryDrawer(pid);
  }, []);

  const downloadReport = async (pid) => {
    await actions.getReport({
      pid: pid
    })
  }

  const payloads = {
    projectInfo,
    drawVisible,
    modalVisible,
    confirmLoading,
    modalText,
    regionMap,
    prepareMode,
    showDrawer,
    onClose,
    showModal,
    handleOk,
    handleCancel,
    handleDonationHistoryClick,
    downloadReport,
  };

  return (
    <div className="project-list">
      <div className="mode-switch">
        <Switch onChange={handleModeChange} />
        <span>Prepare Mode</span>
      </div>
      <Table
        columns={columnsConfig(payloads)}
        rowKey={record => record.pid}
        dataSource={_.get(projectInfo, 'projectInfo', [])}
        scroll={{ x: 1500 }}
      />
      <Drawer
        title="Project Detail Information"
        className='project-detail-drawer'
        placement="right"
        onClose={onClose}
        visible={drawVisible}
        bodyStyle={{ paddingBottom: 80 }}
        width={800}
        extra={
          <Space>
            <Button onClick={onClose}>Cancel</Button>
          </Space>
        }>
        {drawerType === 'detail' && <DrawerDetail detailInfo={projectDetailInfo} />}
        {drawerType === 'edit' && <EditDetail targetProject={projectDetailInfo} />}
      </Drawer>
      <Modal
        title={titleText}
        visible={modalVisible}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
      >
        <p>{modalText}</p>
      </Modal>
      <DonateHistory visible={!_.isEmpty(historyDrawer)} pid={historyDrawer} onClose={() => setHistoryDrawer('')} />
    </div>
  );
};
