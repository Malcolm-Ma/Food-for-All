import {Button, Form} from "antd";
import React from "react";
import {useNavigate} from "react-router-dom";

export default () => {

  const navigate = useNavigate();


  function edit() {
    navigate('/project/edit');
  };

  return (
    <Form.Item wrapperCol={{offset: 6}}>
      <Button type="primary" htmlType="submit" onClick={edit}>
        Submit
      </Button>
    </Form.Item>
  );
};