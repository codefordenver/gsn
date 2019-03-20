import React from 'react';
import { Switch, Route, Router } from 'react-router-dom';
import history from 'utils/history';
import Layout from 'components/layouts/Default';
// import Nav from 'components/Nav';
import HomePage from 'components/HomePage';
import Login from 'pages/Login';
import SignupForm from 'pages/Register';
import Districts from 'components/Districts';
import Students from 'components/Students';
import StudentDetail from 'components/StudentDetail';

import PrivateRoute from './PrivateRoute';
// username: user.get('username'),
// loading: user.get('loading'),


export default function () {
  return (
      <Router history={history}>
          <Switch>
              <Route exact path="/login" component={Login} />
              <Route exact path="/register" component={SignupForm} />
              <Switch>
                  <Layout>
                      <PrivateRoute exact path="/" component={HomePage} />
                      <PrivateRoute path="/districts" component={Districts} />
                      <PrivateRoute exact path="/students" component={Students} />
                      <PrivateRoute path="/students/:studentId" component={StudentDetail} />
                  </Layout>
              </Switch>
          </Switch>
      </Router>

  );
}

/* <div>
              {isLoggedIn && <Nav navItems={navItems} />} */
/*
        <h3>
            {isLoggedIn && (
            <p>
              Hello {username}
            </p>
            )}
        </h3> */
