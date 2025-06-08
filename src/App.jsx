// src/App.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import NavBar from './components/NavBar';
import Home from "./Pages/Home";
import Kontakt from "./Pages/Kontakt";
import Login from "./Pages/Login";
import Analiza from "./Pages/Analiza";
import ProtectedRoute from "./components/ProtectedRoute";
import Profil from "./Pages/Profil";

function App() {
  const [user, setUser] = useState(null);

  // Učitavanje korisnika iz localStorage prilikom pokretanja
  useEffect(() => {
    const savedUser = localStorage.getItem("biljnaUser");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-white text-black"> {/* Možeš dodati Tailwind klase ako koristiš */}
        <NavBar /> {/* ✅ Prikazuje navigaciju na svim stranicama */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/kontakt" element={<Kontakt />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/analiza" element={<ProtectedRoute user={user}> <Analiza /> </ProtectedRoute> } />
          <Route path="/profil" element={<Profil />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;




//import React, { useState, useEffect } from "react"
//import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

//import NavBar from './components/NavBar';
//import Home from './pages/Home';
//import Analiza from './pages/Analiza';
//import Kontakt from './pages/Kontakt';
//import Login from './pages/Login';
//import ProtectedRoute from './components/ProtectedRoute';

//export default function App() {
//  return (
//    <Router>
//      <div className="min-h-screen bg-gray-100">
//        <NavBar />
//        <div className="p-6">
//          <Routes>
//            <Route path="/" element={<Home />} />
//            <Route path="/analiza" element={<ProtectedRoute> <Analiza /> </ProtectedRoute>} />
//            <Route path="/kontakt" element={<Kontakt />} />
//            <Route path="/login" element={<Login />} />
//          </Routes>
//        </div>
//      </div>
//    </Router>
//  );
//} 






// src/App.jsx
//import React, { useState, useEffect } from "react";
//import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

//import NavBar from './components/NavBar';
//import Home from "./pages/Home";
//import Kontakt from "./pages/Kontakt";
//import Prijava from "./pages/Login";
//import Analiza from "./pages/Analiza";
//import ProtectedRoute from "./components/ProtectedRoute";

//function App() {
//  const [user, setUser] = useState(null);

  // Učitavanje korisnika iz localStorage prilikom pokretanja
//  useEffect(() => {
//    const savedUser = localStorage.getItem("biljnaUser");
//    if (savedUser) {
//      setUser(JSON.parse(savedUser));
//    }
//  }, []);

//  return (
//    <Router>
//     <Routes>
//       <Route path="/" element={<Home />} />
//        <Route path="/kontakt" element={<Kontakt />} />
//        <Route path="/prijava" element={<Login setUser={setUser} />} />
//        <Route path="/analiza" element={<ProtectedRoute user={user}> <Analiza /> </ProtectedRoute>} />
//      </Routes>
//    </Router>
//  );
//}




















//export default function App() {
//  return (
//    <div className="h-screen flex items-center justify-center bg-green-600 text-white text-3xl font-bold">
//      TAILWIND 3.4.1 radi savršeno
//    </div>
//  );
//}