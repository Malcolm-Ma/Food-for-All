/**
 * @file Project list page
 * @author Mingze Ma
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from 'react-redux';
import React from 'react';
import moment from "moment";
import {
  Button,
  Progress,
  Modal,
  Table,
  Space,
  Drawer,
  Tag,
} from "antd";

import actions from "src/actions";
import _ from "lodash";
import { getProjectInfo } from "src/actions/projectActions";

import DrawerDetail from './ProjectDetail';
import {
  CheckCircleOutlined,
  ClockCircleOutlined,
  SyncOutlined
} from "@ant-design/icons";

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
  } = payloads;

  return [
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
    {
      title: 'Start Time',
      key: 'start_time',
      width: 130,
      render: (text, record) => {
        const { start_time: startTime } = record;
        const timeOfStart = moment(startTime * 1000).format("MMM DD, YYYY");
        return timeOfStart;
      }
    },
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
      width: 160,
      fixed: 'right',
      render: (text, record) => (
        <Space size="middle">
          <Button type="primary" onClick={() => showDrawer(record.pid)}>
            Detail
          </Button>
          <Button type="primary" onClick={() => showModal(record.pid)}>
            Stop
          </Button>
        </Space>
      ),
    },
  ];
}

export default () => {

  const dispatch = useDispatch();

  const { regionMap } = useSelector(state => state.global);

  const tableWrapperRef = useRef(null);

  const [projectInfo, setProjectInfo] = useState({});

  const getProjectList = useCallback(async () => {
    try {
      const res = await actions.getProjectList({
        currency_type: "GBP",
        page_info: {
          page_size: 10000,
          page: 1
        },
        search: '',
        order: '',
        uid: '',
        valid_only: '',
      });
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
  }, []);

  useEffect(() => {
    getProjectList().catch(err => console.error(err));
    dispatch(actions.getRegionList());
  }, [dispatch, getProjectList]);

  // projectDetailInfo state
  const [projectDetailInfo, setProjectDetailInfo] = React.useState({});

  const [deleteProjectInfo, setDeleteProjectInfo] = React.useState(0);
  //project progress state
  const [progressStatus, setProgressStatus] = React.useState("exception");

  const [drawVisible, drawSetVisible] = React.useState(false);
  //Edit button
  const [modalVisible, modalSetVisible] = React.useState(false);
  const [confirmLoading, setConfirmLoading] = React.useState(false);
  const [modalText, setModalText] = React.useState('Are you sure you want to terminate the project. Terminated projects cannot be continued.');
  //Edit popup window
  const showDrawer = async (projectId) => {
    try {
      const res = await getProjectInfo({
        "pid": projectId,
        "currency_type": _.get(projectInfo, 'currencyType'),
      });
      setProjectDetailInfo(_.get(res, 'project_info'));
    } catch (error) {
      console.log(error);
    }
    drawSetVisible(true);
  };

  const onClose = () => {
    drawSetVisible(false);
  };
  //Below is the delete button pop-up warning box
  const showModal = async (projectId) => {
    try {
      const res = await getProjectInfo({
        "pid": projectId,
        "currency_type": _.get(projectInfo, 'currencyType'),
      });
      setDeleteProjectInfo(projectId);
    } catch (error) {
      console.log(error);
    }
    modalSetVisible(true);
  };

  const handleOk = () => {
    setModalText('Terminating project.');
    setConfirmLoading(true);
    actions.stopProject({
      "pid": deleteProjectInfo,
    });
    setTimeout(() => {
      modalSetVisible(false);
      setConfirmLoading(false);
    }, 2000);
  };

  const handleCancel = () => {
    console.log('Clicked cancel button');
    modalSetVisible(false);
  };
  const payloads = {
    projectInfo,
    drawVisible,
    modalVisible,
    confirmLoading,
    modalText,
    regionMap,
    showDrawer,
    onClose,
    showModal,
    handleOk,
    handleCancel,
  };

  return (
    <div>
      <Table
        ref={tableWrapperRef}
        columns={columnsConfig(payloads)}
        rowKey={record => record.pid}
        dataSource={_.get(projectInfo, 'projectInfo', [])}
        scroll={{ x: 1500 }}
      />
      <Drawer
        className='ffa-home'
        title="Project Detail Info"
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
        <DrawerDetail detailInfo={projectDetailInfo} />
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
