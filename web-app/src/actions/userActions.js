/**
 * @file user action
 * @author Mingze Ma
 */
import api from "src/api";
import apiConfig from "src/api/apiConfig";
import { SET_USER_INFO } from 'src/constants/actionTypes';

export const login = params => async (dispatch) => {
  try {
    const loginRes = await api.post(apiConfig.login, params);
    if (loginRes.status !== 0) {
      return loginRes;
    }
    return await dispatch(getUserInfo());
  } catch (e) {
    console.error(e);
  }
};

export const getUserInfo = () => async (dispatch) => {
  try {
    const userInfo = await api.get(apiConfig.userInfo);
    console.log('--userInfo--\n', userInfo);
    dispatch({
      type: SET_USER_INFO,
      payload: { userInfo },
    });
    return userInfo;
  } catch (e) {
    dispatch({
      type: SET_USER_INFO,
      payload: {
        userInfo: {},
      },
    });
  }
}

export const register = params => api.post(apiConfig.register, params);
