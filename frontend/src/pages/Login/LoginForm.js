import React, {useState} from 'react';
// import PropTypes from 'prop-types';
import Layout from "../../components/layouts/SignUpLayout"

import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';
import { Button, TextField, Typography, Divider } from '@material-ui/core';

function LoginForm (props) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {loading, error, logIn} = props;
  return (
      <Layout>
        <Typography variant="h1" gutterBottom={true}>Log In</Typography>

        {error && <p>Error: {error}</p>}

        <TextField
          onChange={(e)=>setUsername(e.target.value)}
          type='text'
          error={submitted && !username}
          name='username'
          label="User Name"
          value={username}
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth={true}
        />

        <TextField
          onChange={(e)=>setPassword(e.target.value)}
          type='password'
          error={submitted && !password}
          name='password'
          label="Password"
          value={password}
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth={true}
          gutterBottom={true}
        />

        <Button
          style={{ marginTop: 16 }}
          onClick={
            ()=>{
              setSubmitted(true);
              if (username && password) logIn({username, password});
            }
          }
          disabled={loading}
          variant="raised"
          color="primary"
          fullWidth={true}>
          Log In
        </Button>

        {loading && <Typography>Loading...</Typography>}

        <Divider style={{ marginTop: 16, marginBottom: 16 }}/>

        <Typography>No account? <Link to='/register' style={{color: "cyan"}}>Register</Link></Typography>
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
)(LoginForm);
