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

  const {loading, logIn } = props;
  return (
      <Layout>
        <Typography variant="h1" gutterBottom>Log In</Typography>

        <TextField
          onChange={(e)=>setUsername(e.target.value)}
          type='text' className={`form-control username${submitted && !username ? ' is-invalid' : ''}`}
          name='username'
          label="User Name"
          value={username}  
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth
          />

        <TextField onChange={(e)=>setPassword(e.target.value)}
          type='password'
          className={`form-control password${submitted && !password ? ' is-invalid' : ''}`}
          name='password'
          label="Password"
          value={password}
          disabled={loading}
          margin="normal"
          variant="outlined"
          fullWidth
          gutterBottom
          />

        <Button style={{ marginTop: 16 }} onClick={()=>logIn({username, password})} disabled={loading} variant="raised" color="primary" fullWidth gutterBottom>Log In</Button>

        {loading && <Typography>Loading...</Typography>}

        <Divider style={{ marginTop: 16, marginBottom: 16 }}/>

        <Typography>No account? <Link to='/register' style={{color: "cyan"}}>Register</Link></Typography>
      </Layout>
  );
}

export default connect(({user})=>({loading: user.get('loading')}), {logIn:userActions.logIn})(((LoginForm)));
