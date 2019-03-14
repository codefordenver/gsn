import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

const PrivateRoute = ({ component: Component, isLoggedIn, ...rest }) => (
    <Route
      {...rest}
      render={componentProps => (
        isLoggedIn
          ? <Component {...componentProps} />
          : <Redirect to={{ pathname: '/login', state: { from: componentProps.location } }} />
      )}
    />
);

PrivateRoute.propTypes = {
  component: PropTypes.func,
  isLoggedIn: PropTypes.bool.isRequired,
};

export default PrivateRoute;
