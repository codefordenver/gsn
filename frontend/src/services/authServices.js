import {request} from './request';

export const getUserState = () => request({
  url: 'user_app/current_user/',
  headers: {
    Authorization: `JWT ${localStorage.getItem('token')}`
  }
});

export const loginUser = (data) => {
  return request({
  url: 'token-auth/',
  method: 'POST',
  body: JSON.stringify(data),
})};

export const signupUser = (data) => request({
  url: 'user_app/users/',
  method: 'POST',
  body: JSON.stringify(data),
});
