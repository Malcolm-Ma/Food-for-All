import api from "src/api";
import apiConfig from "src/api/apiConfig";
import {SET_PROJECT_INFO} from "src/constants/actionTypes";

export const getCreateResult = () => async (dispatch) => {
  try {
    const createResult = await api.get(apiConfig.createProject);
    console.log('--createResult--\n', createResult);
    dispatch({
      type: SET_PROJECT_INFO,
      payload: { createResult },
    });
    return createResult;
  } catch (e) {
    dispatch({
      type: SET_PROJECT_INFO,
      payload: {
        createResult: {},
      },
    });
  }
}