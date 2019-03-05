import {request} from './request';

export const getUserState = (token) => {
  return token
  ? request({
    url: 'user_app/current_user/',
    headers: {
      Authorization: `JWT ${token}`
    }
  })
  : Promise.reject(new Error('no token passed to getUserState service'))
};

export const loginUser = ({username, password}) => {
  return request({
  url: 'token-auth/',
  method: 'POST',
  body: JSON.stringify({username, password}),
})};

export const signupUser = ({username, password}) => request({
  url: 'user_app/users/',
  method: 'POST',
  body: JSON.stringify({username, password}),
});
