/**
 * @file Project creating page
 * @author Mingze Ma
 */

import {useDispatch, useSelector} from 'react-redux';
import React from 'react';
import {
  Form,
  Input,
  InputNumber,
  Select,
  Button,
  DatePicker, Upload,
} from 'antd';
import actions from 'src/actions';
import {InboxOutlined} from "@ant-design/icons";

const { RangePicker } = DatePicker;
const { Option } = Select;

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

const suffixSelector = (
  <Form.Item name="suffix" noStyle>
    <Select style={{ width: 100 }}>
      <Option value="USD">$ USD</Option>
      <Option value="CNY">¥ CNY</Option>
    </Select>
  </Form.Item>
);

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

const rangeConfig = {
  rules: [{ type: 'array', required: true, message: 'Please select time!' }],
};

export default () => {
   const { userInfo } = useSelector(state => state.user);

  const dispatch = useDispatch();

  // useEffect(() => {
  //   console.log('--userInfo--\n', userInfo);
  // }, [userInfo]);

  const onFinish = async (values) => {

    try {
      console.log(values);
      // @Todo generate "pid"?
      const createProjectRes = await actions.createProject({ userInfo });
      // console.log('--createProjectRes--\n', createProjectRes);

      // @Todo reset status
      if (createProjectRes.status === 1) {
        const editProjectRes = await actions.editProject({
          ...values
        });
      }
    } catch (e) {

    }

  };

  return (
    <Form {...layout} name="nest-messages" onFinish={onFinish} validateMessages={validateMessages}>

      <Form.Item name="test" label="Title" rules={[{ required: true, message: 'Please input the title'}]}>
        <Input />
      </Form.Item>

      <Form.Item
        // name="donation"
        name={['user', 'donation']}
        label="Donation Amount"
        rules={[{ required: true, message: 'Please input donation amount!' }]}
      >
        <InputNumber addonAfter={suffixSelector} style={{ width: '100%' }} />
      </Form.Item>

      <Form.Item name="range-picker" label="RangePicker" {...rangeConfig}>
        <RangePicker />
      </Form.Item>

      <Form.Item name={['user', 'introduction']} label="Introduction">
        <Input.TextArea />
      </Form.Item>

      <Form.Item label="Backgrund Image">
        <Form.Item name="dragger" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
          <Upload.Dragger name="files" action={handleUpload}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">Click or drag file to this area to upload</p>
            <p className="ant-upload-hint">Support for a single or bulk upload.</p>
          </Upload.Dragger>
        </Form.Item>
      </Form.Item>

      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
