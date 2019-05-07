import { request } from './request';

export const getStudents = () => request({
  url: 'gsndb/student/',
});

export const getStudentDetail = id => request({
  url: `gsndb/student/${id}/`,
});
