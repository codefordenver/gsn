import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

const mapStateToProps = state => ({
  isLoggedIn: state.user.get('isLoggedIn'),
});

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

export default connect(
  mapStateToProps,
  null,
  null,
  { pure: false },
)(PrivateRoute);
