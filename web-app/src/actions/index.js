/**
 * @file action entry
 * @author Mingze Ma
 */

import * as userActions from './userActions';
import * as globalActions from './globalActions';

export default {
  ...userActions,
  ...globalActions,
};
