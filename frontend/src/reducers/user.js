const initialState = {
  authToken: null,
  isLoggedIn: false,
  userName: null,
  laoding: false,
  error: null
};

export default function reducer(state = initialState, action) {
  if (action.type === SET_AUTH_TOKEN) {
    return Object.assign({}, state, {
      authToken: action.authToken
    });
  } else if (action.type === CLEAR_AUTH) {
    return Object.assign({}, state, {
      authToken: null,
      userName: null,
      isLoggedIn: false
    });
  } else if (action.type === AUTH_REQUEST) {
    return Object.assign({}, state, {
      loading: true,
      error: null
    });
  } else if (action.type === AUTH_SUCCESS) {
    return Object.assign({}, state, {
      loading: false,
      // TODO add in userName
      // TODO add in authToken
      isLoggedIn: true
    });
  } else if (action.type === AUTH_ERROR) {
    return Object.assign({}, state, {
      loading: false,
      error: action.error
    });
  }
  return state;
}
