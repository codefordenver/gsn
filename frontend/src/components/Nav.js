import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux'
import * as userActions from '../globalState/user/UserActions';

function Nav({isLoggedIn, logOut, display_form}) {

  const logged_out_nav = (
    <ul>
      <li onClick={() => display_form('login')}><span className="navitem">login</span></li>
      <li onClick={() => display_form('signup')}><span className="navitem">signup</span></li>
    </ul>
  );

  const logged_in_nav = (
    <ul>
      <li onClick={logOut}><span className="navitem">logout</span></li>
    </ul>
  );

  return <div>{isLoggedIn ? logged_in_nav : logged_out_nav}</div>;
}

const mapStateToProps = state => {
  const {user} = state;
  return {
    isLoggedIn: user.get('isLoggedIn'),
  }
}

export default connect(mapStateToProps, {logOut: userActions.logOut})(Nav);

Nav.proptypes = {
  display_form: PropTypes.func.isRequired,
}
