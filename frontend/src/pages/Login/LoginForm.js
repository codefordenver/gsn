import React, {useState} from 'react';
// import PropTypes from 'prop-types';
import Layout from "../../components/layouts/SignUpLayout"

import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';
import { Button, InputBase, Typography, Divider, withStyles } from '@material-ui/core';
import styles from "../../components/sharedStyles/LoginStyles"

function LoginForm (props) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {
    classes: { divider, header, input, link, text },
    loading,
    logIn,
    error,
    } = props;

  return (
      <Layout>
        <Typography
        className={header}
        variant="h1"
        gutterBottom
        >
          Log In
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
              if (username && password) logIn({username, password});
            }
          }
          disabled={loading}
          variant="contained"
          color="secondary"
          fullWidth
          >
          Log In
        </Button>

        {loading && <Typography>Loading...</Typography>}

        <Divider className={divider}/>

        <Typography className={text}>
          No account?&nbsp;
          <Link to='/register' className={link}>
            Register
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
  { logIn: userActions.logIn }
)(
  withStyles(styles)
  (LoginForm)
);
