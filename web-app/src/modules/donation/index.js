/**
 * @file entrance of payment&detail page
 * @author Mingze Ma
 */

// module import
import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import _ from 'lodash';

// style import
import './index.less';
import actions from "src/actions";
import { useSelector } from "react-redux";
import Box from "@mui/material/Box";

import { SERVICE_BASE_URL } from "src/constants/constants";
import Grid from "@mui/material/Grid";
import { Container, CssBaseline, Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import PaymentForm from "src/modules/donation/PaymentForm";
import { Statistic, Row, Col, Progress, Form } from 'antd';
import moment from "moment";

export default (props) => {
  const {} = props;
  const { pid, currency } = useParams();

  const { userinfo } = useSelector(state => state.user);
  const { regionInfo } = useSelector(state => state.global);

  const [projectDetail, setProjectDetail] = useState();

  const currentNum = _.get(projectDetail, 'current_num');
  const totalNum = _.get(projectDetail, 'total_num');
  const percent = _.floor((currentNum / totalNum) * 100, 0);

  useEffect(() => {
    if (!_.isEmpty(regionInfo)) {
      (async () => {
        try {
          const res = await actions.getProjectInfo({
            pid,
            currency_type: currency || regionInfo.currencyType,
          });
          setProjectDetail(res.project_info);
          console.log(projectDetail);
        } catch (e) {
          console.error(e);
        }
      })();
    }
  }, [pid, regionInfo, userinfo]);

  const theme = createTheme();
  const bgImageUrl = useMemo(() => {
    const srcImage = _.get(projectDetail, 'background_image');
    if (!_.isEmpty(srcImage)) {
      return `url(${SERVICE_BASE_URL}${_.get(projectDetail, 'background_image')})`;
    }
    return `url(${require('src/assets/broken-1.jpg')})`;
  }, [projectDetail]);
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {
        projectDetail ? <>
            <Box
              sx={{
                backgroundImage: bgImageUrl,
                position: 'absolute',
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                zIndex: -2,
              }}
            >
            </Box>
            <Box
              sx={{
                position: 'absolute',
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                backgroundColor: 'rgba(61, 92, 118, 0.7)',
                // opacity: 0.7,
                zIndex: -1,
              }}
            >
            </Box>
            <Grid
              className="donation"
              container={true}
              sx={{
                zIndex: 2,
                pt: 12,
              }}
            >
              <Grid item sm={6} sx={{ color: 'white' }}>
                <Container component="div" maxWidth="sm" sx={{ p: { xs: 0, sm: 2 } }}>
                  <Typography variant="h4" sx={{ color: 'white' }}>
                    {_.get(projectDetail, 'title', '')}
                  </Typography>
                  <Box sx={{ pt: 6 }}>
                    <Row gutter={16}>
                      <Col span={12}>
                        <Statistic className="project-statistic" valueStyle={{ color: 'white' }}
                                   title="Number of Meals Donated"
                                   value={_.get(projectDetail, "current_num")} />
                      </Col>
                      <Col span={12}>
                        <Statistic className="project-statistic" valueStyle={{ color: 'white' }}
                                   title="Total Meals Due for Donation"
                                   value={_.get(projectDetail, "total_num")} />
                      </Col>
                    </Row>
                    <Row gutter={16}>
                      <Col span={12}>
                        <Statistic className="project-statistic" valueStyle={{ color: 'white' }} title="Start Time"
                                   value={moment(_.get(projectDetail, 'start_time') * 1000).format("MMM DD, YYYY")} />
                      </Col>
                      <Col span={12}>
                        <Statistic className="project-statistic" titleStyle={{ color: 'white' }}
                                   valueStyle={{ color: 'white' }} title="End Time"
                                   value={moment(_.get(projectDetail, 'end_time') * 1000).format("MMM DD, YYYY")} />
                      </Col>
                    </Row>
                    <Row gutter={16}>
                      <Col span={20}>
                        <Form.Item
                          className="project-progress"
                          label="Progress"
                          style={{ margin: 0 }}
                        >
                          <Progress percent={percent} width={150} />
                        </Form.Item>
                      </Col>
                    </Row>
                  </Box>
                  <Typography variant="body1" sx={{ pt: 6 }}>
                    {_.get(projectDetail, 'details', '')}
                  </Typography>
                  <Typography variant="h4" sx={{ pt: 8, color: 'white' }}>
                    Please donate now, it only takes a minute.
                  </Typography>
                </Container>
              </Grid>
              <Grid item sm={6}>
                <PaymentForm currency={currency} projectDetail={projectDetail} />
              </Grid>
            </Grid>
          </>
          : <>

          </>
      }
    </ThemeProvider>
  );
};
