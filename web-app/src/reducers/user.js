/**
 * @file user reducer
 * @author Mingze Ma
 */

import {
  SET_USER_INFO,
} from 'src/constants/actionTypes';

const initialState = {
  userInfo: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_USER_INFO: {
      const { userInfo = {} } = action.payload;
      return {
        ...state,
        userInfo,
      };
    }
    default: {
      return {
        ...state,
      };
    }
  }
};
