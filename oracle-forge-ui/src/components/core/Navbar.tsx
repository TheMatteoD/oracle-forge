import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '../../api/apiClient';
import styles from './Core.module.css';

interface NavbarProps {
  activeAdventure?: string | null;
}

export default function Navbar({ activeAdventure: propAdventure }: NavbarProps) {
  const [activeAdventure, setActiveAdventure] = useState<string | null>(null);

  useEffect(() => {
    if (propAdventure !== undefined) {
      setActiveAdventure(propAdventure);
      return;
    }

    apiClient.get('/adventures/active')
      .then(response => {
        const data = response.data as { active?: string };
        if (response.success) {
          setActiveAdventure(data?.active || null);
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