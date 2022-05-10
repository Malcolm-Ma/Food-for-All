/**
 * @file global actions
 * @author Mingze Ma
 */

import axios from 'axios';
import _ from "lodash";

import { reformatOptions, reformatToMap } from 'src/utils/utils'

import api from "../api";
import apiConfig from "../api/apiConfig";
import { SET_REGION_LIST, SET_CURRENCY_LIST, SET_COUNTRY_CODE } from "../constants/actionTypes";
import { DEFAULT_CURRENCY, SERVICE_BASE_URL } from "src/constants/constants";

export const getRegionList = (params) => async (dispatch) => {
  try {
    let { region_list: regionList } = await api.get(apiConfig.regionList, params);
    const regionMap = reformatToMap(regionList, 'code', 'region');
    regionList = reformatOptions(regionList, 'region', 'code');
    dispatch({
      type: SET_REGION_LIST,
      payload: { regionList, regionMap },
    });
    return regionList;
  } catch (e) {
    dispatch({
      type: SET_REGION_LIST,
      payload: {
        regionList: [],
        regionMap: {},
      },
    });
  }
}

export const getCurrencyList = (params) => async (dispatch) => {
  try {
    let { currency_list: currencyList } = await api.get(apiConfig.currencyList, params);
    const currencyMap = reformatToMap(currencyList, 'code', 'currency_type');
    currencyList = reformatOptions(currencyList, 'currency_type', 'code');
    dispatch({
      type: SET_CURRENCY_LIST,
      payload: { currencyList, currencyMap },
    });
    return currencyList;
  } catch (e) {
    dispatch({
      type: SET_CURRENCY_LIST,
      payload: {
        currencyList: [],
        currencyMap: {},
      },
    });
  }
}

export const getRegionInfo = () => async (dispatch) => {
  try {
    const { data } = await axios.get(apiConfig.ipInfo);
    const countryCode = _.get(data, 'country_code', 'GB');
    const { region2currency: regionToCurrency } = await api.get(apiConfig.regionToCurrency);
    const currencyType = (() => {
      const type = _.get(regionToCurrency, countryCode);
      if (!type) {
        return DEFAULT_CURRENCY;
      }
      return type;
    })();

    const regionInfo = {
      countryCode,
      currencyType,
    };
    dispatch({
      type: SET_COUNTRY_CODE,
      payload: { regionInfo },
    });
    return data;
  } catch (e) {
    dispatch({
      type: SET_COUNTRY_CODE,
      payload: {
        regionInfo: {
          countryCode: 'GB',
          currencyType: DEFAULT_CURRENCY,
        }
      },
    });
  }
};

export const uploadImage = params => api.post(apiConfig.upLoadImg, params);

export const getStat = params => api.post(apiConfig.getStat, params);

export const getReport = async (params = { pid: '' }) => {
  const res = await api.post(apiConfig.report, params);
  const { url } = res;
  window.open(`${SERVICE_BASE_URL}${url}`, '_blank');
  return res;
};
