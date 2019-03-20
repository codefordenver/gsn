import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import * as userActions from 'state/UserActions';

import CssBaseline from '@material-ui/core/CssBaseline';
import { MuiThemeProvider } from '@material-ui/core';
import theme from './utils/theme';
import Routes from './components/Routes';

const loggedInNav = [
  { key: 'navitem1', path: '/', text: 'Home' },
  { key: 'navitem2', path: '/students', text: 'All Students' },
  { key: 'navitem3', path: '/districts', text: 'All Districts' },
];

function App(props) {
  const { setUserState } = props;

  useEffect(() => {
    setUserState();
  }, []);

  const {
    username, isLoggedIn, loading, logOut,
  } = props;
  if (loading) return <h1>Loading...</h1>;


  const logOutItem = { key: 'navitem10', action: logOut, text: 'Log Out' };
  const navItems = [...loggedInNav, logOutItem];

  return (
      <MuiThemeProvider theme={theme}>
          <CssBaseline />
          <Routes />
      </MuiThemeProvider>

  );
}

const mapStateToProps = (state) => {
  const { user } = state;

  return {
    username: user.get('username'),
    isLoggedIn: user.get('isLoggedIn'),
    loading: user.get('loading'),
  };
};

export default connect(mapStateToProps, {
  setUserState: userActions.setUserState,
  logOut: userActions.logOut,
})(App);
