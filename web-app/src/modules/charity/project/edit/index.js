import React, {useEffect} from "react";
import {useDispatch} from "react-redux";
import actions from "src/actions";

export default () => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(actions.getProjectInfo({
      // @Todo change params
      pid: "21726c8a19073d9f5b46fd074be8bbb0",
      currency_type: "GBP",
    }))
  })

  return (
    <span>1</span>
  );
};