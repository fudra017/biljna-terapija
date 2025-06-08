import React from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  // Provera da li korisnik postoji u localStorage i da li je ulogovan
  const jeUlogovan = localStorage.getItem('ulogovan') === 'true';
  const korisnik = localStorage.getItem('biljnaUser');

  if (!jeUlogovan || !korisnik) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
