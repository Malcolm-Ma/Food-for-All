import Grid from "@mui/material/Grid";
import ReactEcharts from "echarts-for-react";
import option from "src/configure/ChartConfigDemo"
import actions from "src/actions";
import {useEffect, useState} from "react";
import _ from "lodash";
import {ToggleButtonGroup} from "@mui/material";
import ToggleButton from "@mui/material/ToggleButton";

export default () => {

  const [data, setData] = useState();
  const [time, setTime] = useState("half month")

  useEffect(async () => {
    const res = await actions.getStat({
      pid: "",
      op: time
    });
    setData(res.stat);
  }, [time]);

  const handleChange = (event, newTime) => {
    setTime(newTime);
  }

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

              <ToggleButtonGroup
                color="primary"
                value={time}
                exclusive
                onChange={handleChange}
              >
                <ToggleButton value="week">Last Week</ToggleButton>
                <ToggleButton value="half month">Half Month</ToggleButton>
                <ToggleButton value="month">Last Month</ToggleButton>
                <ToggleButton value="all">All</ToggleButton>
              </ToggleButtonGroup>

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