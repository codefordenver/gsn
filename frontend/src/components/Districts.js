import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getDistricts } from 'services/districtServices';

export default function Districts(props) {
  const [districts, setDistricts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('useEffect ran in Districts');
    getDistricts().then((d) => {
      setDistricts(d);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
        <div>
            <h1>Districts</h1>
            <h2>Loading...</h2>
        </div>
    );
  }

  return (
      <div>
          <h1>Districts</h1>
          {districts.map((district) => {
            const {
              id, districtState, districtCity, districtCode,
            } = district;
            return (
                <p key={id}>
                    <Link to={`district/${id}`}>
                        {districtCode}: {districtCity}, {districtState}
                    </Link>
                </p>
            );
          })}
      </div>
  );
}
