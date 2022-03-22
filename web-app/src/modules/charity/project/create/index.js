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
  Modal,
} from 'antd';
import actions from 'src/actions';
import {InboxOutlined} from "@ant-design/icons";
import moment from "moment";

const {Option} = Select;

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

const validateMessages = {
  required: '${label} is required!',
  types: {
    email: '${label} is not a valid email!',
    number: '${label} is not a valid number!',
  },
  number: {
    range: '${label} must be between ${min} and ${max}',
  },
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

export default () => {
  const dispatch = useDispatch();

  const key = 'MessageKey';

  const [isModalVisible, setIsModalVisible] = useState(false);
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
        style={{ width: 200 }}
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

  const logout = () => {
    actions.logout();
    console.log('logout');
  }

  const onFinish = async (values) => {
    try {
      message.loading({content: 'Loading...', key});
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
    <Form {...layout}
          name="nest-messages"
          onFinish={onFinish}
          validateMessages={validateMessages}
          initialValues={{
            currency: userInfo.currency_type,
            price: 100,
          }}
    >

      <Form.Item name="title" label="Title" rules={[{required: true, message: 'Please input the title'}]}>
        <Input/>
      </Form.Item>

      <Form.Item name="price" label="Price" rules={[{required: true, message: 'Please input the price'}]}>
        <InputNumber min={1} />
      </Form.Item>

      <Form.Item
        name="donation"
        label="Donation Amount"
        rules={[{required: true, message: 'Please input donation amount!'}]}
      >
        <InputNumber addonAfter={suffixSelector} style={{width: '100%'}}/>
      </Form.Item>

      <Form.Item name="projectTime" label="Deadline" rules={[{required: true, message: 'Please select deadline!'}]}>
        <DatePicker disabledDate={disabledDate} />
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

      <Form.Item wrapperCol={{...layout.wrapperCol, offset: 8}}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>

      <Form.Item wrapperCol={{...layout.wrapperCol, offset: 8}}>
        <Button type="primary" onClick={logout}>
          Logout
        </Button>
      </Form.Item>

      <Modal title="Error!" visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
        <p>You have not logged in! Please login first!</p>
      </Modal>
    </Form>
  );
};
