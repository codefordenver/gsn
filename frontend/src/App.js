import React, { useEffect } from 'react';
import Nav from 'components/Nav';
import HomePage from 'components/HomePage';
import LoginForm from 'components/LoginForm';
import SignupForm from 'components/SignupForm';
import Districts from 'components/Districts';
import Students from 'components/Students';
import StudentDetail from 'components/StudentDetail';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';
import {Switch, Route, Router} from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import { history } from 'utils/history';

const loggedOutNav = [
  {path: '/login', text:'Log In'},
  {path: '/register', text: 'Register'},
];

const loggedInNav = [
  {path: '/', text:'Home'},
  {path: '/students', text: 'All Students'},
  {path: '/districts', text:'All Districts'},
];

function App (props) {
  const { setUserState } = props;

  useEffect(() => {
    console.log('useEffect ran in App.js');
    setUserState();
  }, []);

  const { username, isLoggedIn, loading, logOut } = props;
  if (loading) return <h1>Loading...</h1>;

  else {
    const logOutItem = {action: logOut, text: 'Log Out'};
    const navItems = isLoggedIn ? [...loggedInNav, logOutItem] : loggedOutNav;

    return (
      <Router history={history}>
        <div className="BaseComponent">
          <Nav navItems={navItems} />

          <h3>
            {isLoggedIn && <p>Hello {username}</p>}
            <Switch>
              <PrivateRoute exact path='/' isLoggedIn={isLoggedIn} component={HomePage} />
              <Route path='/login' component={LoginForm} />
              <Route path='/register' component={SignupForm} />
              <PrivateRoute path='/districts' isLoggedIn={isLoggedIn} component={Districts} />
              <PrivateRoute path='/students' isLoggedIn={isLoggedIn} component={Students} />
              <PrivateRoute path='/student/:studentId' isLoggedIn={isLoggedIn} component={StudentDetail} />
            </Switch>
          </h3>
         </div>
       </Router>
    );
  }
}

const mapStateToProps = state => {
  const {user} = state;

  return {
    username: user.get('username'),
    isLoggedIn: user.get('isLoggedIn'),
    loading: user.get('loading'),
  }
}

export default connect(mapStateToProps,{
  setUserState: userActions.setUserState,
  logOut: userActions.logOut,
})(App);
