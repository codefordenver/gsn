export const getStudents = () => fetch('/mockdata/students.json')
  .then(result => result.json());

export const getStudentDetail = () => fetch('/mockdata/studentDetail.json')
  .then(result => result.json());
