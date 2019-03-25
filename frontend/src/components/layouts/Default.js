import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import IconButton from '@material-ui/core/IconButton';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { Menu, MenuItem } from '@material-ui/core';
import { connect } from 'react-redux';
import * as userActions from 'state/UserActions';
import { UserSolidCircle } from '../Icons';

// import Logo from '../../../public/img/gsn_logo_mark.png';


import LeftNav from '../LeftNav';
import Breadcrumbs from '../Breadcrumbs';

function ClippedDrawer(props) {
  const { classes, logOut, user_name } = props;
  // const [open, toggleOpen] = useState(false);
  const [anchorEl, setAnchor] = useState(null);
  const open = Boolean(anchorEl);

  const handleMenu = event => setAnchor(event.currentTarget);
  const handleClose = event => setAnchor(null);

  return (
      <div className={classes.root}>
          <AppBar elevation={0} position="fixed" className={classes.appBar}>
              <Toolbar>
                  <IconButton
                    aria-owns={open ? 'menu-appbar' : undefined}
                    aria-haspopup="true"
                    onClick={handleMenu}
                    color="primary"
                  >
                      <UserSolidCircle />
                  </IconButton>
                  <Menu
                    id="menu-appbar"
                    anchorEl={anchorEl}
                    anchorOrigin={{
                      vertical: 'top',
                      horizontal: 'left',
                    }}
                    transformOrigin={{
                      vertical: 'top',
                      horizontal: 'left',
                    }}
                    open={open}
                    onClose={handleClose}
                  >
                      <MenuItem
                        onClick={logOut}
                      >Logout
                      </MenuItem>
                  </Menu>
                  <Typography
                    className={classes.name}
                    variant="h6"
                    noWrap
                  >
                      {user_name}
                  </Typography>
                  <div className={classes.spacer} />
                  <div>
                      {/* <img src={Logo} height="auto" width="100" /> */}
                  </div>
              </Toolbar>
          </AppBar>
          <Drawer
            className={classes.drawer}
            variant="permanent"
            classes={{
              paper: classes.drawerPaper,
            }}
          >
              <div className={classes.toolbar} />
              <div className={classes.nav}>
                  <LeftNav />
              </div>
          </Drawer>
          <main className={classes.main}>
              <div className={classes.toolbar} />
              <Breadcrumbs />
              <div className={classes.content}>
                  {props.children}
              </div>
          </main>
      </div>
  );
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
  children: PropTypes.object,
  user_name: PropTypes.string.isRequired,
};

const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    color: theme.grays.g4,
    backgroundColor: 'white',
    borderBottom: `1px solid ${theme.palette.primary.main}`,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
    borderRight: `1px solid ${theme.palette.primary.main}`,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    backgroundColor: theme.grays.g2,
    minHeight: '85.5vh',
  },
  main: {
    backgroundColor: 'white',
    width: '100%',
  },
  name: { paddingLeft: theme.spacing.unit * 2 },
  nav: {
    marginTop: theme.spacing.unit * 3 + 5, // so close...
  },
  // TODO This is kind of hacky but stops us from having to do nested flexbox-es on the toolbar for now
  spacer: { width: '65%' },
  toolbar: theme.mixins.toolbar,
});

export default connect(
  null,
  { logOut: userActions.logOut },
)(withStyles(styles)(ClippedDrawer));
