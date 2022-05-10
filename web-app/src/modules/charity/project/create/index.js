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
  Modal, Result, Image,
} from 'antd';
import actions from 'src/actions';
import {InboxOutlined} from "@ant-design/icons";
import moment from "moment";
import {useNavigate} from "react-router-dom";
import {SERVICE_BASE_URL} from "src/constants/constants";
import _ from "lodash";

export default () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const key = 'MessageKey';
  const [isModalVisible, setIsModalVisible] = useState(false);
  const {Option} = Select;
  const [price, setPrice] = useState(100);
  const [donation, setDonation] = useState(10);
  const [img, setImg] = useState(null);

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

  const imgView = (values) => {
    console.log(values);
    if (values.file.status === "done") {
      setImg(SERVICE_BASE_URL + values.file.response.url);
    }
  };

  const onFinish = async (values) => {
    try {
      const createProjectRes = await actions.createProject();
      console.log('createProjectRes\n', createProjectRes);
      if (createProjectRes !== null) {
        let imgURL;
        try {
          imgURL = values.background_image[0].response.url;
        } catch (e) {
          imgURL = "";
        }
        try {
          const editProjectRes = await actions.editProject({
            pid: createProjectRes.pid,
            currency_type: values.currency,
            edit: {
              title: values.title,
              intro: values.introduction,
              background_image: imgURL,
              total_num: values.donation,
              end_time: moment(values.projectTime).unix(),
              details: values.details,
              price: values.price,
            }
          });
          if (editProjectRes !== null) {
            navigate('/charity/project/create/result');
            await message.success({content: 'Success!', key});
          }
        } catch (e) {
          console.error(e);
          await message.error({content: 'Edit Error! ERROR INFO: '+e.name, key});
        }
      }
    } catch (e) {
      console.error(e);
      await message.error({content: "Create failed! ERROR INFO: "+e.name, key});
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
            currency: userInfo.currency_type,
            price: 100,
            donation: 10,
          }}
    >
      <Form.Item name="title" label="Title" rules={[{required: true, message: 'Please input the title'}]}>
        <Input/>
      </Form.Item>

      <Form.Item
        name="price"
        label="Price per Meal"
        rules={[{required: true, message: 'Please input the price'}]}
      >
        <InputNumber name="price" min={1} addonAfter={suffixSelector} style={{width: '100%'}} onChange={(value)=>{setPrice(value)}}/>
      </Form.Item>

      <Form.Item
        name="donation"
        label="Total Meals Due for Donation"
        rules={[{required: true, message: 'Please input donation amount!'}]}
      >
        <InputNumber name="donation" min={1} style={{width: '30%'}} onChange={(value)=>{setDonation(value)}}/>
      </Form.Item>

      <Form.Item name="sum" label="Amount of Meals will be Donated">
        <span>{price * donation}</span>
      </Form.Item>

      <Form.Item name="projectTime" label="Donating End Time" rules={[{required: true, message: 'Please select deadline!'}]}>
        <DatePicker disabledDate={disabledDate}/>
      </Form.Item>

      <Form.Item name="introduction" label="Introduction" rules={[{required: true, message: 'Please write the introduction!'}]}>
        <Input.TextArea/>
      </Form.Item>

      <Form.Item name="details" label="Details" rules={[{required: true, message: 'Please write the details'}]}>
        <Input.TextArea/>
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
              src={img}
            />
          </Upload.Dragger>
        </Form.Item>
      </Form.Item>

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
