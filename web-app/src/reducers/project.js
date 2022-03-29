import {
  SET_PROJECT_INFO,
} from 'src/constants/actionTypes';

const initialState = {
  projectInfo: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_PROJECT_INFO: {
      const { projectInfo = {} } = action.payload;
      return {
        ...state,
        projectInfo,
      };
    }
    default: {
      return {
        ...state,
      };
    }
  }
};