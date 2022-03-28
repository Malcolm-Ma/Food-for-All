/**
 * @file Drawer content of editing
 * @author Tianhao Shi
 * @modified Mingze Ma
 */

import moment from "moment";
import { Button, DatePicker, Form, Input, InputNumber, message, Modal, Select, Upload } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import React, { useEffect, useState } from "react";
import actions from "src/actions";
import { useDispatch, useSelector } from "react-redux";

const { Option } = Select;

export default (props) => {
  const {
    targetProject,
  } = props;

  const dispatch = useDispatch();

  const { userInfo } = useSelector(state => state.user);
  const { currencyList } = useSelector(state => state.global);

  const [detailInfo, setDetailInfo] = useState({});

  const [price, setPrice] = useState(100);
  const [donation, setDonation] = useState(10);

  useEffect(() => {
    dispatch(actions.getCurrencyList());
  }, [dispatch]);

  useEffect(() => {
    (async () => {
      try {
        const { project_info: projectInfo } = actions.getProjectInfo({
          pid: targetProject.pid,
          currency_type: userInfo.currency_type,
        });
        setDetailInfo(projectInfo);
        setPrice(projectInfo.price);
        setDonation(projectInfo.donation);
      } catch (e) {
        console.error(e);
      }
    })();
  }, [targetProject.pid, userInfo.currency_type]);

  const disabledDate = (current) => {
    // Can not select days before today and today
    return current && current < moment().endOf('day');
  }

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

  const onFinish = async (values) => {
    const key = 'MessageKey';
    message.loading({ content: 'Loading' }, key);
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
        await message.success({ content: 'Success! Waiting for refreshing...', duration: 1, key });
        location.reload();
      }
    } catch (e) {
      console.error(e);
      await message.error({ content: 'Edit Error! ERROR INFO: ' + e.name, key });
    }
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

  return (
    <>
      <Form labelCol={{ span: 6 }}
            wrapperCol={{ span: 12 }}
            name="nest-messages"
            onFinish={onFinish}
            initialValues={{
              currency: userInfo.currency_type,
              price: detailInfo.price,
              donation: detailInfo.total_num,
              title: detailInfo.title,
              projectTime: moment(detailInfo.end_time * 1000),
              introduction: detailInfo.intro,
            }}
      >
        <Form.Item name="title" label="Title" rules={[{ required: true, message: 'Please input the title' }]}>
          <Input />
        </Form.Item>

        <Form.Item
          name="price"
          label="Price"
          rules={[{ required: true, message: 'Please input the price' }]}
        >
          <InputNumber name="price" min={1} addonAfter={suffixSelector} style={{ width: '100%' }} onChange={(value) => {
            setPrice(value)
          }} />
        </Form.Item>

        <Form.Item
          name="donation"
          label="Donation Amount"
          rules={[{ required: true, message: 'Please input donation amount!' }]}
        >
          <InputNumber name="donation" min={1} style={{ width: '100%' }} onChange={(value) => {
            setDonation(value)
          }} />
        </Form.Item>

        <Form.Item name="sum" label="Total money">
          <span>{price * donation}</span>
        </Form.Item>

        <Form.Item name="projectTime" label="Deadline" rules={[{ required: true, message: 'Please select deadline!' }]}>
          <DatePicker disabledDate={disabledDate} />
        </Form.Item>

        <Form.Item name="introduction" label="Introduction"
                   rules={[{ required: true, message: 'Please write the introduction!' }]}>
          <Input.TextArea />
        </Form.Item>

        <Form.Item name="details" label="Details">
          <Input.TextArea />
        </Form.Item>

        <Form.Item label="Background Image">
          <Form.Item name="background_image" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
            <Upload.Dragger name="files" action={handleUpload}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to this area to upload</p>
              <p className="ant-upload-hint">Support for a single or bulk upload.</p>
            </Upload.Dragger>
          </Form.Item>
        </Form.Item>

        {/* @Todo add submit Success page*/}
        <Form.Item wrapperCol={{ offset: 6 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </>
  );
};
