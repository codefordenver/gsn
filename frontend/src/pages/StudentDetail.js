import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Link as StyledLink, Typography, withStyles,
} from '@material-ui/core';
import PropTypes from 'prop-types';

import { getStudentDetail } from 'services/studentServices';

const DetailBase = ({ k, val, classes: { lDiv, rDiv, root } }) => (
    <Typography color="primary" className={root}>
        <div className={lDiv}>{k}:</div>
        <div className={rDiv}>{val}</div>
    </Typography>
);

DetailBase.propTypes = {
  k: PropTypes.string,
  val: PropTypes.string,
  classes: PropTypes.object,
};

const DLinkBase = ({
  k, val, link, classes: { lDiv, rDiv, root },
}) => (
    <Typography color="primary" className={root}>
        <div className={lDiv}>{k}:</div>
        <div className={rDiv}><Link to={link}><StyledLink>{val}</StyledLink></Link></div>
    </Typography>
);

DLinkBase.propTypes = {
  k: PropTypes.string,
  val: PropTypes.string,
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
  const studentId = params;

  useEffect(() => {
    console.log('useEffect ran in StudentDetail', studentId);
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
          <Typography className={header} component="h1" variant="h4">{name}</Typography>
          <DetailItem k="Gender" val={gender} />
          <DetailItem k="Birthdate" val={birthdate} />
          <DetailItem k="Grade" val={grade} />
          <DetailItem k="Year" val={studentYear} />
          <DetailItem k="Term" val={studentTerm} />
          <DetailItem k="State Id" val={stateId} />
          <DetailItem k="Gender" val={stateId} />
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
