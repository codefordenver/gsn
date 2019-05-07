import React, { useState } from 'react';
import PropTypes from 'prop-types';
import {
  List, ListItem, ListItemIcon, ListItemText, withStyles,
} from '@material-ui/core';

import { Link } from 'react-router-dom';
import {
  Radar, UserGroup, ViewShow, Wrench,
} from './Icons';


const navItems = [
  {
    name: 'My Students',
    icon: <UserGroup />,
    route: 'students',
  },
  {
    name: 'Visualize',
    icon: <ViewShow />,
    route: 'visualize',
  },
  {
    name: 'Analyze Data',
    icon: <Radar />,
    route: 'analyze-data',
  },
  {
    name: 'Manage Data',
    icon: <Wrench />,
    route: 'manage-data',
  },
];

function BaseLink(props) {
  const {
    classes: { icon }, index, item, selected, setIndex,
  } = props;
  const renderLink = itemProps => <Link to={`/${item.route}`} {...itemProps} />;

  return (
      <ListItem
        button
        selected={selected}
        onClick={() => setIndex(index)}
        component={renderLink}
      >
          <ListItemIcon className={(selected ? icon : '')}>{item.icon}</ListItemIcon>
          <ListItemText primary={item.name} />
      </ListItem>
  );
}

BaseLink.propTypes = {
  classes: PropTypes.object,
  index: PropTypes.number,
  item: PropTypes.object,
  selected: PropTypes.bool,
  setIndex: PropTypes.func,
};

const styles = theme => ({
  icon: {
    color: theme.palette.primary.main,
  },
});
const LiLink = withStyles(styles)(BaseLink);

export default function Navigation() {
  const [selectedIndex, updateSelected] = useState(0);
  const setIndex = index => updateSelected(index);

  return (
      <List>
          {navItems.map((item, index) => (
              <LiLink
                index={index}
                item={item}
                key={item.name}
                selected={(index === selectedIndex)}
                setIndex={setIndex}
              />
          ))}
      </List>
  );
}
