import React, { useState } from 'react';
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
    route: 'my-students',
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
  const { classes: { icon } } = props;
  const renderLink = itemProps => <Link to={props.item.route} {...itemProps} />;
  const {
    index, item, selected, setIndex,
  } = props;

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
const styles = theme => ({
  icon: {
    color: theme.palette.primary.main,
  },
});
const LiLink = withStyles(styles)(BaseLink);

function Navigation(props) {
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


export default Navigation;
