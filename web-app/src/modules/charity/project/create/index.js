/**
 * @file Project creating page
 * @author Mingze Ma
 */

import { useSelector } from 'react-redux';
import React from 'react';
import {
  Form,
  Input,
  InputNumber,
  Select,
  Button,
  DatePicker,
} from 'antd';

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

const rangeConfig = {
  rules: [{ type: 'array', required: true, message: 'Please select time!' }],
};


export default () => {
  const { createResult } = useSelector(state => state.project);

  // useEffect(() => {
  //   console.log('--userInfo--\n', userInfo);
  // }, [userInfo]);

  console.log(createResult);

  const onFinish = (values) => {
    console.log(values);
  };

  return (
    <Form {...layout} name="nest-messages" onFinish={onFinish} validateMessages={validateMessages}>

      <Form.Item
        name="donation"
        label="Donation"
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

      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
