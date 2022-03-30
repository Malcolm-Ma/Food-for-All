/**
 * @file global reducer
 * @author Mingze Ma
 */

import {
  SET_REGION_LIST,
  SET_CURRENCY_LIST,
} from 'src/constants/actionTypes';

const initialState = {
  regionList: [],
  regionMap: {},
  currencyList: [],
  currencyMap: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_REGION_LIST: {
      const { regionList = [], regionMap } = action.payload;
      return {
        ...state,
        regionList,
        regionMap,
      };
    }
    case SET_CURRENCY_LIST: {
      const { currencyList = [] } = action.payload;
      return {
        ...state,
        currencyList,
      };
    }
    default: {
      return {
        ...state,
      };
    }
  }
};
