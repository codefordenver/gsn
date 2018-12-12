import React, { Component } from 'react';
import Nav from './Nav';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import DatabaseInteractor from './DatabaseInteractor';
import {getUserState, loginUser, signupUser} from './services/authServices';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
    displayed_form: '',
    logged_in: localStorage.getItem('token') ? true : false,
    username: ''
    };
  }

  componentDidMount() {
    if (this.state.logged_in) {
      getUserState()
        .then(res => res.json())
        .then(json => {
          console.log('getUserState', json);
          this.setState({ username: json.username });
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();

    loginUser(data)
    .then(res => res.json())
    .then(json => {
      localStorage.setItem('token', json.token);
      this.setState({
        logged_in: true,
        displayed_form: '',
        username: json.user.username
      });
    });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    signupUser(data)
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: ''});
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
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
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3>
          <p>Username: {this.state.username}</p>
          {this.state.logged_in
            ? null
            : 'Please Log In'}
        </h3>
        {this.state.logged_in ? <DatabaseInteractor /> : null}
       </div>
    );
  }
}

export default App;
