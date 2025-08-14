// src/components/Header.jsx

import { useUser } from "../context/UserContext";
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { FaLinkedin, FaGithub, FaMoon, FaSun } from "react-icons/fa";

export default function Header() {
  const { user } = useUser();
  const location = useLocation();

  const [vreme, setVreme] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setVreme(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const breadcrumbs = {
    "/": "Početna",
    "/analiza": "Analiza",
    "/login": "Prijava",
    "/registracija": "Registracija",
    "/kontakt": "Kontakt",
    "/profil": "Profil",
  };

  return (
    <header className="bg-white dark:bg-slate-800 shadow px-4 py-3 border-b border-gray-200 dark:border-slate-700">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        {/* ✅ Gornji red – korisnik, vreme, jezik */}
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600 dark:text-gray-300">
            {user ? `Zdravo, ${user.ime}!` : "Dobrodošli!"}
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {vreme.toLocaleDateString("sr-RS")} {vreme.toLocaleTimeString("sr-RS")}
          </span>
          <button className="text-xs px-2 py-1 border rounded hover:bg-gray-100 dark:hover:bg-slate-700">
            🇷🇸 SR
          </button>
          <button className="text-xs px-2 py-1 border rounded hover:bg-gray-100 dark:hover:bg-slate-700">
            🇬🇧 EN
          </button>
        </div>

        {/* ✅ Breadcrumb i dugmad */}
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600 dark:text-gray-300">
            {breadcrumbs[location.pathname] || "Stranica"}
          </span>
          <button className="text-xl hover:text-yellow-500" title="Tamni mod">
            <FaMoon />
          </button>
          <a href="https://github.com/" target="_blank" rel="noreferrer" className="text-xl hover:text-black dark:hover:text-white">
            <FaGithub />
          </a>
          <a href="https://linkedin.com/" target="_blank" rel="noreferrer" className="text-xl hover:text-blue-700">
            <FaLinkedin />
          </a>
        </div>
      </div>
    </header>
  );
}

