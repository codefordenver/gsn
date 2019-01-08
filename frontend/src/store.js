import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import user from './globalState/user/UserReducer';

const store = createStore(
  combineReducers({
    user
  }),
  applyMiddleware(thunk)
);

// Hydrate the authToken from localStorage if it exist

export default store;
