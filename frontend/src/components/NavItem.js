import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

export default function NavItem({ path, action, text }) {
  return (
      <li className="navListItem">
          {path && !action && <Link to={path} className="navitem">{text}</Link>}
          {action && <span className="navitem" onClick={action}>{text}</span>}
      </li>
  );
}

const pathActionPropTest = (...args) => {
  const [props, propName, componentName] = args;
  const { path, action } = props;
  if (!path && !action) {
    return new Error(`${propName}: One of 'path' or 'action' is required by '${componentName}' component.`);
  } if (path && !action) {
    return PropTypes.string(...args);
  } if (action) {
    return PropTypes.func(...args);
  }
};

export const NavItemPropTypes = {
  path: pathActionPropTest,
  action: pathActionPropTest,
  text: PropTypes.string.isRequired,
};

NavItem.propTypes = NavItemPropTypes;
