// src/pages/Registracija.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Registracija() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    ime: "",
    prezime: "",
    email: "",
    sifra: ""
  });

  const [greska, setGreska] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setGreska("");
    try {
      const response = await axios.post("http://localhost:8000/api/korisnik/registracija", formData);
      alert("✅ Registracija uspešna!");
      navigate("/login");
    } catch (err) {
      const msg = err.response?.data?.detail || "Greška pri registraciji.";
      setGreska(msg);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md mt-10">
      <h2 className="text-2xl font-semibold text-center mb-6">Registracija</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="ime"
          value={formData.ime}
          onChange={handleChange}
          placeholder="Ime"
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <input
          type="text"
          name="prezime"
          value={formData.prezime}
          onChange={handleChange}
          placeholder="Prezime"
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <input
          type="password"
          name="sifra"
          value={formData.sifra}
          onChange={handleChange}
          placeholder="Lozinka"
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        {greska && <p className="text-red-500 text-sm">{greska}</p>}
        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
        >
          Registruj se
        </button>
      </form>
    </div>
  );
}
