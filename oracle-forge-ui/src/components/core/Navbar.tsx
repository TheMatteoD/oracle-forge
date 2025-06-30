import { Link } from 'react-router-dom';
import styles from './Core.module.css';

// TODO: Add RTK Query integration for active adventure if needed
export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link to="/adventure">🌍 Adventure</Link>
      <Link to="/oracle">🔮 Oracle</Link>
      <Link to="/lookup">📚 Lookups</Link>
      <Link to="/generators">🛠️ Generators</Link>
      <Link to="/combat">⚔️ Combat</Link>
    </nav>
  );
} 