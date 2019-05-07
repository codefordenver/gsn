import React from 'react';
import { Switch, Route, Router } from 'react-router-dom';
import history from 'utils/history';
import Layout from 'components/layouts/Default';
// import Nav from 'components/Nav';
// import HomePage from 'components/HomePage';
import Login from 'pages/Login';
import SignupForm from 'pages/Register';
import Districts from 'components/Districts';
import Students from 'pages/Students';
import StudentDetail from 'pages/StudentDetail';

import PrivateRoute from './PrivateRoute';

export default function () {
  return (
      <Router history={history}>
          <Switch>
              <Route exact path="/login" component={Login} />
              <Route exact path="/register" component={SignupForm} />
              <Switch>
                  <Layout>
                      <PrivateRoute exact path="/" component={() => 'homepage...'} />
                      <PrivateRoute exact path="/districts" component={Districts} />
                      <PrivateRoute exact path="/students" component={Students} />
                      <PrivateRoute exact path="/students/:studentId" component={StudentDetail} />
                  </Layout>
              </Switch>
          </Switch>
      </Router>

  );
}
