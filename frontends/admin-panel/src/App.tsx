import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import LayerConfigView from './components/LayerConfigView';
import Navigation from './components/Navigation';
import SwatchConfigView from './components/SwatchConfigView';
import TpmConfigView from './components/TpmConfigView';
import './styles/admin.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/swatches" element={<SwatchConfigView />} />
            <Route path="/layers" element={<LayerConfigView />} />
            <Route path="/tpm" element={<TpmConfigView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
