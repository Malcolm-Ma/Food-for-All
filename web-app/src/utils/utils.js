/**
 * @file utils
 * @author Mingze Ma
 */

import _ from "lodash";

export const reformatOptions = (data = [], labelName = '', valueName = '') => {
  return _.map(data, (item) => {
    const label = item[labelName];
    const value = item[valueName];

    return { label, value };
  })
};
