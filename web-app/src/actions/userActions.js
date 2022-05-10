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
    await api.post(apiConfig.login, params);
    return await dispatch(getUserInfo());
  } catch (e) {
    if (e.status !== 0) {
      return Promise.reject(e);
    }
  }
};

export const getUserInfo = () => async (dispatch) => {
  try {
    const { user_info: userInfo } = await api.get(apiConfig.userInfo);
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

export const getUserInfoById = params => api.post(apiConfig.userInfo, params);

export const register = params => api.post(apiConfig.register, params);

export const logout = params => api.get(apiConfig.logout, params);

export const editUser = params => api.post(apiConfig.editUser, params);

export const payByDonator = params => api.post(apiConfig.payByDonator, params);

export const capturePayment = params => api.post(apiConfig.capturePayment, params);

export const resetPassword = params => api.post(apiConfig.resetPassword, params);
