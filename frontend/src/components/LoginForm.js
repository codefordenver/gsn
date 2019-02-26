import React, {useState} from 'react';
// import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';

function LoginForm (props) {
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {loading, logIn} = props;
  return (
      <div>
        <h1>Log In</h1>
        <label htmlFor="username">Username</label>

        <input onChange={(e)=>setUsername(e.target.value)}
          type='text' className={`form-control username${submitted && !username ? ' is-invalid' : ''}`}
          name='username' value={username}
          disabled={loading} />

        <label htmlFor="password">Password</label>

        <input onChange={(e)=>setPassword(e.target.value)}
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

export default connect(({user})=>({loading: user.get('loading')}), {logIn:userActions.logIn})(LoginForm);
