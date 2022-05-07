import Grid from "@mui/material/Grid";
import ReactEcharts from "echarts-for-react";
import option from "src/configure/ChartConfigDemo"
import actions from "src/actions";
import {useEffect, useState} from "react";
import _ from "lodash";

export default () => {

  const [data, setData] = useState();

  useEffect(async () => {
    const res = await actions.getStat({
      pid: "",
      op: "all"
    });
    setData(res.stat);
  }, []);

  return (
    <>
      {
        !_.isEmpty(data)
          ? <Grid container rowSpacing={20}>
            <Grid item xs={6}>
              <ReactEcharts option={data[1]}/>
            </Grid>
            <Grid item xs={6}>
              <ReactEcharts option={data[0]}/>
            </Grid>
            <Grid item xs={12}>
              <ReactEcharts
                option={data[2]}
                style={{height:600}}
              />
            </Grid>
          </Grid>
          : <div></div>
      }
    </>
  )
}