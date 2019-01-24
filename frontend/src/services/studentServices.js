export const getStudents = () => {
  return fetch('/mockdata/students.json')
  .then(result=>result.json())
};
