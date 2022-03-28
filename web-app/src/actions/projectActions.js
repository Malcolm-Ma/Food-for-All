/**
 * @file project actions
 * @author Mingze Ma
 */

import _ from 'lodash';

import api from "src/api";
import apiConfig from "src/api/apiConfig";

export const getProjectList = params => {
  if (_.isNil(params)) {
    return api.get(apiConfig.projectList, params);
  }
  return api.post(apiConfig.projectList, params);
};

export const createProject = params => api.get(apiConfig.createProject, params);

export const editProject = params => api.post(apiConfig.editProject, params);

export const stopProject = params => api.post(apiConfig.stopProject, params);

export const getProjectInfo = params => api.post(apiConfig.projectInfo, params);

export const prepareProject = params => api.get(apiConfig.prepareProject, params);
