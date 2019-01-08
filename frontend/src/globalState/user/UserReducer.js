import {fromJS} from 'immutable';
import {
  SET_AUTH_TOKEN,
  CLEAR_AUTH,
  AUTH_REQUEST,
  AUTH_SUCCESS,
  AUTH_ERROR,
} from './UserConstants';

const initialState = fromJS({
  authToken: null,
  isLoggedIn: false,
  username: null,
  loading: false,
  error: null
});

export default function reducer(state = initialState, action) {

  const {type, payload} = action;

  switch (type) {
    case SET_AUTH_TOKEN:
      return state.set('authToken', payload);
    case CLEAR_AUTH:
      return state.set('authToken', null)
                  .set('userName', null)
                  .set('isLoggedIn', false);
    case AUTH_REQUEST:
      return state.set('loading', true)
                  .set('error', null);
    case AUTH_SUCCESS:
      return state.set('loading', false)
                  .set('isLoggedIn', true)
                  .set('username', payload.username)
                  .set('authToken', payload.authToken);
    case AUTH_ERROR:
      return state.set('loading', false)
                  .set('error', payload);
    default: return state;

  }
  
}
