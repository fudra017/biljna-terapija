import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [lozinka, setLozinka] = useState('');
  const [greska, setGreska] = useState('');
  const navigate = useNavigate();
  const { setUser } = useUser(); // ✅ koristi UserContext

  const handleSubmit = (e) => {
    e.preventDefault();

    // ✅ Validacija emaila
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      setGreska('Unesite ispravnu e-mail adresu.');
      return;
    }

    // ✅ Validacija lozinke
    if (!lozinka || lozinka.length < 6) {
      setGreska('Lozinka mora imati najmanje 6 karaktera.');
      return;
    }

    setGreska('');

    // ✅ Simulirani korisnik
    const korisnik = {
      ime: 'Draško',
      email: email
    };

    // ✅ Upis u localStorage
    localStorage.setItem('ulogovan', 'true');
    localStorage.setItem('biljnaUser', JSON.stringify(korisnik));

    // ✅ Ažuriranje globalnog konteksta
    setUser(korisnik);

    // ✅ Alert i preusmerenje
    alert('Prijava uspešna! (simulirano)');
    navigate('/analiza');
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
