/**
 * @file Project creating page
 * @author Mingze Ma
 */

import {useDispatch, useSelector} from 'react-redux';
import React, {useEffect, useState} from 'react';
import {
  Form,
  Input,
  InputNumber,
  Select,
  Button,
  DatePicker,
  Upload,
  message,
  Modal, Result,
} from 'antd';
import actions from 'src/actions';
import {InboxOutlined} from "@ant-design/icons";
import moment from "moment";
import {useNavigate} from "react-router-dom";

export default () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const key = 'MessageKey';
  const [isModalVisible, setIsModalVisible] = useState(false);
  const {Option} = Select;
  const [price, setPrice] = useState(100);
  const [donation, setDonation] = useState(10);

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
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  useEffect(() => {
    dispatch(actions.getUserInfo());
    dispatch(actions.getCurrencyList());
  }, [dispatch]);

  const {userInfo} = useSelector(state => state.user);
  const {currencyList} = useSelector(state => state.global);

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

  const onFinish = async (values) => {
    try {
      message.loading({content:'Loading'}, key);
      const createProjectRes = await actions.createProject();
      console.log('createProjectRes.status\n', createProjectRes);
      switch (createProjectRes.status) {
        case 0:
          const editProjectRes = await actions.editProject({
            pid: createProjectRes.pid,
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
          switch (editProjectRes.status) {
            case 0:
              navigate('/project/create/result');
              await message.success({content: 'Successs!', key});
              break;
            case 1:
              await message.error({content: "Please login first!", key});
              break;
            case 2:
              await message.error({content: "Wrong currency type!", key});
              break;
            case 3:
              await message.error({content: "Create project failed!", key});
              break;
            case 4:
              await message.error({content: "You are not the project owner!", key});
              break;
            case 5:
              await message.error({content: "Project edit failed!", key});
              break;
          }
          break;
        case 1:
          setIsModalVisible(true);
          await message.error({content: "Please login first!", key});
          break;
        case 2:
          await message.error({content: "You are not the charity", key});
          break;
      }
    } catch (e) {

    }
  };

  function disabledDate(current) {
    // Can not select days before today and today
    return current && current < moment().endOf('day');
  }

  return (
    <Form labelCol={{ span: 6 }}
          wrapperCol={{ span: 12}}
          name="nest-messages"
          onFinish={onFinish}
          initialValues={{
            currency: userInfo.user_info.currency_type,
            price: 100,
            donation: 10,
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
        <InputNumber name="price" min={1} addonAfter={suffixSelector} style={{width: '30%'}} onChange={(value)=>{setPrice(value)}}/>
      </Form.Item>

      <Form.Item
        name="donation"
        label="Donation Amount"
        rules={[{required: true, message: 'Please input donation amount!'}]}
      >
        <InputNumber name="donation" min={1} style={{width: '75%'}} onChange={(value)=>{setDonation(value)}}/>
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
  );
};
