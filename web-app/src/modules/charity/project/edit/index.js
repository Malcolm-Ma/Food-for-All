import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import actions from "src/actions";
import {Button, DatePicker, Form, Input, InputNumber, Modal, Select, Upload} from "antd";
import {InboxOutlined} from "@ant-design/icons";
import moment from "moment";

export default () => {
  const dispatch = useDispatch();
  const {userInfo} = useSelector(state => state.user);
  const user_info = userInfo.user_info;
  const { regionList, currencyList } = useSelector(state => state.global);
  const currencyCode = currencyList.map(item => item.value);
  useEffect(() => {
    dispatch(actions.getRegionList()).catch(err => console.error(err));
    dispatch(actions.getCurrencyList()).catch(err => console.error(err));
  }, [dispatch]);

  const {Option} = Select;

  function disabledDate(current) {
    // Can not select days before today and today
    return current && current < moment().endOf('day');
  }

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

  return (
    <Form>
      <Form.Item name="title" label="Title" rules={[{required: true, message: 'Please input the title'}]}>
        <Input/>
      </Form.Item>

      <Form.Item name="price" label="Price" rules={[{required: true, message: 'Please input the price'}]}>
        <InputNumber min={1} addonAfter={suffixSelector} style={{width: '30%'}}/>
      </Form.Item>

      <Form.Item name="donation" label="Donation Amount" rules={[{required: true, message: 'Please input donation amount!'}]}>
        <InputNumber min={1} style={{width: '30%'}}/>
      </Form.Item>

      {/* @Todo multiply price and amount of donation*/}
      <Form.Item name="sum" label="Total money">
        <span>{}</span>
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