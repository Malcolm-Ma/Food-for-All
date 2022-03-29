import { Col, Form, Row, Progress, Descriptions, Image } from "antd"
import React from "react";
import _ from "lodash";
import moment from 'moment';
import { SERVICE_BASE_URL } from "src/constants/constants";
import { useSelector } from "react-redux";

export default (props) => {
  const { detailInfo } = props;

  const { regionMap } = useSelector(state => state.global);

  const currentNum = _.get(detailInfo, 'current_num');
  const totalNum = _.get(detailInfo, 'total_num');
  const percent = _.floor((currentNum / totalNum) * 100, 0);

  return (
    <div className="project-detail">
      <Form layout="vertical" hideRequiredMark>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Title"
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
              label="Details"
            >
              <Descriptions>
                <Descriptions.Item>{_.get(detailInfo, 'details')}</Descriptions.Item>
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
                src={SERVICE_BASE_URL + _.get(detailInfo, 'background_image')}
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
                <Descriptions.Item>
                  {_.floor(_.get(detailInfo, 'price'), 2) + ' ' + detailInfo.currencyType}
                </Descriptions.Item>
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
                <Descriptions.Item>
                  {moment(_.get(detailInfo, 'start_time') * 1000).format("MMM DD, YYYY")}
                </Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="End Time"
            >
              <Descriptions>
                <Descriptions.Item>
                  {moment(_.get(detailInfo, 'end_time') * 1000).format("MMM DD, YYYY")}
                </Descriptions.Item>
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
                <Descriptions.Item>{
                  (() => {
                    const region = _.get(detailInfo, 'region');
                    const fullRegion = _.get(regionMap, region);
                    if (fullRegion) {
                      return `${fullRegion} (${region})`;
                    }
                    return region;
                  })()
                }</Descriptions.Item>
              </Descriptions>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="progress"
              label="Progress"
            >
              <Progress percent={percent} width={60} />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </div>
  );
};
