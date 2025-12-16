import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* Hozircha Dashboard yo'q, vaqtinchalik Login ga otamiz */}
        <Route path="/dashboard" element={<h1 className="text-3xl text-center mt-10">Dashboard Coming Soon...</h1>} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;