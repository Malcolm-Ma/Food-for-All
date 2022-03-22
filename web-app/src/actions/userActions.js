/**
 * @file user action
 * @author Mingze Ma
 */
import _ from 'lodash';
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
    const isLoggedIn = !!_.get(userInfo, 'uid');

    dispatch({
      type: SET_USER_INFO,
      payload: {
        userInfo: {
          ...userInfo,
          isLoggedIn,
        }
      },
    });
    return userInfo;
  } catch (e) {
    dispatch({
      type: SET_USER_INFO,
      payload: {
        userInfo: {
          isLoggedIn: false,
        },
      },
    });
  }
}

export const register = params => api.post(apiConfig.register, params);

export const logout = params => api.get(apiConfig.logout, params);
