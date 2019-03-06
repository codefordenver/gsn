import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom';
import {getStudentDetail} from 'services/studentServices.js';

export default function StudentDetail(props) {

  const [studentDetail, setStudentDetail] = useState({});
  const [loading, setLoading] = useState(true);

  const {studentId} = props.match.params;

  useEffect(() => {
    console.log('useEffect ran in StudentDetail', studentId);
    getStudentDetail(studentId).then(studentDetail=> {
      setStudentDetail(studentDetail);
      setLoading(false);
    });
  }, []);

  if (loading) return (
    <div>
      <h1>Student Detail</h1>
      <h2>Loading...</h2>
    </div>
  )

  const {
    // studentId,
    name,
    gender,
    school,
    schoolId,
    birthdate,
    grade,
    stateId,
    studentYear,
    studentTerm,
  } = studentDetail;

  return (
    <div>
      <h1>{name}</h1>
      <p><strong>Gender:</strong> {gender}</p>
      <p><strong>Birthdate:</strong> {birthdate}</p>
      <p><strong>Grade:</strong> {grade}</p>
      <p><strong>Year:</strong> {studentYear}</p>
      <p><strong>Term: </strong> {studentTerm}</p>
      <p><strong>State Id:</strong> {stateId}</p>
      <p><strong>School:</strong> <Link to={`/school/${schoolId}`}>{school}</Link></p>
    </div>
  )
}
