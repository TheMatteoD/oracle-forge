import React from 'react';
import Navbar from '../components/core/Navbar';

const CombatPage: React.FC = () => {
  // TODO: Reintroduce Combat components using RTK Query
  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      <h1>Combat Page (Under Refactor)</h1>
    </div>
  );
};

export default CombatPage;
