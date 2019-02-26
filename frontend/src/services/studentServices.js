export const getStudents = () => {
  return fetch('/mockdata/students.json')
  .then(result=>result.json());
};

export const getStudentDetail = () => {
  return fetch('/mockdata/studentDetail.json')
  .then(result=>result.json());
}
