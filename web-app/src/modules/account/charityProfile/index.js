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
import { DEFAULT_CURRENCY, SERVICE_BASE_URL } from "src/constants/constants";
import Box from "@mui/material/Box";
import {ProjectList} from "src/components/ProjectCardList";
import Container from "@mui/material/Container";
import {useParams} from "react-router-dom";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import {ArrowBack} from "@mui/icons-material";

export default (props) => {

  const { uid } = useParams();

  const { regionInfo } = useSelector(state => state.global);
  const { userInfo: systemUserInfo } = useSelector(state => state.user);

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
      currency_type: _.get(userInfo, 'currency_type', null) || _.get(regionInfo, 'currencyType', DEFAULT_CURRENCY),
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
  }, [regionInfo, uid]);

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
      <Grid item xs={1.5}>
        <Grid container rowSpacing={2}>
          <Grid item xs={3}>
            <Avatar sx={{ width: 100, height: 100 }} alt="Remy Sharp" src={SERVICE_BASE_URL + _.get(userInfo, 'avatar')}/>
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
          <Grid item xs={12}>
            <Button variant="contained" startIcon={<ArrowBack />} href="/project">
              Return
            </Button>
          </Grid>
        </Grid>
      </Grid>


      <Divider orientation="vertical" flexItem/>

      <Grid item xs={10} rowSpacing={2}>
        <Box>
          <Box>
            <Container>
              <ProjectList
                currencyType={systemUserInfo.currency_type || regionInfo.currencyType}
                projects={_.get(projectInfo, 'projectInfo', [])}
              />
            </Container>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};
