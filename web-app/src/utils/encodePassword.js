/**
 * @file utils for encode password
 * @author Mingze Ma
 */
import _ from "lodash";

export const ENCODE_KEY = '85';

export const encode = (password = '') => {
  const encodePassword = _.map(password, (str) => {
    return String.fromCharCode(str.charCodeAt() ^ ENCODE_KEY);
  }).join('');
  return btoa(encodePassword);
};
