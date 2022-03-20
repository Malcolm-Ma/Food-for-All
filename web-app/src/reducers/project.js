import {
  SET_PROJECT_INFO,
} from 'src/constants/actionTypes';

const initialState = {
  createResult: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_PROJECT_INFO: {
      const { createResult = {} } = action.payload;
      return {
        ...state,
        createResult,
      };
    }
    default: {
      return {
        ...state,
      };
    }
  }
};
