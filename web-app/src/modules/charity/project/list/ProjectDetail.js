import {Col, Form, Input, Row, Select, Space, DatePicker, Progress, Descriptions, Image} from "antd"
import React from "react";
import Text from "antd/es/typography/Text";
import {Option} from "antd/es/mentions";
import _ from "lodash";
import {Description} from "@mui/icons-material";
import {render} from "react-dom";
import moment from "moment";

export default (props) => {
  const {detailInfo} = props;
  const currentNum = _.get(detailInfo, 'current_num');
  const totalNum = _.get(detailInfo, 'total_num');
  const percent = _.floor((currentNum / totalNum) * 100, 0);
  return (
    <div>
      <Form layout="vertical" hideRequiredMark>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Name"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'title')}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Introduction"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'intro')}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Picture"
            >
              <Image
                src={_.get(detailInfo, 'background_image')}
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              label="Price"
            >
              <Descriptions>
                <Descriptions.Item>{String(_.floor(_.get(detailInfo, 'price'), 2))}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              label="Donation Num"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'current_num')}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              label="Total Num"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'total_num')}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Start Time"
            >
              <Descriptions>
                <Descriptions.Item>{moment(_.get(detailInfo, 'start_time') * 1000).format("YYYY-MM-DD")}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="End Time"
            >
              <Descriptions>
                <Descriptions.Item>{moment(_.get(detailInfo, 'end_time') * 1000).format("YYYY-MM-DD")}</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Region"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'region')}</Descriptions.Item>
              </Descriptions>
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