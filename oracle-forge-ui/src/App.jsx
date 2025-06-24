import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import OraclePage from './pages/OraclePage';
import AdventurePage from './pages/AdventurePage';
import LookupPage from './pages/LookupPage';
import GeneratorPage from './pages/GeneratorPage';
import CombatPage from './pages/CombatPage';
import CharacterPage from './pages/CharacterPage';
import config from "./config";

const API_BASE = config.SERVER_URL;

function App() {
  const [activeAdventure, setActiveAdventure] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/adventures/active`)
      .then(res => res.json())
      .then(data => {
        if (data.active) {
          localStorage.setItem("activeAdventure", data.active);
          setActiveAdventure(data.active);
        } else {
          localStorage.removeItem("activeAdventure");
          setActiveAdventure(null);
        }
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
