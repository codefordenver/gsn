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

function App (props) {
  const {setUserState} = props;

  useEffect(() => {
    console.log('useEffect ran in App.js');
    setUserState();
  }, []);

  const { username, isLoggedIn, loading } = props;
  if (loading) return <h1>Loading...</h1>

  else return (
    <Router history={history}>
      <div className="BaseComponent">
        <Nav />

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

const mapStateToProps = state => {
  const {user} = state;

  return {
    username: user.get('username'),
    isLoggedIn: user.get('isLoggedIn'),
    loading: user.get('loading'),
  }
}

export default connect(mapStateToProps,{
  setLoading: userActions.setLoading,
  setUserState: userActions.setUserState,
})(App);
