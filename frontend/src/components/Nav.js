import React from 'react';
import PropTypes from 'prop-types';
import NavItem, { NavItemPropTypes } from 'components/NavItem';

export default function Nav({ navItems }) {
  return (
      <div>
          <ul>
              {navItems.map(navItem => <NavItem {...navItem} />)}
          </ul>
      </div>
  );
}

Nav.propTypes = {
  navItems: PropTypes.arrayOf(PropTypes.shape(NavItemPropTypes)),
};
