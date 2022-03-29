/**
 * @file utils
 * @author Mingze Ma
 */

import _ from "lodash";

/**
 * Reformat data to label, value object
 * @param data Data source
 * @param labelName
 * @param valueName
 * @returns {unknown[]} List of options
 */
export const reformatOptions = (data = [], labelName = '', valueName = '') => {
  return _.map(data, (item) => {
    const label = item[labelName];
    const value = item[valueName];

    return { label, value };
  });
};

export const reformatToMap = (data = [], keyName = '', valueName = '') => {
  return _.reduce(data, (result, item) => {
    const key = item[keyName];
    const value = item[valueName];
    result[key] = value;

    return result;
  }, {});
}
