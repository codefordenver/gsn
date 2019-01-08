import {request} from './request';

export const getDistricts = () => request({
  url: 'gsndb/district/',
});
