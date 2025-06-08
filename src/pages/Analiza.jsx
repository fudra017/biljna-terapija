export default function Analiza() {
  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-semibold text-blue-700">Analiza korisničkih podataka</h2>
      <p className="text-gray-700">
        Ova stranica će sadržati obrazac za unos:
      </p>
      <ul className="list-disc list-inside text-gray-600">
        <li>Dijagnoze</li>
        <li>Pol i starost</li>
        <li>Trudnoća (ako je primenljivo)</li>
        <li>Komorbiditeti</li>
        <li>Alergije</li>
      </ul>
      <p className="text-gray-600">
        Možete birati između:
      </p>
      <ul className="list-disc list-inside text-gray-600">
        <li>AI preporuke</li>
        <li>Preporuke iz baze podataka</li>
        <li>Kombinovane analize</li>
      </ul>
    </div>
  );
}  