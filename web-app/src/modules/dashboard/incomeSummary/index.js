import Grid from "@mui/material/Grid";
import ReactEcharts from "echarts-for-react";
import option from "src/configure/ChartConfigDemo"

export default () => {
  return (
    <Grid container rowSpacing={20}>
      <Grid item xs={6}>
        <ReactEcharts option={option[1]}/>
      </Grid>
      <Grid item xs={6}>
        <ReactEcharts option={option[0]}/>
      </Grid>
      <Grid item xs={12}>
        <ReactEcharts
          option={option[2]}
          style={{height:600}}
        />
      </Grid>
    </Grid>
  )
}