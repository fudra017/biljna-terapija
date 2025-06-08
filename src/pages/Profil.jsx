// src/Pages/Profil.jsx
export default function Profil() {
  const korisnik = JSON.parse(localStorage.getItem('biljnaUser'));

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Profil korisnika</h2>
      <p><strong>Ime:</strong> {korisnik?.ime}</p>
      <p><strong>Email:</strong> {korisnik?.email}</p>
    </div>
  );
}
