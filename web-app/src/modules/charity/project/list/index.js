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
  Select, InputNumber, Upload, message,
} from "antd";

import actions from "src/actions";
import _ from "lodash";
import {InboxOutlined} from "@ant-design/icons";
import {useDispatch, useSelector} from "react-redux";
import {useNavigate} from "react-router-dom";

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
    // @Todo prepared project don't have start time
    // {
    //   title: 'Start Time',
    //   key: 'start_time',
    //   render: (text, record) => {
    //     const {start_time: startTime} = record;
    //     const timeOfStart = moment(startTime).format("YYYY-MM-DD");
    //     return timeOfStart;
    //   }
    // },
    {
      title: 'End Time',
      key: 'end_time',
      render: (text, record) => {
        const {end_time: endTime} = record;
        const timeOfEnd = moment(endTime * 1000).format("YYYY-MM-DD");
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
      render: (text, record) => {
        const {status} = record.status;
        return (
          <Space size="middle">
            <Button type="primary" onClick={() => showDrawer(record)} disabled={status==="0"}>
              Edit
            </Button>
            <Button type="primary" onClick={showModal} disabled={status!=="0"}>
              Stop
            </Button>
          </Space>
        );
      }
    },
  ];
}

export default () => {

  const key = 'MessageKey';

  const navigate = useNavigate();

  const [projectInfo, setProjectInfo] = useState({});
  const dispatch = useDispatch();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [price, setPrice] = useState(100);
  const [donation, setDonation] = useState(10);
  const [targetProject, setTargetProject] = useState({});

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
    dispatch(actions.getUserInfo());
    dispatch(actions.getCurrencyList());
  }, [dispatch]);

  const {userInfo} = useSelector(state => state.user);
  const {currencyList} = useSelector(state => state.global);

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

  const showDrawer = (record) => {
    console.log('record',record);
    setTargetProject(record);
    setPrice(record.price);
    setDonation(record.total_num);
    drawSetVisible(true);
  };

  const onClose = () => {
    drawSetVisible(false);
  };
  //Below is the delete button pop-up warning box
  const showModal = () => {
    modalSetVisible(true);
  };

  const handleUpload = async (file) => {
    console.log('--file--\n', file);
  };

  const normFile = (e) => {
    console.log('Upload event:', e);
    if (Array.isArray(e)) {
      return e;
    }
    return e && e.fileList;
  };

  const handleOk = () => {
    setModalText('Terminating project.');
    setConfirmLoading(true);
    setTimeout(() => {
      modalSetVisible(false);
      setConfirmLoading(false);
    }, 3000);
    setIsModalVisible(false);
  };

  function disabledDate(current) {
    // Can not select days before today and today
    return current && current < moment().endOf('day');
  }

  const handleCancel = () => {
    console.log('Clicked cancel button');
    modalSetVisible(false);
    setIsModalVisible(false);
  };

  const suffixSelector = (
    <Form.Item name="currency" noStyle>
      <Select
        showSearch
        style={{ width: 100 }}
        placeholder="Search to Select"
        optionFilterProp="children"
        filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        }
        filterSort={(optionA, optionB) =>
          optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())
        }
      >
        {currencyList.map(item => (
          <Option value={item.value} key={item.value}>{item.value}</Option>
        ))}
      </Select>
    </Form.Item>
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

  const onFinish = async (values) => {
    message.loading({content: 'Loading'}, key);
    try {
      const editProjectRes = await actions.editProject({
        pid: targetProject.pid,
        currency_type: values.currency,
        edit: {
          title: values.title,
          intro: values.introduction,
          background_image: "",
          total_num: values.donation,
          end_time: moment(values.projectTime).unix(),
          details: values.details,
          price: values.price,
        }
      });
      if (editProjectRes !== null) {
        await message.success({content: 'Success! Waiting for refreshing...', duration: 1, key});
        location.reload();
      }
    } catch (e) {
      console.error(e);
      await message.error({content: 'Edit Error! ERROR INFO: '+e.name, key});
    }
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
        // zIndex={10000}
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
        <Form labelCol={{ span: 6 }}
              wrapperCol={{ span: 12}}
              name="nest-messages"
              onFinish={onFinish}
              initialValues={{
                currency: userInfo.currency_type,
                price: targetProject.price,
                donation: targetProject.total_num,
                title: targetProject.title,
                projectTime: moment(targetProject.end_time * 1000),
                introduction: targetProject.intro,
              }}
        >
          <Form.Item name="title" label="Title" rules={[{required: true, message: 'Please input the title'}]}>
            <Input/>
          </Form.Item>

          <Form.Item
            name="price"
            label="Price"
            rules={[{required: true, message: 'Please input the price'}]}
          >
            <InputNumber name="price" min={1} addonAfter={suffixSelector} style={{width: '100%'}} onChange={(value)=>{setPrice(value)}}/>
          </Form.Item>

          <Form.Item
            name="donation"
            label="Donation Amount"
            rules={[{required: true, message: 'Please input donation amount!'}]}
          >
            <InputNumber name="donation" min={1} style={{width: '100%'}} onChange={(value)=>{setDonation(value)}}/>
          </Form.Item>

          <Form.Item name="sum" label="Total money">
            <span>{price * donation}</span>
          </Form.Item>

          <Form.Item name="projectTime" label="Deadline" rules={[{required: true, message: 'Please select deadline!'}]}>
            <DatePicker disabledDate={disabledDate}/>
          </Form.Item>

          <Form.Item name="introduction" label="Introduction" rules={[{required: true, message: 'Please write the introduction!'}]}>
            <Input.TextArea/>
          </Form.Item>

          <Form.Item name="details" label="Details">
            <Input.TextArea/>
          </Form.Item>

          <Form.Item label="Background Image">
            <Form.Item name="background_image" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
              <Upload.Dragger name="files" action={handleUpload}>
                <p className="ant-upload-drag-icon">
                  <InboxOutlined/>
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload</p>
                <p className="ant-upload-hint">Support for a single or bulk upload.</p>
              </Upload.Dragger>
            </Form.Item>
          </Form.Item>

          {/* @Todo add submit Success page*/}
          <Form.Item wrapperCol={{offset: 6}}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>

          <Modal title="Error!" visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
            <p>You have not logged in! Please login first!</p>
          </Modal>
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
