import React from 'react';
// import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'globalState/user/UserActions';

class LoginForm extends React.Component {
  state = {user: {
    username: '',
    password: '',
    submitted: false,
  }};

  handleChange = (event) => {
      event.preventDefault();
      const {name, value} = event.target;
      this.setState({user: {...this.state.user, [name]: value}});
  }

  render(){
    const { user: {username, password}, submitted } = this.state;
    const {loading, logIn} = this.props;
    return (
        <div>
          <h1>Log In</h1>
          <label htmlFor="username">Username</label>

          <input onChange={this.handleChange}
            type='text' className={`form-control username${submitted && !username ? ' is-invalid' : ''}`}
            name='username' value={username}
            disabled={loading} />

          <label htmlFor="password">Password</label>

          <input onChange={this.handleChange}
            type='password'
            className={`form-control password${submitted && !password ? ' is-invalid' : ''}`}
            name='password'
            value={password}
            disabled={loading} />

          <input type="button" onClick={()=>logIn({username, password})} disabled={loading} value="Log In" />
          {loading && <p>Loading...</p>}

          <p>No account? <Link to='/register'>Register</Link></p>
        </div>
    );
  }
}

export default connect(({user})=>({loading: user.get('loading')}), {logIn:userActions.logIn})(LoginForm);
