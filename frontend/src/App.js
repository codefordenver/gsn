import React, { useEffect } from 'react';
import Nav from 'components/Nav';
import HomePage from 'components/HomePage';
import Login from 'pages/Login';
import SignupForm from 'pages/Register';
import Districts from 'components/Districts';
import Students from 'components/Students';
import StudentDetail from 'components/StudentDetail';
import { connect } from 'react-redux';
import * as userActions from 'state/UserActions';
import { Switch, Route, Router } from 'react-router-dom';
import history from 'utils/history';

import CssBaseline from '@material-ui/core/CssBaseline';
import { MuiThemeProvider } from '@material-ui/core';
import PrivateRoute from './PrivateRoute';
import theme from './utils/theme';

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
          <Router history={history}>
              <div>
                  <CssBaseline />
                  {isLoggedIn && <Nav navItems={navItems} />}

                  <h3>
                      {isLoggedIn && (
                      <p>
                        Hello {username}
                      </p>
                      )}
                  </h3>
                  <Switch>
                      <PrivateRoute exact path="/" isLoggedIn={isLoggedIn} component={HomePage} />
                      <Route path="/login" component={Login} />
                      <Route path="/register" component={SignupForm} />
                      <PrivateRoute path="/districts" isLoggedIn={isLoggedIn} component={Districts} />
                      <PrivateRoute path="/students" isLoggedIn={isLoggedIn} component={Students} />
                      <PrivateRoute path="/student/:studentId" isLoggedIn={isLoggedIn} component={StudentDetail} />
                  </Switch>
              </div>
          </Router>
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
