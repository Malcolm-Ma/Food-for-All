/**
 * @file global actions
 * @author Mingze Ma
 */

import axios from 'axios';

import api from "../api";
import apiConfig from "../api/apiConfig";
import { SET_REGION_LIST, SET_CURRENCY_LIST } from "../constants/actionTypes";

import { reformatOptions, reformatToMap } from 'src/utils/utils'

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
    console.log('--currencyList--\n', currencyList);
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

export const getIpInfo = () => axios.get(apiConfig.ipInfo);

export const uploadImage = params => api.post(apiConfig.upLoadImg, params);

