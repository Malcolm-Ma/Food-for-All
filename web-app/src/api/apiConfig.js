import {getProjectsList} from "src/actions/projectActions";

/**
 * @file API config
 * @author Mingze Ma
 */

export default {
  login: '/login/',
  userInfo: '/get_user/',
  createProject: '/create_project/',
  editProject: '/edit_project/',
  register: '/regis/',
  regionList: '/region_list/',
  currencyList: '/currency_list/',
  logout: '/logout/',
  projectList: '/get_projects_list/',
  projectInfo: '/get_project/',
  editUser: '/edit_user/',
  prepareProject: '/get_prepare_projects_list/',
  stopProject:'/stop_project/',
  getProjectInfo:'/get_project/',
  startProject:'/start_project/',
  suspendProject:'/suspend_project/',
  deleteProject:'/delete_project/',
  shareByEmail:'/share_by_email/',
  upLoadImg: '/upload_img/',
  ipInfo: 'https://geolocation-db.com/json/',
  regionToCurrency: '/region2currency/',
  payByDonator:'/pay/',
  capturePayment:'/capture_payment/',
  getStat: '/get_stat/',
  resetPassword: '/reset_password/',
  report: '/get_report/',
};
