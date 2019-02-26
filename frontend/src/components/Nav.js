import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux'
import {Link} from 'react-router-dom';
import * as userActions from 'state/UserActions';

function Nav({isLoggedIn, logOut, display_form}) {

  const $loggedOutNav = (
    <ul>
      <li className="navListItem">
        <Link to="/login" className="navitem">Log In</Link>
      </li>
      <li className="navListItem">
        <Link to="/register" className="navitem">Register</Link>
      </li>
    </ul>
  );

  const $loggedInNav = (
    <ul>
      <li className="navListItem">
        <Link to="/" className="navitem">Home</Link>
      </li>
      <li className="navListItem">
        <Link to="/students" className="navitem">All Students</Link>
      </li>
      <li className="navListItem">
        <Link to="/districts" className="navitem">All Districts</Link>
      </li>
      <li className="navListItem">
        <span className="navitem" onClick={logOut}>Log Out</span>
      </li>
    </ul>
  );

  return <div>{isLoggedIn ? $loggedInNav : $loggedOutNav}</div>;
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
