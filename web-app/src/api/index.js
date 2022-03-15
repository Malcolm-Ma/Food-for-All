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
  }

  get(url, data, options) {
    return this.axiosInstance(url, {
      method: 'get',
      params: data,
      ...options,
    });
  }

  post(url, data, options) {
    this.axiosInstance(url, {
      method: 'post',
      data,
      ...options,
    });
  }
}

export default new Api();
