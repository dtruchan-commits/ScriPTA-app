import { NavLink } from 'react-router-dom';

const Navigation: React.FC = () => {
  return (
    <nav className="navigation">
      <div className="nav-header">
        <h1>ScriPTA Admin Panel</h1>
        <p>Configuration Management System</p>
      </div>
      
      <ul className="nav-menu">
        <li>
          <NavLink 
            to="/" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
            end
          >
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/swatches" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            Swatch Config
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/layers" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            Layer Config
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/tpm" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            TPM Config
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;