
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './Core.module.css';
import config from "../../config";

const API_BASE = config.SERVER_URL;

export default function Navbar({ activeAdventure: propAdventure }) {
  const [activeAdventure, setActiveAdventure] = useState(null);

  useEffect(() => {

    if (propAdventure !== undefined) {
      setActiveAdventure(propAdventure);
      return;
    }

    fetch(`${API_BASE}/adventures/active`)
      .then(res => res.json())
      .then(data => {
        setActiveAdventure(data.active || null);
      });
  }, [propAdventure]);

  return (
    <nav className={styles.navbar}>
      {activeAdventure && (
        <>
          <Link to="/adventure">🌍 {activeAdventure || 'Adventure'}</Link>
          <Link to="/oracle">🔮 Oracle</Link>
          <Link to="/lookup">📚 Lookups</Link>
          <Link to="/generators">🛠️ Generators</Link>
          <Link to="/combat">⚔️ Combat</Link>
        </>
      )}
    </nav>
  );
}
