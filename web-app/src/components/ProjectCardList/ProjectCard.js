/**
 * @file project Card component
 * @author Mingze Ma
 */
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import _ from "lodash";
import { SERVICE_BASE_URL } from "src/constants/constants";
import moment from "moment";
import Button from "@mui/material/Button";
import { TwitterShareButton } from 'react-twitter-embed';

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

export default function ShowProjectCard(props) {
  const [expanded, setExpanded] = React.useState(false);
  const [openDialog, setOpenDialog] = React.useState(false);

  const handleClickOpen = () => {
    setOpenDialog(true);
  };

  const handleClose = () => {
    setOpenDialog(false);
  };

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const { project } = props;

  function stringToColor(string) {
    let hash = 0;
    let i;

    /* eslint-disable no-bitwise */
    for (i = 0; i < string.length; i += 1) {
      hash = string.charCodeAt(i) + ((hash << 5) - hash);
    }

    let color = '#';

    for (i = 0; i < 3; i += 1) {
      const value = (hash >> (i * 8)) & 0xff;
      color += `00${value.toString(16)}`.slice(-2);
    }
    /* eslint-enable no-bitwise */

    return color;
  }

  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardHeader
        avatar={
          <IconButton href={`/account/charity_profile/${_.get(project, 'uid')}`}>
            <Avatar sx={{ bgcolor: stringToColor(_.get(project, 'region')) }} aria-label="recipe">
              {_.get(project, 'region')}
            </Avatar>
          </IconButton>
        }
        action={
          <Button endIcon={<MoreVertIcon />} href={`/donation/${project.pid}`}>
          </Button>
        }
        title={
          <span className="card-header">{_.get(project, 'title')}</span>
        }
        subheader={moment(_.get(project, 'end_time') * 1000).format("MMM DD, YYYY")}
      />
      <CardMedia
        component="img"
        height="194"
        image={SERVICE_BASE_URL + _.get(project, 'background_image')}
        alt={_.get(project, 'background_image')}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary" noWrap={true}>
          {_.get(project, 'intro')}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <Button size="small" onClick={handleClickOpen}>Share</Button>
        <Dialog open={openDialog} onClose={handleClose}>
          <DialogTitle>Share</DialogTitle>
          <DialogContent dividers={true}>
            <Typography variant="h6" sx={{pb: 2}}>
              Share By Twitter
            </Typography>
            <TwitterShareButton
              url={`${window.location.href}/${_.get(project, 'pid')}`}
              options={{
                size: 'large',
                text: 'Apex - Food For All',
              }}
            />
          </DialogContent>
          <DialogContent>
            <Typography variant="h6">
              Share By Email
            </Typography>
            <DialogContentText>
              Please input the email of the friend you want to share,
              we will send the project information to your friend.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Email Address"
              type="email"
              fullWidth
              variant="standard"
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleClose} href='share'>Share</Button>
          </DialogActions>
        </Dialog>
        <Button size="small" href={`/donation/${project.pid}`}>Donate</Button>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {_.get(project, 'intro')}
        </CardContent>
      </Collapse>
    </Card>
  );
}
