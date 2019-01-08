export const SET_AUTH_TOKEN = "SET_AUTH_TOKEN";
export const setAuthToken = authToken => ({
  type: SET_AUTH_TOKEN,
  authToken
});

export const CLEAR_AUTH = "CLEAR_AUTH";
export const clearAuth = () => ({
  type: CLEAR_AUTH
});

export const AUTH_REQUEST = "AUTH_REQUEST";
export const authRequest = () => ({
  type: AUTH_REQUEST
});

export const AUTH_SUCCESS = "AUTH_SUCCESS";
export const authSuccess = currentUser => ({
  type: AUTH_SUCCESS,
  currentUser
});

export const AUTH_ERROR = "AUTH_ERROR";
export const authError = error => ({
  type: AUTH_ERROR,
  error
});
