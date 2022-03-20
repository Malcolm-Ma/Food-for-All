import api from "src/api";
import apiConfig from "src/api/apiConfig";

export const createProject = params => api.get(apiConfig.createProject, params);