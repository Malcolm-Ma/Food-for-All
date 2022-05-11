/**
 * @file project constant
 * @author Mingze Ma
 */

export const STATUS_CODE = {
  "success": 0,
  "user has not logged in": 100001,
  "user update failed": 100002,
  "operation is not available to individual user": 100003,
  "user is already logged in": 100004,
  "invalid username": 100005,
  "wrong password": 100006,
  "email is already registered": 100007,
  "password setting failed": 100008,
  "email is not registered": 100009,
  "mismatch between logged in user and target user": 100010,
  "invalid user type": 100011,
  "wrong parameters for user creation": 100012,
  "user creation failed": 100013,
  "target user does not exist": 100014,
  "project creation failed": 200001,
  "project does not exist": 200002,
  "user is not the owner of the project": 200003,
  "project is not deletable": 200004,
  "project update failed": 200005,
  "project is not editable": 200006,
  "project information is incomplete": 200007,
  "project start up failed": 200008,
  "project has already started": 200009,
  "project stop failed": 200010,
  "project is not ongoing or on hold": 200011,
  "project end time is invalid": 200012,
  "project status invalid": 200013,
  "project price invalid": 200014,
  "project order invalid": 200015,
  "project is already finished": 200016,
  "project is not ongoing": 200017,
  "project suspension failed": 200018,
  "invalid currency type": 300001,
  "email delivery failed": 300002,
  "captcha verification failed": 300003,
  "invalid action": 300004,
  "write to file failed": 300005,
  "wrong region name or code": 300006,
  "invalid request parameters": 400001,
  "unable to get image file from request": 400002,
  "unable to get document file from request": 400003,
  "temporary ban due to too frequent login attempts": 400004,
  "create paypal product failed": 500001,
  "payment capture failed": 500002,
}

export const SERVICE_BASE_URL = 'http://localhost:8000/'

export const DEFAULT_CURRENCY = 'GBP';

export const SECRET_KEY = 'apex-food-for-all';
