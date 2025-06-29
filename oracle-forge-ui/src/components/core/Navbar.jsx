import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './Core.module.css';

export default function Navbar({ activeAdventure: propAdventure }) {
  const [activeAdventure, setActiveAdventure] = useState(null);

  useEffect(() => {
    if (propAdventure !== undefined) {
      setActiveAdventure(propAdventure);
      return;
    }

    fetch(`${API_BASE}/adventures/active`)
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setActiveAdventure(response.data?.active || null);
        } else {
          console.error("Failed to fetch active adventure:", response.error);
          setActiveAdventure(null);
        }
      })
      .catch(error => {
        console.error("Error fetching active adventure:", error);
        setActiveAdventure(null);
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
