import React, { useState } from 'react';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import * as userActions from 'state/UserActions';
import {
  Button, InputBase, Typography, Divider, withStyles,
} from '@material-ui/core';
import Layout from '../../components/layouts/SignUpLayout';
import styles from '../../components/sharedStyles/LoginStyles';

function LoginForm(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {
    classes: {
      divider, header, input, link, text,
    },
    loading,
    logIn,
    error,
  } = props;

  const completeLogin = () => {
    setSubmitted(true);
    if (username && password) logIn({ username, password });
  };

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
          {error && (
          <p>
Error:
              {error}
          </p>
          )}

          <InputBase
            className={input}
            onChange={e => setUsername(e.target.value)}
            type="text"
            error={submitted && !username}
            name="username"
            placeholder="User Name"
            value={username}
            disabled={loading}
            onKeyPress={e => (e.key === 'Enter' ? completeLogin() : () => {})}
            fullWidth
          />

          <InputBase
            className={input}
            onChange={e => setPassword(e.target.value)}
            type="password"
            error={submitted && !password}
            name="password"
            placeholder="Password"
            value={password}
            disabled={loading}
            onKeyPress={e => (e.key === 'Enter' ? completeLogin() : () => {})}
            fullWidth
          />

          <Button
            onClick={completeLogin}
            disabled={loading}
            variant="contained"
            color="secondary"
            fullWidth
          >
          Log In
          </Button>

          {loading && <Typography>Loading...</Typography>}

          <Divider className={divider} />

          <Typography className={text}>
          No account?&nbsp;
              <Link to="/register" className={link}>
            Register
              </Link>
          </Typography>
      </Layout>
  );
}
const mapStateToProps = ({ user }) => ({
  loading: user.get('loading'),
  error: user.get('error'),
});

/* eslint-disable no-unexpected-multiline */
LoginForm.propTypes = {
  loading: PropTypes.bool,
  logIn: PropTypes.func,
  error: PropTypes.objectOf(PropTypes.string),
  classes: PropTypes.shape({
    divider: PropTypes.string,
    header: PropTypes.string,
    input: PropTypes.string,
    link: PropTypes.string,
    text: PropTypes.string,
  }),
};

export default connect(
  mapStateToProps,
  { logIn: userActions.logIn },
)(
  withStyles(styles)(LoginForm),
);
