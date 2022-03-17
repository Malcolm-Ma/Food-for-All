/**
 * @file Project creating page
 * @author Mingze Ma
 */

import { useSelector } from 'react-redux';
import { useEffect } from "react";

export default () => {

  const { userInfo } = useSelector(state => state.user);

  useEffect(() => {
    console.log('--userInfo--\n', userInfo);
  }, [userInfo]);

  return (
    <div></div>
  );
};
