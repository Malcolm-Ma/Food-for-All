import {Col, Form, Input, Row, Select, Space, DatePicker, Progress} from "antd"
import React from "react";
import Text from "antd/es/typography/Text";
import {Option} from "antd/es/mentions";
import _ from "lodash";
export default (props) => {
  const { detailInfo } = props;
  const percent = 15;
  const title = detailInfo
  return (
    <div>
      <Form layout="vertical" hideRequiredMark>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="title"
              label="Name"
            >
              <Text>
                Title
              </Text>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="introduction"
              label="Introduction"
            >
              <Input.TextArea rows={4} placeholder="Introduction"/>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              name="picture"
              label="Picture"
            >
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="price"
              label="Price"
            >
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="donationNum"
              label="Donation Num"
              rules={[{required: true, message: 'Please choose the type'}]}
            >
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="totalNum"
              label="Total Num"
            >
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="startTime"
              label="Start Time"
            >
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="endTime"
              label="End Time"
            >
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="region"
              label="Region"
            >
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="progress"
              label="Progress"
            >
              <Progress percent={percent} width={60}/>
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </div>
  );
};