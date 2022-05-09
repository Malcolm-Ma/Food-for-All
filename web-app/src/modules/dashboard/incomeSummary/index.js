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
  const [time, setTime] = useState("half month");
  const [res, setRes] = useState();

  const handleChange = (event, newTime) => {
    setTime(newTime);
    let days = 0;
    switch (newTime) {
      case 'half month':
        days = 15;
        break;
      case 'month':
        days = 30;
        break;
      case 'week':
        days = 7;
        break;
      case 'all':
        days = 0;
        break;
    }
    initData(days);
  }

  function initData(days) {
    const originalData = _.cloneDeep(res);
    const date = originalData.stat['date'].slice(-days);
    const title = originalData.stat['title'];
    const pie = originalData.stat['pie'];
    const progress = originalData.stat['progress'];
    const history = originalData.stat['history'];

    for (const v of progress) {
      v['data'] = v['data'].slice(-days)
    }

    for (const v of history) {
      v['data'] = v['data'].slice(-days)
    }

    setData({
      '0': {
        'title': {
          'text': 'Donation Line'
        },
        'tooltip': {
          'trigger': 'axis'
        },
        'legend': {
          'data': title
        },
        'grid': {
          'left': '3%',
          'right': '4%',
          'bottom': '3%',
          'containLabel': 'true'
        },
        'toolbox': {
          'feature': {
            'saveAsImage': {}
          }
        },
        'xAxis': {
          'type': 'category',
          'boundaryGap': 'false',
          'data': date
        },
        'yAxis': {
          'type': 'value',
          'axisLabel': {
            'show': 'true',
            'formatter': '{value}%',
          },
          'show': 'true'
        },
        'series': progress
      },
      '1': {
        'title': {
          'text': 'Donation Location',
          'left': 'center'
        },
        'tooltip': {
          'trigger': 'item'
        },
        'legend': {
          'type': 'scroll',
          'orient': 'vertical',
          'left': 'left'
        },
        'series': [
          {
            'name': 'Access From',
            'type': 'pie',
            'radius': '50%',
            'data': pie,
            'emphasis': {
              'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      '2': {
        'title': {
          'text': 'Donation History'
        },
        'tooltip': {
          'trigger': 'axis',
          'axisPointer': {
            'type': 'shadow'
          }
        },
        'legend': {},
        'grid': {
          'left': '3%',
          'right': '4%',
          'bottom': '3%',
          'containLabel': 'true'
        },
        'xAxis': {
          'type': 'value'
        },
        'yAxis': {
          'type': 'category',
          'data': date
        },
        'series': history
      }
    });
  }

  useEffect(async () => {
    const r = await actions.getStat({
      pid: ""
    });
    setRes(r);
  }, []);

  useEffect(() => {
    if (!_.isNil(res)) {
      initData(15);
    }
  }, [res]);

  return (
    <>
      {
        (!_.isEmpty(data))
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
          : <div>loading</div>
      }
    </>
  )
}