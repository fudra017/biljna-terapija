//Home.jsx
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="p-6 space-y-6">
      
      {/* ✅ Navigacioni meni sa dugmadi */}
      {/* Navigacioni meni se sada koristi iz NavBar komponente */}
	
      {/* ✅ Ostatak originalnog sadržaja */}
      <div className="text-center space-y-4 mt-12">
        <h1 className="text-3xl font-bold text-green-700">Biljna Terapija</h1>
        <p className="text-lg text-gray-800">
		          Aplikacija za personalizovane preporuke biljnih terapija na osnovu vašeg zdravstvenog stanja.
        </p>
		
		<p className="text-lg text-gray-800">  
		
		Ulaz u aplikaciju Biljna Terapija je Registracija, klik na dugme gore desno. Svaki sledeći pristup ide preko dugmeta Prijava.
		</p>
        <p className="text-md text-gray-700">
          Kliknite na dugme Analiza i unesite svoje osnovne parametre i saznajte koji prirodni tretmani mogu da vam pomognu.
        </p>
      </div>

    </div>
  );
}
