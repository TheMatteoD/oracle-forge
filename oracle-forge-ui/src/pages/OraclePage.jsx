import React, { useState } from 'react';
import Navbar from '../components/core/Navbar';
import YesNoOracle from '../components/oracle/YesNoOracle';
import MeaningOracle from '../components/oracle/MeaningOracle';
import SceneCheck from '../components/oracle/SceneCheck';

export default function OraclePage() {
  const [chaos, setChaos] = useState(5);

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      <h1 style={{ fontSize: '1.5em' }}>🔮 Oracle Forge</h1>

      <section style={{ marginBottom: '2em' }}>
        <label>Chaos Factor (1-9):
          <input
            type="number"
            min="1"
            max="9"
            value={chaos}
            onChange={(e) => setChaos(parseInt(e.target.value))}
          />
        </label>
      </section>

      <YesNoOracle chaos={chaos} />
      <MeaningOracle chaos={chaos} />
      <SceneCheck chaos={chaos} />
    </div>
  );
}
