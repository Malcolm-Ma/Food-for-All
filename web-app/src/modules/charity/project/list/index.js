/**
 * @file Project list page
 * @author Mingze Ma
 */
import { useCallback, useEffect, useRef, useState } from "react";
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
} from "antd";

import actions from "src/actions";
import _ from "lodash";
import { getProjectInfo } from "src/actions/projectActions";
import { InboxOutlined } from "@ant-design/icons";

import {
  CheckCircleOutlined,
  ClockCircleOutlined,
  SyncOutlined
} from "@ant-design/icons";

import EditDetail from "./EditDetail";
import DrawerDetail from './ProjectDetail';

import './index.less';

// Column config of a table
// Using either dataIndex or key to point out unique props
const columnsConfig = (payloads) => {

  const {
    projectInfo,
    drawVisible,
    modalVisible,
    confirmLoading,
    modalText,
    showDrawer,
    onClose,
    showModal,
    handleOk,
    handleCancel,
    regionMap,
    prepareMode,
  } = payloads;

  return _.compact([
    {
      title: 'Title',
      dataIndex: 'title',
      width: 200,
      fixed: 'left',
      render: text => <a>{text}</a>,
    },
    {
      title: 'Introduction',
      dataIndex: 'intro',
      ellipsis: true,
      width: 160,
      render: value =>
        <Tooltip title={value}>
          <div style={{ float: 'left', maxWidth: '100%', cursor: 'pointer' }}>
            {value.substring(0,12)+'...'}
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
                  Outgoing
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
        }
      }
    },
    {
      title: 'Price',
      key: 'price',
      render: (text, record) => {
        const { price: price } = record;
        const realPrice = String(_.floor(price, 2));
        return (realPrice + ' ' + _.get(projectInfo, 'currencyType'));
      }
    },
    {
      title: 'Progress',
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
      title: 'Donation Num',
      dataIndex: 'current_num',
      render: (text, record) => {
        const { total_num: totalNum } = record;
        return `${text} / ${totalNum}`;
      }
    },
    {
      title: 'Region',
      dataIndex: 'region',
      render: (text, record) => {
        const fullRegionName = _.get(regionMap, text);
        if (fullRegionName) {
          return `${fullRegionName} (${text})`;
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
      title: 'Action',
      key: 'action',
      width: 200,
      align: 'right',
      fixed: 'right',
      render: (text, record) => (
        <Space size={0}>
          <Button type="link" onClick={() => showDrawer('detail', record.pid)}>
            Detail
          </Button>
          <Button type="link" onClick={() => showDrawer('edit', record.pid)} disabled={record.status !== 0}>
            Edit
          </Button>
          <Button type="link" onClick={() => showModal(record.pid, record.status)}>
            {record.status === 0 ? 'Start' : 'Stop'}
          </Button>
        </Space>
      ),
    },
  ]);
}

export default () => {

  const dispatch = useDispatch();

  const { regionMap } = useSelector(state => state.global);
  const { currencyList } = useSelector(state => state.global);
  const { userInfo } = useSelector(state => state.user);

  const [projectInfo, setProjectInfo] = useState({});
  const [isModalVisible, setIsModalVisible] = useState(false);

  const [prepareMode, setPrepareMode] = useState(false);
  const [drawerType, setDrawerType] = useState('');

  // projectDetailInfo state
  const [projectDetailInfo, setProjectDetailInfo] = useState({});

  const [operatingProject, setOperatingProject] = useState([]);
  //project progress state
  const [progressStatus, setProgressStatus] = useState("exception");

  const [drawVisible, drawSetVisible] = useState(false);
  //Edit button
  const [modalVisible, modalSetVisible] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [modalText, setModalText] = useState('Are you sure you want to terminate the project. '
    + 'Terminated projects cannot be continued.');

  const getProjectList = useCallback(async () => {
    try {
      let res = {};
      if (prepareMode) {
        res = await actions.getPrepareProject();
      } else {
        res = await actions.getProjectList({
          currency_type: userInfo.currency_type || 'GBP',
          page_info: {
            page_size: 10000,
            page: 1
          },
          search: '',
          order: '',
          uid: '',
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
      setProjectInfo(result);
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
  const showModal = (projectId, status) => {
    setOperatingProject([projectId, status]);
    modalSetVisible(true);
  };

  const handleOk = async () => {
    const [projectId, status] = operatingProject;
    if (status === 0) {
      // prepare mode
      setModalText('Start project.');
      setConfirmLoading(true);
      // TODO change to start project
      await actions.stopProject({
        "pid": projectId,
      });
    }
    if (status === 1) {
      // ongoing mode
      setModalText('Terminating project.');
      setConfirmLoading(true);
      // TODO change to start project
      await actions.stopProject({
        "pid": projectId,
      });
    }
    setTimeout(() => {
      modalSetVisible(false);
      setConfirmLoading(false);
    }, 500);
    setIsModalVisible(false);
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
        // title="Edit Project"
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
        {drawerType === 'edit' && <EditDetail targetProject={projectDetailInfo}/>}
      </Drawer>
      <Modal
        title="Stop Project"
        visible={modalVisible}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
      >
        <p>{modalText}</p>
      </Modal>
    </div>
  );

};
