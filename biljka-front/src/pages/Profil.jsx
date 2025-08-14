// src/Pages/Profil.jsx
import { useUser } from "../context/UserContext";
import { Navigate } from "react-router-dom";

export default function Profil() {
  const { user } = useUser();

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Profil korisnika</h2>
      <p><strong>Ime:</strong> {user?.ime}</p>
      <p><strong>Email:</strong> {user?.email}</p>
    </div>
  );
}
