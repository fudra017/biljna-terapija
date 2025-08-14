// src/context/UserContext.jsx

import { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext();

export function UserProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const userData = localStorage.getItem("biljnaUser");
      return userData ? JSON.parse(userData) : null;
    } catch {
      return null;
    }
  });

  const [token, setToken] = useState(() => {
    return localStorage.getItem("jwtToken") || null;
  });

  // Funkcija za proveru autentifikacije
  const isAuthenticated = () => !!token && !!user;

  // ✅ Funkcija za odjavu
  const logout = () => {
    localStorage.removeItem("jwtToken");
    localStorage.removeItem("biljnaUser");
    localStorage.removeItem("ulogovan"); // ako koristiš
    setUser(null);
    setToken(null);
  };

  // Kada se korisnik promeni, ažuriraj localStorage
  useEffect(() => {
    if (user) {
      localStorage.setItem("biljnaUser", JSON.stringify(user));
    }
  }, [user]);

  // Kada se token promeni, ažuriraj localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem("jwtToken", token);
    }
  }, [token]);

  return (
    <UserContext.Provider
      value={{
        user,
        setUser,
        token,
        setToken,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}

// Hook za lako korišćenje konteksta u komponentama
export const useUser = () => useContext(UserContext);
