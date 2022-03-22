/**
 * @file action entry
 * @author Mingze Ma
 */

import * as userActions from './userActions';
import * as projectActions from './projectActions';

import * as globalActions from './globalActions';

export default {
  ...userActions,
  ...projectActions,
  ...globalActions,
};
