/**
 * @file api
 * @author Mingze Ma
 */

import axios from "axios";

const BASE_URL = 'http://localhost:8000'

export class Api {
  constructor() {
    this.axiosInstance = axios.create({
      baseURL: BASE_URL,
    });

    this.axiosInstance.defaults.withCredentials = true;

    this.axiosInstance.interceptors.response.use((response) => {
      if (response.status === 200) {
        const { data } = response;
        return data;
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
