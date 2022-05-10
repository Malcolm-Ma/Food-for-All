/**
 * @file entrance of payment&detail page
 * @author Mingze Ma
 */

// module import
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import _ from 'lodash';

// style import
import './index.less';
import actions from "src/actions";
import { useSelector } from "react-redux";
import Box from "@mui/material/Box";

import { SERVICE_BASE_URL } from "src/constants/constants";
import Grid from "@mui/material/Grid";
import { Container, CssBaseline, Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import PaymentForm from "src/modules/donation/PaymentForm";

export default (props) => {
  const {} = props;
  const { pid } = useParams();

  const { userinfo } = useSelector(state => state.user);
  const { regionInfo } = useSelector(state => state.global);

  const [projectDetail, setProjectDetail] = useState();

  useEffect(() => {
    if (!_.isEmpty(regionInfo)) {
      (async () => {
        try {
          const res = await actions.getProjectInfo({
            pid,
            currency_type: regionInfo.currencyType,
          });
          setProjectDetail(res.project_info);
        } catch (e) {
          console.error(e);
        }
      })();
    }
  }, [pid, regionInfo, userinfo]);

  const theme = createTheme();
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {
        projectDetail ? <>
            <Box
              sx={{
                backgroundImage: `url(${SERVICE_BASE_URL}${_.get(projectDetail, 'background_image')})`,
                position: 'absolute',
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                zIndex: -2,
              }}
            >
            </Box>
            <Box
              sx={{
                position: 'absolute',
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                backgroundColor: 'rgba(61, 92, 118, 0.7)',
                // opacity: 0.7,
                zIndex: -1,
              }}
            >
            </Box>
            <Grid
              className="donation"
              container={true}
              sx={{
                zIndex: 2,
                pt: 12,
              }}
            >
              <Grid item sm={6} sx={{ color: 'white' }}>
                <Container component="div" maxWidth="sm" sx={{ p: { xs: 0, sm: 2 } }}>
                  <Typography variant="h4" sx={{ color: 'white' }}>
                    {_.get(projectDetail, 'title', '')}
                  </Typography>
                  <Typography variant="body1" sx={{ pt: 6 }}>
                    {_.get(projectDetail, 'details', '')}
                  </Typography>
                  <Typography variant="h4" sx={{ pt: 8, color: 'white' }}>
                    Please donate now, it only takes a minute.
                  </Typography>
                </Container>
              </Grid>
              <Grid item sm={6}>
                <PaymentForm projectDetail={projectDetail} />
              </Grid>
            </Grid>
          </>
          : <>

          </>
      }
    </ThemeProvider>
  );
};
