import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdventurePage from './pages/AdventurePage';
import CharacterPage from './pages/CharacterPage';
import CombatPage from './pages/CombatPage';
import GeneratorPage from './pages/GeneratorPage';
import LookupPage from './pages/LookupPage';
import OraclePage from './pages/OraclePage';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
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
