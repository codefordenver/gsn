import React from 'react';
import NavItem from 'components/NavItem';

export default function Nav({navItems}) {
  return (
    <div>
      <ul>
        {navItems.map((navItem, index)=><NavItem key={navItem+index} {...navItem} />)}
      </ul>
    </div>
  )
}
