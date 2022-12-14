/**
 * @file Drawer content of editing
 * @author Tianhao Shi
 * @modified Mingze Ma
 */

import moment from "moment";
import {Button, DatePicker, Form, Image, Input, InputNumber, message, Modal, Select, Upload} from "antd";
import { InboxOutlined } from "@ant-design/icons";
import React, { useEffect, useState } from "react";
import actions from "src/actions";
import { useDispatch, useSelector } from "react-redux";
import {SERVICE_BASE_URL} from "src/constants/constants";
import _ from "lodash";

const { Option } = Select;

export default (props) => {
  const {
    targetProject,
  } = props;

  const dispatch = useDispatch();

  const { userInfo } = useSelector(state => state.user);
  const { currencyList } = useSelector(state => state.global);

  const [price, setPrice] = useState(100);
  const [donation, setDonation] = useState(10);
  const [img, setImg] = useState(_.get(targetProject, 'background_image'));

  useEffect(() => {
    dispatch(actions.getCurrencyList());
  }, [dispatch]);

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
    console.log('values, ', values);
    const key = 'MessageKey';
    try {
      const editProjectRes = await actions.editProject({
        pid: targetProject.pid,
        currency_type: values.currency,
        edit: {
          title: values.title,
          intro: values.introduction,
          background_image: img,
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

  const imgView = (values) => {
    if (values.file.status === "done") {
      setImg(values.file.response.url);
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
      <Form
        className="project-detail-edit"
        labelCol={{ span: 6 }}
        wrapperCol={{ span: 12 }}
        name="nest-messages"
        onFinish={onFinish}
        initialValues={{
          currency: userInfo.currency_type,
          price: targetProject.price,
          donation: targetProject.total_num,
          title: targetProject.title,
          projectTime: moment(targetProject.end_time * 1000),
          introduction: targetProject.intro,
          details: targetProject.details,
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
          <Input.TextArea rows={5}/>
        </Form.Item>

        <Form.Item name="details" label="Details" rules={[{required: true, message: 'Please write the details'}]}>
          <Input.TextArea rows={5}/>
        </Form.Item>

        <Form.Item label="Background Image">
          <Form.Item name="background_image" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
            <Upload.Dragger
              maxCount={1}
              name="files"
              action={SERVICE_BASE_URL + 'upload_img/'}
              onChange={imgView}
            >
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to this area to change the image</p>
              <Image
                preview={false}
                src={SERVICE_BASE_URL + img}
              />
            </Upload.Dragger>
          </Form.Item>
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 6 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </>
  );
};
