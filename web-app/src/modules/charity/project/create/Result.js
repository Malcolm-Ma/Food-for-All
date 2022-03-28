import {Button, Result} from "antd";
import React from "react";
import {useNavigate} from "react-router-dom";

export default () => {

  const navigate = useNavigate();

  const toProjectList = () => {
    navigate('/project/list');
  };

  const toMain = () => {
    navigate('/');
  };

  return (
    <Result
      status="success"
      title="Successfully Created Your Project!"
      subTitle="Tips:Project needs to be activated by yourself!"
      extra={[
        <Button type="primary" key="activate" onClick={toProjectList}>
          Activate Project
        </Button>,
        <Button key="back" onClick={toMain}>
          Back
        </Button>,
      ]}
    />
  )
}
