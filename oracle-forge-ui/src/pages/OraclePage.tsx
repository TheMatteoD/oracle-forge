import React from 'react';
import YesNoOracle from '../components/oracle/YesNoOracle';
import SceneCheck from '../components/oracle/SceneCheck';
import MeaningOracle from '../components/oracle/MeaningOracle';

const OraclePage: React.FC = () => {
  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <h1>Oracle Page</h1>
      <SceneCheck chaos={5} />
      {/* <YesNoOracle chaos={5} /> */}
      {/* <MeaningOracle chaos={5} /> */}
    </div>
  );
};

export default OraclePage;
