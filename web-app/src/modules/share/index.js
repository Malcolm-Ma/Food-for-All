/**
 * @file share and payment success page
 * @author Mingze Ma
 */

// module import
import {} from 'react';

// style import
import './index.less';
import Box from "@mui/material/Box";
import Typography from '@mui/material/Typography';
import Button from "@mui/material/Button";
import * as React from "react";
import {Image} from "antd";
import success from 'src/modules/share/success.jpg'

export default (props) => {

  return (
    <div align="center">
      <Box align="center" textAlign="center"
           sx={{width: '100%', maxWidth: 500}}>
        <img src={success} alt="success" />
        <Typography variant="h5" component="div" gutterBottom>
            You have successfully donated!
            Thank you very much. We hope you will be able to share this project with more people.
        </Typography>

        <Button size="large" variant="outlined" href='project'>Confirm</Button>
      </Box>
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
