import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import IconButton from '@material-ui/core/IconButton';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { UserSolidCircle } from "../../components/Icons"

import Logo from "../../../public/img/gsn_logo_mark.png";

import LeftNav from "../LeftNav"
import Breadcrumbs from "../Breadcrumbs"

function ClippedDrawer(props) {
  const { classes, user_name } = props;

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar elevation={0} position="fixed" className={classes.appBar}>
        <Toolbar>
          <IconButton color="primary">
            <UserSolidCircle />
          </IconButton>
          <Typography
            className={classes.name}
            variant="h6"
            noWrap>
            {user_name}
          </Typography>
          <div className={classes.spacer} />
          <div>
            <img src={Logo} height="auto" width="100"/>
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
          <Typography paragraph>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
            ut labore et dolore magna aliqua. Rhoncus dolor purus non enim praesent elementum
            facilisis leo vel. Risus at ultrices mi tempus imperdiet. Semper risus in hendrerit
            gravida rutrum quisque non tellus. Convallis convallis tellus id interdum velit laoreet id
            donec ultrices. Odio morbi quis commodo odio aenean sed adipiscing. Amet nisl suscipit
            adipiscing bibendum est ultricies integer quis. Cursus euismod quis viverra nibh cras.
            Metus vulputate eu scelerisque felis imperdiet proin fermentum leo. Mauris commodo quis
            imperdiet massa tincidunt. Cras tincidunt lobortis feugiat vivamus at augue. At augue eget
            arcu dictum varius duis at consectetur lorem. Velit sed ullamcorper morbi tincidunt. Lorem
            donec massa sapien faucibus et molestie ac.
          </Typography>
          <Typography paragraph>
            Consequat mauris nunc congue nisi vitae suscipit. Fringilla est ullamcorper eget nulla
            facilisi etiam dignissim diam. Pulvinar elementum integer enim neque volutpat ac
            tincidunt. Ornare suspendisse sed nisi lacus sed viverra tellus. Purus sit amet volutpat
            consequat mauris. Elementum eu facilisis sed odio morbi. Euismod lacinia at quis risus sed
            vulputate odio. Morbi tincidunt ornare massa eget egestas purus viverra accumsan in. In
            hendrerit gravida rutrum quisque non tellus orci ac. Pellentesque nec nam aliquam sem et
            tortor. Habitant morbi tristique senectus et. Adipiscing elit duis tristique sollicitudin
            nibh sit. Ornare aenean euismod elementum nisi quis eleifend. Commodo viverra maecenas
            accumsan lacus vel facilisis. Nulla posuere sollicitudin aliquam ultrices sagittis orci a.
          </Typography>
        </div>
      </main>
    </div>
  );
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
  user_name: PropTypes.string.isRequired,
};

ClippedDrawer.defaultProps = {
  user_name: "Error: No user name found"
}

const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    color: theme.grays.g4,
    backgroundColor: "white",
    borderBottom: `1px solid ${theme.palette.primary.main}`,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    backgroundColor: theme.grays.g2,
  },
  main: {
    borderLeft: `1px solid ${theme.palette.primary.main}`,
    backgroundColor: 'white',
    },
  name: { paddingLeft: theme.spacing.unit * 2 },
  nav: {
    marginTop: theme.spacing.unit * 3 + 5 // so close...
  },
  // TODO This is kind of hacky but stops us from having to do nested flexbox-es on the toolbar for now
  spacer: { width:"65%" },
  toolbar: theme.mixins.toolbar,
});

export default withStyles(styles)(ClippedDrawer);