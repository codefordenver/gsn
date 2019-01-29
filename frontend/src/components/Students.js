import React, { Component } from 'react';
import {Link} from 'react-router-dom';
import {getStudents} from 'services/studentServices.js';

class Students extends Component {
  constructor() {
    super();
    this.state = {
      students: [],
    }
  }



  componentWillMount() {
    getStudents().then(students=> {
      this.setState({students, loading: false});
    });
  }

  render() {
    const {students} = this.state;
    return (
      <div>
        <h1>Students</h1>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>School</th>
              <th>Birthdate</th>
            </tr>
          </thead>
          <tbody>
          {students.map(student=>{
            const {studentId, name, school, schoolId, birthdate} = student;
            return (<tr key={studentId}>
              <td><Link to={`student/${studentId}`}>{name}</Link></td>
              <td><Link to={`school/${schoolId}`}>{school}</Link></td>
              <td>{birthdate}</td>
            </tr>)
          })}
          </tbody>
        </table>
      </div>
    )
  }
}

export default Students;
