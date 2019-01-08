import {
  SET_AUTH_TOKEN,
  CLEAR_AUTH,
  AUTH_REQUEST,
  AUTH_SUCCESS,
  AUTH_ERROR,
} from './UserConstants';

export const setAuthToken = authToken => ({
  type: SET_AUTH_TOKEN,
  payload: authToken
});

export const clearAuth = () => ({
  type: CLEAR_AUTH
});

export const authRequest = () => ({
  type: AUTH_REQUEST
});

export const authSuccess = ({username, token}) => ({
  type: AUTH_SUCCESS,
  payload: {username, token}
});

export const authError = error => ({
  type: AUTH_ERROR,
  payload: error
});
