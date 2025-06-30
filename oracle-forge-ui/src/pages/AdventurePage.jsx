import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/apiClient';
import Navbar from '../components/core/Navbar';
import AdventureSelector from '../components/adventure/AdventureSelector';
import SessionDashboard from '../components/adventure/SessionDashboard';

export default function AdventurePage() {
  const [activeAdventure, setActiveAdventure] = useState(null);

  useEffect(() => {
    apiClient.get('/adventures/active')
      .then(response => {
        if (response.success && response.data?.active) {
          if (typeof response.data.active === 'string') {
            setActiveAdventure(null);
          } else {
            setActiveAdventure(response.data.active);
          }
        } else {
          setActiveAdventure(null);
        }
      })
      .catch(error => {
        console.error("Error fetching active adventure:", error);
        setActiveAdventure(null);
      });
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
