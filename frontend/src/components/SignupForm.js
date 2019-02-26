import React, {useState} from 'react';
// import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';

function SignupForm(props) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {loading, register} = props;
  return (
    <div>
      <h1>Sign Up</h1>
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

        <input type="button" onClick={()=>register({username, password})} disabled={loading} value="Register" />
        {loading && <p>Loading...</p>}

        <p>Already Have an account? <Link to='/login'>Log In</Link></p>
    </div>
  );
}
const mapStateToProps = ({user})=>({loading: user.get('loading')})
export default connect(
  mapStateToProps,
  {register:userActions.register})(SignupForm);
