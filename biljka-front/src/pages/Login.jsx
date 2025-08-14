// src/pages/Login.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import api from '../api/axios';

export default function Login() {
  const [email, setEmail] = useState('');
  const [lozinka, setLozinka] = useState('');
  const [greska, setGreska] = useState('');
  const navigate = useNavigate();
  const { setUser, setToken } = useUser(); // Dodato: setToken
  // ✅ Ovde ide useEffect, odmah nakon inicijalizacije hook-ova
  useEffect(() => {
    if (localStorage.getItem("jwtToken") && localStorage.getItem("biljnaUser")) {
      navigate("/analiza"); // možeš da menjaš destinaciju ako želiš
    }
  }, []);
  // ostatak funkcije...
  const handleSubmit = async (e) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      setGreska('Unesite ispravnu e-mail adresu.');
      return;
    }

    if (!lozinka || lozinka.length < 6) {
      setGreska('Lozinka mora imati najmanje 6 karaktera.');
      return;
    }

    setGreska('');

    try {
      const response = await api.post('/auth/login',
        new URLSearchParams({
          username: email,
          password: lozinka
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );
      console.log("📥 Backend response (ceo):", response.data);
      console.log("👤 user iz response.data.user:", response.data.user);
      if (response.data.user) {
  	// validan login
      } else {
  	console.log("⚠️ Korisnik nije validan:", response.data.user);
      }

      const token = response.data.access_token;
      const korisnik = response.data.user;

      console.log("✅ Uspesna prijava:", response.data);
      console.log("👤 Korisnik (response.data.user):", korisnik);
      console.log("👁️ Pregled user objekta:", JSON.stringify(response.data.user, null, 2));
      if (!token || typeof token !== 'string') {
        console.error("⚠️ Token nije dobijen ili nije validan:", token);
        setGreska("Neuspešno logovanje: token nedostaje.");
        return;
      }

      if (!korisnik || typeof korisnik !== 'object') {
        console.error("⚠️ Korisnik nije validan:", korisnik);
        setGreska("Neuspešno logovanje: korisnik nedostaje.");
        return;
      }

      // ✅ Čuvanje u localStorage
      localStorage.setItem('jwtToken', token);
      localStorage.setItem('biljnaUser', JSON.stringify(korisnik));
      localStorage.setItem('ulogovan', 'true');

      // ✅ Ažuriranje konteksta
      setUser(korisnik);
      setToken(token);

      alert('Prijava uspešna!');
      navigate('/'); // ili npr. '/analiza'

    } catch (error) {
      console.error('❌ Greška prilikom prijave:', error);
      if (error.response && error.response.status === 401) {
        setGreska('Neispravan e-mail ili lozinka.');
      } else {
        setGreska('Došlo je do greške. Pokušajte ponovo.');
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-2xl font-bold text-center text-red-600">Prijava</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">E-mail adresa</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Lozinka</label>
          <input
            type="password"
            value={lozinka}
            onChange={(e) => setLozinka(e.target.value)}
            className="mt-1 block w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {greska && <p className="text-red-600 text-sm">{greska}</p>}

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
        >
          Prijavi se
        </button>
      </form>
    </div>
  );
}
