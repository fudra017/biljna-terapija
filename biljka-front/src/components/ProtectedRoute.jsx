// src/components/ProtectedRoute.jsx

import { Navigate } from "react-router-dom";
import { useUser } from "../context/UserContext";

export default function ProtectedRoute({ children }) {
  const { user, token } = useUser();

  if (!user || !user.email || !token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
