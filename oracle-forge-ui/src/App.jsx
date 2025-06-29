import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import OraclePage from './pages/OraclePage';
import AdventurePage from './pages/AdventurePage';
import LookupPage from './pages/LookupPage';
import GeneratorPage from './pages/GeneratorPage';
import CombatPage from './pages/CombatPage';
import CharacterPage from './pages/CharacterPage';
import { apiGet } from './api/apiClient';

function App() {
  const [activeAdventure, setActiveAdventure] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet('/adventures/active')
      .then(response => {
        if (response.success && response.data?.active) {
          localStorage.setItem("activeAdventure", response.data.active);
          setActiveAdventure(response.data.active);
        } else {
          localStorage.removeItem("activeAdventure");
          setActiveAdventure(null);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching active adventure:", error);
        setActiveAdventure(null);
        setLoading(false);
      });
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<AdventurePage setActiveAdventure={setActiveAdventure} />} />
        <Route path="/adventure" element={<AdventurePage setActiveAdventure={setActiveAdventure} />} />
        <Route path="/character/:characterName" element={<CharacterPage />} />
        <Route path="/oracle" element={<OraclePage />} />
        <Route path="/lookup" element={<LookupPage />} />
        <Route path="/generators" element={<GeneratorPage />} />
        <Route path="/combat" element={<CombatPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
