import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Typography, withStyles,
} from '@material-ui/core';
import PropTypes from 'prop-types';

import { getStudentDetail } from 'services/studentServices';

const DetailBase = ({ k, val, classes: { lDiv, rDiv, root } }) => (
    <div color="primary" className={root}>
        <Typography color="primary" className={lDiv}>{k}:</Typography>
        <Typography color="primary" className={rDiv}>{val}</Typography>
    </div>
);

DetailBase.propTypes = {
  k: PropTypes.string,
  val: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  classes: PropTypes.object,
};

const DLinkBase = ({
  k, val, link, classes: { lDiv, rDiv, root },
}) => (
    <div className={root}>
        <Typography color="primary" className={lDiv}>{k}:</Typography>
        <Typography color="primary" className={rDiv}><Link to={link}>{val}</Link></Typography>
    </div>
);

DLinkBase.propTypes = {
  k: PropTypes.string,
  val: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  link: PropTypes.string,
  classes: PropTypes.object,
};

const dStyles = theme => ({
  lDiv: {
    fontWeight: 800,
    minWidth: 120,
    marginRight: theme.spacing.unit * 4,
    textAlign: 'right',
  },
  rDiv: {
    textAlign: 'left',
  },
  root: {
    display: 'flex',
    flexDirection: 'row',
    marginBottom: theme.spacing.unit * 1,
  },
});

const DetailItem = withStyles(dStyles)(DetailBase);
const DetailLink = withStyles(dStyles)(DLinkBase);

function StudentDetail(props) {
  const [studentDetail, setStudentDetail] = useState({});
  const [loading, setLoading] = useState(true);
  const { classes: { header }, match: { params } } = props;
  const { studentId } = params;

  useEffect(() => {
    getStudentDetail(studentId).then((s) => {
      setStudentDetail(s);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
        <div>
            <h1>Student Detail</h1>
            <h2>Loading...</h2>
        </div>
    );
  }

  const {
    // studentId,
    studentFirstName,
    studentLastName,
    studentGender,
    school,
    schoolId,
    studentBirthDate,
    grade,
    studentStateId,
    studentYear,
    studentTerm,
  } = studentDetail;

  return (
      <div>
          <Typography className={header} component="h1" variant="h4">{`${studentFirstName} ${studentLastName}`}</Typography>
          <DetailItem k="Gender" val={studentGender} />
          <DetailItem k="Birthdate" val={studentBirthDate} />
          <DetailItem k="Grade" val={grade} />
          <DetailItem k="Year" val={studentYear} />
          <DetailItem k="Term" val={studentTerm} />
          <DetailItem k="State Id" val={studentStateId} />
          <DetailLink k="School" val={school} link={`/school/${schoolId}`} />
      </div>
  );
}


const styles = theme => ({
  header: {
    color: theme.palette.primary.main,
    marginBottom: theme.spacing.unit * 1,
    textTransform: 'uppercase',
  },
  striped: {
    background: theme.grays.g0,
  },
  tHead: {
    fontSize: 16,
    color: theme.palette.primary.main,
    textTransform: 'uppercase',
  },
  tRow: {
    height: 32,
  },
});

StudentDetail.propTypes = {
  classes: PropTypes.object,
  match: PropTypes.object,
};

export default withStyles(styles)(StudentDetail);
