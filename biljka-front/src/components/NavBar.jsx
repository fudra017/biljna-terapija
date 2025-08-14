// biljka-front/src/components/NavBar.jsx
import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

export default function NavBar() {
  const { user, setUser } = useUser();
  const navigate = useNavigate();
  const [meniOtvoren, setMeniOtvoren] = useState(false);
  const meniRef = useRef(null);

  const jeUlogovan = !!user;

  const handleLogout = () => {
    localStorage.removeItem('ulogovan');
    localStorage.removeItem('biljnaUser');
    localStorage.removeItem('jwtToken');
    setUser(null);
    setMeniOtvoren(false);
    navigate('/login');
  };

  // Automatsko zatvaranje na klik van menija
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (meniRef.current && !meniRef.current.contains(e.target)) {
        setMeniOtvoren(false);
      }
    };
    if (meniOtvoren) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [meniOtvoren]);

  return (
    <nav className="bg-green-600 text-white px-4 py-3 shadow-md">
      <div className="flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">Biljna Terapija</Link>

        <button
          className="sm:hidden text-2xl focus:outline-none"
          onClick={() => setMeniOtvoren(!meniOtvoren)}
        >
          ☰
        </button>

        <div className="hidden sm:flex space-x-6 items-center">
          <Link to="/analiza" className="hover:underline">Analiza</Link>
          <Link to="/kontakt" className="hover:underline">Kontakt</Link>
	{!jeUlogovan ? (
          <>
            <Link to="/login" className="hover:underline">Prijava</Link>
            <Link to="/registracija" className="hover:underline">Registracija</Link>
          </>
        ) : (
            <div className="relative group">
              <button className="hover:underline">{user.ime} ▼</button>
              <div className="absolute right-0 mt-1 bg-white text-black rounded shadow-md hidden group-hover:block">
                <Link to="/profil" className="block px-4 py-2 hover:bg-gray-100">Profil</Link>
                <button onClick={handleLogout} className="block w-full text-left px-4 py-2 hover:bg-gray-100">Odjavi se</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Dropdown meni za mobilne korisnike sa animacijom */}
      <div
        ref={meniRef}
        className={`sm:hidden transition-all duration-300 ease-in-out overflow-hidden ${
          meniOtvoren ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="mt-3 space-y-2">
          <Link to="/analiza" className="block hover:underline" onClick={() => setMeniOtvoren(false)}>Analiza</Link>
          <Link to="/kontakt" className="block hover:underline" onClick={() => setMeniOtvoren(false)}>Kontakt</Link>
          {!jeUlogovan ? (
  	    <>
              <Link to="/login" className="block hover:underline" onClick={() => setMeniOtvoren(false)}>Prijava</Link>
              <Link to="/registracija" className="block hover:underline" onClick={() => setMeniOtvoren(false)}>Registracija</Link>
            </>
          ) : (
            <>
              <Link to="/profil" className="block hover:underline" onClick={() => setMeniOtvoren(false)}>Profil</Link>
              <button onClick={handleLogout} className="block w-full text-left hover:underline">Odjavi se</button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}





