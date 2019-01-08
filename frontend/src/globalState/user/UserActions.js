import {
  SET_AUTH_TOKEN,
  CLEAR_AUTH,
  AUTH_REQUEST,
  AUTH_SUCCESS,
  AUTH_ERROR,
} from './UserConstants';

export const setAuthToken = authToken => ({
  type: SET_AUTH_TOKEN,
  authToken
});

export const clearAuth = () => ({
  type: CLEAR_AUTH
});

export const authRequest = () => ({
  type: AUTH_REQUEST
});

export const authSuccess = currentUser => ({
  type: AUTH_SUCCESS,
  currentUser
});

export const authError = error => ({
  type: AUTH_ERROR,
  error
});
