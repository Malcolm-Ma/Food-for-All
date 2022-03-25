/**
 * @file Project list page
 * @author Mingze Ma
 */
import {useCallback, useEffect, useState} from "react";
import React from 'react';
import 'antd/dist/antd.css';
import moment from "moment";
import {
  DatePicker,
  Button,
  Form,
  Input,
  Progress,
  Modal,
  Table,
  Space,
  Drawer,
  Row,
  Col,
  Select, InputNumber,
} from "antd";

import actions from "src/actions";
import _ from "lodash";

const { Option } = Select;

// Column config of a table
// Using either dataIndex or key to point out unique props
const columnsConfig = (payloads) => {

  const {
    drawVisible,
    modalVisible,
    confirmLoading,
    modalText,
    showDrawer,
    onClose,
    showModal,
    handleOk,
    handleCancel,
  } = payloads;

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
      onCell: () => {
        return {
          style: {
            cursor: 'pointer'
          }
        }
      },
    },
    {
      title: 'Price',
      key: 'price',
      render: (text, record) => {
        const {price: price, region: region} = record;
        const realPrice = String(_.floor(price, 2));
        const shortRegion = region.slice(0, 3);
        return (realPrice + shortRegion);
      }
    },
    {
      title: 'Donation Num',
      dataIndex: 'current_num',
    },
    {
      title: 'Total Num',
      dataIndex: 'total_num',
    },
    {
      title: 'Start Time',
      key: 'start_time',
      render: (text, record) => {
        const {start_time: startTime} = record;
        const timeOfStart = moment(startTime).format("YYYY-MM-DD");
        return timeOfStart;
      }
    },
    {
      title: 'End Time',
      key: 'end_time',
      render: (text, record) => {
        const {end_time: endTime} = record;
        const timeOfEnd = moment(endTime).format("YYYY-MM-DD");
        return timeOfEnd;
      }
    },
    {
      title: 'Region',
      dataIndex: 'region',
    },
    {
      title: 'Progress',
      key: 'Progress',
      width: 160,
      render: (text, record) => {
        const {current_num: currentNum, total_num: totalNum} = record;
        const percent = _.floor((currentNum / totalNum) * 100, 0);
        return (
          <Progress percent={percent}/>
        );
      }
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button type="primary" onClick={showDrawer}>
            Edit
          </Button>
          <Button type="primary" onClick={showModal}>
            Stop
          </Button>
        </Space>
      ),
    },
  ];
}

export default () => {

  const [projectInfo, setProjectInfo] = useState({});

  const getProjectList = useCallback(async () => {
    try {
      const res = await actions.prepareProject();
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

  //
  const [drawVisible, drawSetVisible] = React.useState(false);
  //Edit button
  const [modalVisible, modalSetVisible] = React.useState(false);
  const [confirmLoading, setConfirmLoading] = React.useState(false);
  const [modalText, setModalText] = React.useState('Are you sure you want to terminate the project. Terminated projects cannot be continued.');
  //Edit popup window
  const showDrawer = () => {
    drawSetVisible(true);
  };

  const onClose = () => {
    drawSetVisible(false);
  };
  //Below is the delete button pop-up warning box
  const showModal = () => {
    modalSetVisible(true);
  };

  const handleOk = () => {
    setModalText('Terminating project.');
    setConfirmLoading(true);
    setTimeout(() => {
      modalSetVisible(false);
      setConfirmLoading(false);
    }, 3000);
  };

  const handleCancel = () => {
    console.log('Clicked cancel button');
    modalSetVisible(false);
  };
  const selectAfter = (
    <Select defaultValue="GBP" style={{ width: 60 }}>
      <Option value="USD">$</Option>
      <Option value="EUR">€</Option>
      <Option value="GBP">£</Option>
      <Option value="CNY">¥</Option>
    </Select>
  );
  const payloads = {
    drawVisible,
    modalVisible,
    confirmLoading,
    modalText,
    showDrawer,
    onClose,
    showModal,
    handleOk,
    handleCancel,
  };
  return (
    <div>
      <Table
        columns={columnsConfig(payloads)}
        rowKey={record => record.pid}
        dataSource={_.get(projectInfo, 'projectInfo', [])}
      />
      <Drawer
        className='ffa-home'
        title="Edit Drawer"
        placement="right"
        onClose={onClose}
        zIndex={10000}
        visible={drawVisible}
        bodyStyle={{paddingBottom: 80}}
        width={600}
        extra={
          <Space>
            <Button onClick={onClose}>Cancel</Button>
            <Button onClick={onClose} type="primary">
              Submit
            </Button>
          </Space>
        }>
        <Form layout="vertical" hideRequiredMark>
          <Row gutter={16}>
            <Col span={24}>
              <Form.Item
                name="Title"
                label="Name"
                rules={[{required: true, message: 'Please enter new title'}]}
              >
                <Input placeholder="Please enter title"/>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={24}>
              <Form.Item
                name="introduction"
                label="Introduction"
                rules={[
                  {
                    required: true,
                    message: 'please enter new introduction',
                  },
                ]}
              >
                <Input.TextArea rows={4} placeholder="please enter introduction"/>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="num"
                label="Num"
                rules={[{required: true, message: 'Please enter new num'}]}
              >
                <InputNumber min={1} max={10000000} style={{ width: '100%' }}/>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="price"
                label="Price"
                rules={[{required: true, message: 'Please enter new price'}]}
              >
                <InputNumber addonAfter={selectAfter} min={1} max={30} style={{ width: '100%' }}/>
              </Form.Item>
            </Col>

          </Row>
          <Row gutter={16}>
            <Col span={24}>
              <Form.Item
                name="dateTime"
                label="DateTime"
                rules={[{required: true, message: 'Please choose the dateTime'}]}
              >
                <DatePicker.RangePicker
                  style={{ width: '100%' }}
                  getPopupContainer={trigger => trigger.parentElement}
                />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Drawer>
      <Modal
        title= "Stop Project"
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
