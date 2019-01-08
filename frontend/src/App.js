import React, { Component } from 'react';
import Nav from './components/Nav';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import District from './components/District';
import {getUserState, loginUser, signupUser} from './services/authServices';
import {connect} from 'react-redux'
import * as userActions from './globalState/user/UserActions';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
    displayed_form: '',
    hasToken: localStorage.getItem('token') ? true : false,
    };
  }

  componentDidMount() {
    if (this.state.hasToken) {
      getUserState()
        .then(json => {
          console.log('getUserState', json);
          const {setUsername, setIsLoggedIn} = this.props;
          setUsername(json.username);
          setIsLoggedIn(true);
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();

    loginUser(data)
    .then(json => {
      localStorage.setItem('token', json.token);

      const {authSuccess} = this.props;
      authSuccess({
          token: json.token,
          username: json.user.username
      });

      this.setState({
        displayed_form: '',
      });
    });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    signupUser(data)
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    const { username, isLoggedIn } = this.props;

    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="BaseComponent">
        <Nav
          display_form={this.display_form}
        />
        {form}
        <h3>
          <p>Username: {username}</p>
          {isLoggedIn
            ? null
            : 'Please Log In'}
        </h3>
        {isLoggedIn ? <District /> : null}
       </div>
    );
  }
}

const mapStateToProps = state => {
  const {user} = state;

  return {
    username: user.get('username'),
    isLoggedIn: user.get('isLoggedIn'),
  }
}

export default connect(mapStateToProps,{
  authSuccess: userActions.authSuccess,
  setUsername: userActions.setUsername,
  setIsLoggedIn: userActions.setIsLoggedIn,
})(App);
