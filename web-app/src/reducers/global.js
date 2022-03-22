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
  currencyList: [],
};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_REGION_LIST: {
      const { regionList = [] } = action.payload;
      return {
        ...state,
        regionList,
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
