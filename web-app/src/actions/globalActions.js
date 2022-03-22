/**
 * @file global actions
 * @author Mingze Ma
 */

import api from "../api";
import apiConfig from "../api/apiConfig";
import { SET_REGION_LIST, SET_CURRENCY_LIST } from "../constants/actionTypes";

export const getRegionList = (params) => async (dispatch) => {
  try {
    const { region_list: regionList } = await api.get(apiConfig.regionList, params);
    console.log('--regionList--\n', regionList);
    dispatch({
      type: SET_REGION_LIST,
      payload: { regionList },
    });
    return regionList;
  } catch (e) {
    dispatch({
      type: SET_REGION_LIST,
      payload: {
        regionList: [],
      },
    });
  }
}

export const getCurrencyList = (params) => async (dispatch) => {
  try {
    const { currency_list: currencyList } = await api.get(apiConfig.currencyList, params);
    console.log('--currencyList--\n', currencyList);
    dispatch({
      type: SET_CURRENCY_LIST,
      payload: { currencyList },
    });
    return currencyList;
  } catch (e) {
    dispatch({
      type: SET_CURRENCY_LIST,
      payload: {
        currencyList: [],
      },
    });
  }
}
