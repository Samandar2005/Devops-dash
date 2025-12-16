import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard'; // Dashboardni import qildik

function App() {
  // Oddiy tekshiruv: Token bormi?
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <Router>
      <Routes>
        {/* Login sahifasi */}
        <Route path="/login" element={<Login />} />
        
        {/* Himoyalangan Dashboard yo'li */}
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
        />
        
        {/* Noto'g'ri manzil kiritilsa avtomatik yo'naltirish */}
        <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;