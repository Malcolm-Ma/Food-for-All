/**
 * @file api
 * @author Mingze Ma
 */

import axios from "axios";
import _ from 'lodash';

import { STATUS_CODE, SERVICE_BASE_URL } from 'src/constants/constants';

export class Api {
  constructor() {
    this.axiosInstance = axios.create({
      baseURL: SERVICE_BASE_URL,
    });

    this.codeStatus = _.reduce(STATUS_CODE, (result, value, key) => {
      result[value] = key;
      return result;
    }, {})

    this.axiosInstance.defaults.withCredentials = true;

    this.axiosInstance.interceptors.response.use((response) => {
      if (response.status === 200) {
        const { data } = response;
        const { status, ...otherProps } = data;

        if (status !== 0) {
          return Promise.reject({ status, name: this.codeStatus[status] })
        }

        return otherProps;
      } else {
        message.error('Fall to request：' + response.status);
      }
    }, (error) => {
      message.error('Network Error, please try again');
      return Promise.reject(error);
    });
  }

  get(url, data, options) {
    return this.axiosInstance(url, {
      method: 'get',
      params: data,
      ...options,
    });
  }

  post(url, data, options) {
    return this.axiosInstance(url, {
      method: 'post',
      data,
      ...options,
    });
  }
}

export default new Api();
