import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdventurePage from './pages/AdventurePage';
import CharacterPage from './pages/CharacterPage';
import CombatPage from './pages/CombatPage';
import GeneratorPage from './pages/GeneratorPage';
import LookupPage from './pages/LookupPage';
import OraclePage from './pages/OraclePage';
import AdventureSelectorPage from './pages/AdventureSelectorPage';
import { useGetActiveAdventureQuery } from './api/adventureApi';
import './App.css';
import Navbar from './components/core/Navbar';

const App: React.FC = () => {
  const { data, isLoading, refetch } = useGetActiveAdventureQuery();
  const [activeAdventure, setActiveAdventure] = useState<string | null>(null);

  useEffect(() => {
    if (data && data.active) {
      setActiveAdventure(data.active);
    } else {
      setActiveAdventure(null);
    }
  }, [data]);

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!activeAdventure) {
    return (
      <AdventureSelectorPage
        onAdventureSelected={() => {
          refetch(); // Re-fetch active adventure after selection
        }}
      />
    );
  }

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<AdventurePage />} />
          <Route path="/adventure" element={<AdventurePage />} />
          <Route path="/character/:characterName" element={<CharacterPage />} />
          <Route path="/combat" element={<CombatPage />} />
          <Route path="/generators" element={<GeneratorPage />} />
          <Route path="/lookup" element={<LookupPage />} />
          <Route path="/oracle" element={<OraclePage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
