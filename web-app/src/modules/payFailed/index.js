import React from 'react';
import { Result, Button, Typography } from 'antd';
import { CloseCircleOutlined } from '@ant-design/icons';

const { Paragraph, Text } = Typography;

export default () => (
    <Result
        status="error"
        title="Payment Failed"
        subTitle="Please check and correct your information before re-donating."
        extra={[
            <Button type="primary" key="console" href='project'>
                Confirm
            </Button>
        ]}
    >
        <div className="desc">
            <Paragraph>
                <Text
                    strong
                    style={{
                        fontSize: 16,
                    }}
                >
                    Your payment may contain the following errors:
                </Text>
            </Paragraph>
            <Paragraph>
                <CloseCircleOutlined className="site-result-demo-error-icon" /> You choose to cancel
                your donation
            </Paragraph>
            <Paragraph>
                <CloseCircleOutlined className="site-result-demo-error-icon" /> Your account has been
                frozen.
            </Paragraph>
            <Paragraph>
                <CloseCircleOutlined className="site-result-demo-error-icon" /> You do not have sufficient
                funds in your account.
            </Paragraph>
        </div>
    </Result>
);
