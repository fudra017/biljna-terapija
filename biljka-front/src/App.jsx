// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useUser } from "./context/UserContext";

import NavBar from "./components/NavBar";
import Header from "./components/Header";
import Home from "./pages/Home";
import Kontakt from "./pages/Kontakt";
import Login from "./pages/Login";
import Analiza from "./pages/Analiza";
import Profil from "./pages/Profil";
import ProtectedRoute from "./components/ProtectedRoute";
import Registracija from "./pages/Registracija";

export default function App() {
  const { user, setUser } = useUser();

  return (
    <Router>
      <div className="min-h-screen bg-white text-black dark:bg-slate-900 dark:text-gray-100">
        <NavBar user={user} setUser={setUser} />
	<Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/kontakt" element={<Kontakt />} />
	  <Route path="/registracija" element={<Registracija />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/analiza" element={<ProtectedRoute><Analiza /></ProtectedRoute>} />
	  <Route path="/profil" element={<ProtectedRoute><Profil /></ProtectedRoute>} />
        </Routes>
      </div>
    </Router>
  );
}
