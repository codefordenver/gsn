import React, {useState} from 'react';
// import PropTypes from 'prop-types';

import Layout from "components/layouts/SignUpLayout"

import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';

import { Button, InputBase, Typography, Divider, withStyles } from '@material-ui/core';
import styles from "../../components/sharedStyles/LoginStyles";

function SignupForm(props) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {
    classes: { divider, header, input, link, text },
    loading,
    error,
    register
  } = props;
  return (
    <Layout>
        <Typography
          className={header}
          variant="h1"
          gutterBottom
        >
          Register
        </Typography>

        {/* TODO Add Error Field */}
        {error && <p>Error: {error}</p>}

        <InputBase
          className={input}
          onChange={(e)=>setUsername(e.target.value)}
          type='text'
          error={submitted && !username}
          name='username'
          placeholder="User Name"
          value={username}
          disabled={loading}
          fullWidth
        />

        <InputBase
          className={input}
          onChange={(e)=>setPassword(e.target.value)}
          type='password'
          error={submitted && !password}
          name='password'
          placeholder="Password"
          value={password}
          disabled={loading}
          fullWidth
        />

        <Button
          onClick={
            ()=>{
              setSubmitted(true);
              if (username && password) register({username, password});
            }
          }
          disabled={loading}
          variant="contained"
          color="secondary"
          fullWidth
        >
          Register
        </Button>

        {loading && <Typography>Loading...</Typography>}

        <Divider className={divider}/>
        
        <Typography className={text}>
          Already Have an account? &nbsp;
          <Link to='/login' className={link}>
            Log In
          </Link>
        </Typography>
    </Layout>
  );
}
const mapStateToProps = ({user})=>({
  loading: user.get('loading'),
  error: user.get('error'),
});

export default connect(
  mapStateToProps,
  { register: userActions.register }
)(
  withStyles(styles)
  (SignupForm)
);
