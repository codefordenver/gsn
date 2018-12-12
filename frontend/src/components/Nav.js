import React from 'react';
import PropTypes from 'prop-types';

function Nav(props) {

  const logged_out_nav = (
    <ul>
      <li onClick={() => props.display_form('login')}><span className="navitem">login</span></li>
      <li onClick={() => props.display_form('signup')}><span className="navitem">signup</span></li>
    </ul>
  );

  const logged_in_nav = (
    <ul>
      <li onClick={props.handle_logout}><span className="navitem">logout</span></li>
    </ul>
  );

  return <div>{props.logged_in ? logged_in_nav : logged_out_nav}</div>;
}

export default Nav;

Nav.proptypes = {
  logged_in: PropTypes.bool.isRequired,
  display_form: PropTypes.func.isRequired,
}
