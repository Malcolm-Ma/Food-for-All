/**
 * @file user action
 * @author Mingze Ma
 */
import api from "../api";
import apiConfig from "../api/apiConfig";

export const login = params => api.post(apiConfig.login, params);
