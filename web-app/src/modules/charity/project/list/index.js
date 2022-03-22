/**
 * @file Project list page
 * @author Mingze Ma
 */
import { useCallback, useEffect, useState } from "react";

import actions from "src/actions";
import _ from "lodash";

export default () => {

  const [projectInfo, setProjectInfo] = useState({});

  const getProjectList = useCallback(async () => {
    try {
      const res = await actions.getProjectList();
      setProjectInfo(res);
      console.log('--res--\n', res);
    } catch (e) {
      console.error(e);
    }
  }, []);

  useEffect(() => {
    getProjectList().catch(err => console.error(err));
  }, [getProjectList]);

  return (
    <div>
      {_.map(_.get(projectInfo, 'project_info'), (item) => {
        return (
          <div key={item.pid}>{item.title}</div>
        );
      })}
    </div>
  );

};
