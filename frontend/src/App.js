import React, { Component } from 'react';
import Nav from 'components/Nav';
import HomePage from 'components/HomePage';
import LoginForm from 'components/LoginForm';
import SignupForm from 'components/SignupForm';
import Districts from 'components/Districts';
import Students from 'components/Students';
import {connect} from 'react-redux';
import * as userActions from 'globalState/user/UserActions';
import {Switch, Route, Router} from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import { history } from 'utils/history';

class App extends Component {

  componentWillMount() {
    const {setUserState} = this.props;
    setUserState();
  }

  render() {
    const { username, isLoggedIn, loading } = this.props;
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
              <Route path='/testpath/:testparam' render={(props)=>{
                console.log({props});
                const {testparam} = props.match.params;
                return <p>testpath worked: {testparam}</p>;
              }} />
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
  setLoading: userActions.setLoading,
  setUserState: userActions.setUserState,
})(App);
