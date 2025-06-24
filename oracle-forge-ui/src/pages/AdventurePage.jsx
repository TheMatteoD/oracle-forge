import React, { useEffect, useState } from 'react';
import config from "../config";
import Navbar from '../components/core/Navbar';
import AdventureSelector from '../components/adventure/AdventureSelector';
import SessionDashboard from '../components/adventure/SessionDashboard';

const API_BASE = config.SERVER_URL;

export default function AdventurePage() {
  const [activeAdventure, setActiveAdventure] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/adventures/active`)
      .then(res => res.json())
      .then(data => {
        if (data.active) {
          setActiveAdventure(data.active);
        } else {
          setActiveAdventure(null);
        }
      })
      .catch(console.warn);
  }, []);
  
  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar activeAdventure={activeAdventure} />
      <h1 style={{ fontSize: '1.5em' }}>🔮 Oracle Forge</h1>
      {activeAdventure ? (
        <SessionDashboard adventure={activeAdventure} />
      ) : (
        <AdventureSelector onSelect={setActiveAdventure} />
      )}
    </div>
  );
}
