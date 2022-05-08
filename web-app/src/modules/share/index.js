/**
 * @file share and payment success page
 * @author Mingze Ma
 */

// module import
import {useEffect, useMemo, useState} from 'react';
import {useSearchParams} from 'react-router-dom';
import _ from 'lodash';
import {message} from 'antd';
import {useNavigate} from "react-router-dom";

// style import
import './index.less';
import Box from "@mui/material/Box";
import Typography from '@mui/material/Typography';
import Button from "@mui/material/Button";
import * as React from "react";
import success from 'src/assets/success.jpg'
import {Checkbox, FormControlLabel, FormGroup, TextField} from "@mui/material";
import {Result} from 'antd';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import actions from "src/actions";
import CryptoJS from "crypto-js";
import {SECRET_KEY} from "src/constants/constants";
import moment from "moment";
import {useSelector} from "react-redux";
import Grid from "@mui/material/Grid";

export default (props) => {

    const {regionInfo} = useSelector(state => state.global);

    const [searchParams] = useSearchParams();
    const token = useMemo(() => (searchParams.get('token')), [searchParams]);

    const [loading, setLoading] = useState(true);

    const [sharedProject, setSharedProject] = useState(null);

    const [errorEmail01, setErrorEmail01] = useState(false);
    const [errorEmail02, setErrorEmail02] = useState(false);
    // decode token, including donor's name
    const [decodeToken, setDecodeToken] = useState({});

    const navigate = useNavigate();

    const [errorMessage, setErrorMessage] = useState('');
    //Set Dialog Status
    const [open, setOpen] = React.useState(false);
    const [dialogText, setDialogText] = useState('');

    const handleClickOpen = async (event) => {
        setOpen(true);
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        console.log({
            email01: data.get('email01'),
            email02: data.get('email02'),
            hide: data.get('hide'),
        });
        //error email set
        let email01 = data.get('email01');
        let email02 = data.get('email02');
        if (!(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(email01)) && email01 !== '')
            setErrorEmail01(true);
        else setErrorEmail01(false);
        if (!(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(email02)) && email02 !== '')
            setErrorEmail02(true);
        else setErrorEmail02(false);
        if (errorEmail01 || errorEmail02) {
            setDialogText('Your email is in the wrong format, please re-enter it.')
        } else {
            if (data.get('email01') === '' && data.get('email02') === '') {
                setDialogText("Are you sure you don't want to share the project with others?")
            } else {
                setDialogText("Thank you for sharing。")
            }
            let hideStatus = 0;
            if (data.get('hide') === 'on') {
                hideStatus = 1;
            }
            try {
                await actions.shareByEmail({
                    "mail": [data.get('email01'), data.get('email02')],
                    "project_name": _.get(sharedProject, 'title'),
                    "project_url": window.location.origin + "/donation/" + _.get(sharedProject, 'pid'),
                    "donate_num": _.get(decodeToken, 'donation_count'),
                    "if_hide_personal_information": hideStatus,
                    "user_name": _.get(decodeToken, 'first_name') + " " + _.get(decodeToken, 'last_name')
                });
            } catch (e) {
                message.error(e.name);
            }
        }
    };

    const handleClose = () => {
        setOpen(false);
    };
    const handleOk = () => {
        setTimeout(() => {
            setOpen(false);
            if (!(errorEmail01 || errorEmail01)) {
                navigate('/project');
            }
        }, 500);

    }

    useEffect(() => {
        const validToken = _.replace(token, /[\s]/g, '+');
        const decodeParams = JSON.parse(CryptoJS.AES.decrypt(validToken, SECRET_KEY).toString(CryptoJS.enc.Utf8));
        setDecodeToken(decodeParams);
        // check the auth of showing project
        const localToken = window.localStorage.getItem('pid');
        if (!decodeParams.pid || !_.isEqual(localToken, decodeParams.pid)) {
            setErrorMessage('Invalid project id! ');
            message.error('Invalid project id! ');
            return;
        }
        const paymentId = window.localStorage.getItem('p_id');
        if (!paymentId) {
            setErrorMessage('Invalid payment! ');
            message.error('Invalid payment! ');
            return;
        }
        if (!moment(decodeParams.ttl).isAfter()) {
            setErrorMessage('The session time has expired.');
            message.error('The session time has expired.');
            return;
        }
        // fetch payment result and project info
        (async () => {
            try {
                await actions.capturePayment({
                    "pid": decodeParams.pid,
                    "num": decodeParams.donation_count,
                    "payment_id": paymentId,
                    "plan": decodeParams.plan,
                })
            } catch (e) {
                message.error(e);
            }
            setLoading(false);
        })();
        (async () => {
            try {
                const res = await actions.getProjectInfo({
                    'pid': decodeParams.pid,
                    'currency_type': regionInfo.currencyType,
                });
                setSharedProject(_.get(res, 'project_info'));
            } catch (e) {
                message.error(e);
            }
            setLoading(false);
        })();
    }, [regionInfo.currencyType, token]);

    return (
        <div align="center">
            {
                !loading
                    ? <>{
                        token
                            ? <>{
                                sharedProject ? <div>
                                        <Box align="center" textAlign="center"
                                             sx={{width: '100%', maxWidth: 600, padding: 3}}>
                                            <img src={success} alt="success"/>
                                            <Typography variant="h5" component="div" gutterBottom>
                                                You have successfully donated!
                                            </Typography>
                                            <Typography variant="h5" component="div" gutterBottom>
                                                Thank you very much. We hope you will be able to
                                                share this project with more people.
                                            </Typography>
                                        </Box>
                                        <Box
                                            component="form"
                                            noValidate
                                            autoComplete="off"
                                            align={"center"}
                                            onSubmit={handleClickOpen}
                                        >
                                            <Grid container spacing={3} justifyContent="center">
                                                <Grid item xs={8} md={6}>
                                                    <TextField error={errorEmail01} fullWidth name="email01" label="email"
                                                               variant="outlined"/>
                                                </Grid>
                                                <Grid item xs={8} md={6}>
                                                    <TextField error={errorEmail02} fullWidth name="email02" label="email"
                                                               variant="outlined"/>
                                                </Grid>
                                                <Grid item xs={12}>
                                                    <FormGroup>
                                                        <FormControlLabel  name="hide" control={<Checkbox/>}
                                                                          label=" Hide personal information in emails"/>
                                                    </FormGroup>
                                                </Grid>
                                                <Grid item xs={12}>
                                                    <Button type="submit" size="large" variant="outlined">Confirm</Button>
                                                </Grid>
                                            </Grid>
                                            <Dialog
                                                open={open}
                                                onClose={handleClose}
                                                aria-labelledby="alert-dialog-title"
                                                aria-describedby="alert-dialog-description"
                                                maxWidth='sm'
                                                fullWidth={true}
                                            >
                                                <DialogTitle id="alert-dialog-title">
                                                    {"Share"}
                                                </DialogTitle>
                                                <DialogContent>
                                                    <DialogContentText id="alert-dialog-description">
                                                        {dialogText}
                                                    </DialogContentText>
                                                </DialogContent>
                                                <DialogActions>
                                                    <Button onClick={handleClose}>Cancel</Button>
                                                    <Button onClick={handleOk}
                                                            autoFocus>
                                                        Ok
                                                    </Button>
                                                </DialogActions>
                                            </Dialog>
                                        </Box>
                                    </div>
                                    : <Result
                                        status="error"
                                        title="Invalid Token"
                                        subTitle={errorMessage}
                                        extra={[
                                            <Button size="medium" variant="outlined" href='project'>Go Back</Button>
                                        ]}
                                    />
                            }</>
                            : <div>
                                <Result
                                    status="403"
                                    title="403"
                                    subTitle="Sorry, you are not authorized to access this page."
                                    extra={<Button size="large" variant="outlined" href='project'>Back Home</Button>}
                                />
                            </div>

                    }</>
                    : <div>loading</div>
            }
        </div>
    );
    /**
     * <Dialog open={openDialog} onClose={handleClose}>
     *               <DialogTitle>Share</DialogTitle>
     *               <DialogContent dividers={true}>
     *                 <Typography variant="h6" sx={{pb: 2}}>
     *                   Share By Twitter
     *                 </Typography>
     *                 <TwitterShareButton
     *                     url={`${window.location.href}/${_.get(projectDetail, 'pid')}`}
     *                     options={{
     *                       size: 'large',
     *                       text: 'Apex - Food For All',
     *                     }}
     *                 />
     *               </DialogContent>
     *               <DialogContent>
     *                 <Typography variant="h6">
     *                   Share By Email
     *                 </Typography>
     *                 <DialogContentText>
     *                   Please input the email of the friend you want to share,
     *                   we will send the project information to your friend.
     *                 </DialogContentText>
     *                 <TextField
     *                     autoFocus
     *                     margin="dense"
     *                     id="name"
     *                     label="Email Address"
     *                     type="email"
     *                     fullWidth
     *                     variant="standard"
     *                 />
     *               </DialogContent>
     *               <DialogActions>
     *                 <Button onClick={handleClose}>Cancel</Button>
     *                 <Button onClick={handleClose} href='share'>Share</Button>
     *               </DialogActions>
     *             </Dialog>
     */
}
