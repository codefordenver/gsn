import {
  SET_TOKEN,
  SET_USERNAME,
  SET_LOADING,
  SET_IS_LOGGED_IN,
  SET_ERROR,
  CLEAR_ERROR,
} from './UserConstants';

import {createAction} from 'utils/ActionUtils';

export const setToken = createAction(SET_TOKEN);
export const setUsername = createAction(SET_USERNAME);
export const setLoading = createAction(SET_LOADING);
export const setIsLoggedIn = createAction(SET_IS_LOGGED_IN);
export const setError = createAction(SET_ERROR);
export const clearError = createAction(CLEAR_ERROR);

export const logOut = () => (dispatch) => {
  localStorage.removeItem('token');
  dispatch(setIsLoggedIn(false));
};

export const authRequest = () => (dispatch) => {
  dispatch(setLoading(true));
  dispatch(clearError());
}

export const authSuccess = ({username, token}) => (dispatch) => {
  dispatch(setLoading(false));
  dispatch(setIsLoggedIn(true));
  dispatch(setUsername(username));
  dispatch(setToken(token));
  localStorage.setItem('token', token);
}

export const authError = error => (dispatch) => {
  dispatch(setLoading(false));
  dispatch(setError(error));
}
