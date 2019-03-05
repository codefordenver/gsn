import React, {useState} from 'react';
// import PropTypes from 'prop-types';

import Layout from "components/layouts/SignUpLayout"

import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import * as userActions from 'state/UserActions';

import { Button, TextField, Typography, Divider } from '@material-ui/core';


function SignupForm(props) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const {loading, error, register} = props;
  return (
    <Layout>
      <Typography variant="h1" gutterBottom>Sign Up</Typography>

        {error && <p>Error: {error}</p>}

        <TextField onChange={(e)=>setUsername(e.target.value)}
          type='text'
          error={submitted && !username}
          name='username'
          value={username}
          label="User Name"
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth
        />

        <TextField onChange={(e)=>setPassword(e.target.value)}
          type='password'
          error={submitted && !password}
          name='password'
          label="Password"
          value={password}
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth
        />

        <Button
          style={{ marginTop: 16 }}
          onClick={
            ()=>{
              setSubmitted(true);
              if (username && password) register({username, password});
            }
          }
          disabled={loading}
          value="Register"
          variant="raised"
          color="primary"
          fullWidth
          gutterBottom
        >
          Register
        </Button>

        {loading && <Typography>Loading...</Typography>}

        <Divider style={{ marginTop: 16, marginBottom: 16 }}/>
        
        <Typography>Already Have an account? <Link to='/login' style={{color: "cyan"}}>Log In</Link></Typography>
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
)(SignupForm);
