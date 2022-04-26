// @Todo currency full name following the code in()
// @Todo turn to page after create, change title
// @Todo transform error info
import React, {useCallback, useEffect, useState} from "react";
import {Avatar, Badge, Divider, Grid, styled, TextField} from '@mui/material';
import {useDispatch, useSelector} from "react-redux";
import Typography from "@mui/material/Typography";
import actions from "src/actions";
import {Tag} from 'antd';
import _ from 'lodash';
import {SERVICE_BASE_URL} from "src/constants/constants";
import Box from "@mui/material/Box";
import {ProjectList} from "src/components/ProjectCardList";
import Container from "@mui/material/Container";
import {useParams} from "react-router-dom";

export default (props) => {

  const { uid } = useParams();

  const [userInfo, setUserInfo] = useState({});
  const [projectInfo, setProjectInfo] = useState({});

  useEffect(async () => {
    let userRes = await actions.getUserInfoById({
      'uid': uid
    });
    setUserInfo(userRes['user_info']);
    userRes = userRes['user_info'];
    console.log(userRes);
    let res = {};
    res = await actions.getProjectList({
      currency_type: 'GBP',
      page_info: {
        page_size: 10000,
        page: 1
      },
      search: '',
      order: '',
      uid: userRes.uid,
      valid_only: 0
    });
    console.log(res);
    const {
      project_info: rawProjectInfo,
      page_info: pageInfo,
      currency_type: currencyType,
      ...otherProps
    } = res;
    const projectInfo = _.values(rawProjectInfo);
    const result = {
      ...otherProps,
      projectInfo,
      pageInfo,
      currencyType,
    };
    setProjectInfo(result);
  }, [uid]);

  const userTypeTags = () => {
    const userType = _.get(userInfo, 'type');

    if (userType === 1) {
      return (
        <Tag color="success">
          Charity
        </Tag>
      );
    }
    if (userType === 0) {
      return (
        <Tag color="warning">
          Donor
        </Tag>
      );
    }
  }

  return (
    <Grid container rowSpacing={2}>
      <Grid item xs={3}>
        <Grid container rowSpacing={2}>
          <Grid item xs={3}>
            <Avatar sx={{ width: 200, height: 200 }} alt="Remy Sharp" src={SERVICE_BASE_URL + _.get(userInfo, 'avatar')}/>
          </Grid>
          <Grid item xs={9}>
            {_.get(userInfo, 'type') === 2 && <Grid item xs={12}>
              user
            </Grid>}
          </Grid>
          <Grid item xs={12}>
            <Typography textAlign="left" >{userInfo.name}</Typography>
            {userTypeTags()}
          </Grid>
        </Grid>
      </Grid>

      <Divider orientation="vertical" flexItem/>

      <Grid item xs={8} rowSpacing={2}>
        <Box>
          <h1>Project</h1>
          <Box>
            <Container>
              <ProjectList projects={_.get(projectInfo, 'projectInfo', [])}/>
            </Container>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};
