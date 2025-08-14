// 📁 Analiza.jsx
import React, { useState } from "react";
import axios from "axios";
import {
  FaUser,
  FaVenusMars,
  FaBaby,
  FaStethoscope,
  FaHeartbeat,
  FaAllergies,
  FaDumbbell,
  FaBrain,
  FaLeaf,
  FaFlask,
  FaGlobeEurope
} from "react-icons/fa";
import { useUser } from "../context/UserContext";

const statusMapper = {
  "Fizioloski status": "fizioloski_status",
  "Nutritivni status": "nutritivni_status",
  "Psiholoski faktori": "psiholoski_faktori",
  "Zivotni stil": "zivotni_stil",
  "Genetski faktori": "genetski_faktori",
  "Okruzenje": "okruzenje"
};

const Analiza = () => {
  const [godine, setGodine] = useState("");
  const [pol, setPol] = useState("");
  const [trudnoca, setTrudnoca] = useState(false);
  const [dijagnoza, setDijagnoza] = useState("");
  const [komorbiditet, setKomorbiditet] = useState("");
  const [alergija, setAlergija] = useState("");
  const [statusi, setStatusi] = useState({});
  const [otvoreneGrupe, setOtvoreneGrupe] = useState({});
  const [prikaziPreporuku, setPrikaziPreporuku] = useState(false);
  const [poruka, setPoruka] = useState("");
  const [preporuka, setPreporuka] = useState(
    `Sistem je u fazi provere funkcionalnosti. Vaši podaci su uspešno obrađeni.
Uskoro će biti dostupne personalizovane preporuke koje uključuju biljke, suplemente,
ishranu i druge savete. Ova poruka je informativna i ne predstavlja medicinski savet.`
  );

  const { user, token } = useUser();

  const statusGrupa = {
    "Fizioloski status": ["Vitalne funkcije", "Hronična stanja", "Laboratorije"],
    "Nutritivni status": ["Unos makronutrijenata", "Unos mikronutrijenata", "Digestivno zdravlje"],
    "Psiholoski faktori": ["Stres i anksioznost", "Emocionalna stabilnost", "Kognitivna funkcija"],
    "Zivotni stil": ["Fizička aktivnost", "San i odmor", "Zloupotreba supstanci"],
    "Genetski faktori": ["Porodična anamneza", "Genetski rizici", "Nasledne bolesti"],
    "Okruzenje": ["Zagađenje", "Socioekonomski faktori", "Radno okruzenje"]
  };

  const statusIkonice = {
    "Fizioloski status": <FaHeartbeat className="inline mr-2 text-blue-700" />,
    "Nutritivni status": <FaLeaf className="inline mr-2 text-green-700" />,
    "Psiholoski faktori": <FaBrain className="inline mr-2 text-purple-700" />,
    "Zivotni stil": <FaDumbbell className="inline mr-2 text-orange-700" />,
    "Genetski faktori": <FaFlask className="inline mr-2 text-pink-700" />,
    "Okruzenje": <FaGlobeEurope className="inline mr-2 text-gray-700" />
  };

const statusKeyMapper = {
  // Fizioloski status
  "Vitalne funkcije": "vitalne_funkcije",
  "Hronična stanja": "hronicna_stanja",
  "Laboratorije": "laboratorije",

  // Nutritivni status
  "Unos makronutrijenata": "unos_makronutrijenata",
  "Unos mikronutrijenata": "unos_mikronutrijenata",
  "Digestivno zdravlje": "digestivno_zdravlje",

  // Psiholoski faktori
  "Stres i anksioznost": "stres_i_anksioznost",
  "Emocionalna stabilnost": "emocionalna_stabilnost",
  "Kognitivna funkcija": "mentalna_jacina", // Ako backend očekuje "mentalna_jacina"

  // Zivotni stil
  "Fizička aktivnost": "fizicka_aktivnost",
  "San i odmor": "navike_spavanja",
  "Zloupotreba supstanci": "zloupotreba_supstanci",

  // Genetski faktori
  "Porodična anamneza": "porodicna_istorija",
  "Genetski rizici": "nasledne_bolesti",
  "Nasledne bolesti": "etnicka_pozadina",

  // Okruzenje
  "Zagađenje": "zagadjenje_i_toksini",
  "Socioekonomski faktori": "socioekonomski_faktori",
  "Radno okruzenje": "uslovi_stanovanja"
};


  const handleStatusChange = (group, item, value) => {
    setStatusi((prev) => ({
      ...prev,
      [group]: {
        ...(prev[group] || {}),
        [item]: value
      }
    }));
  };

  const handleToggleGroup = (group) => {
    setOtvoreneGrupe((prev) => ({
      ...prev,
      [group]: !prev[group]
    }));
  };

  const handleSubmit = async () => {
    const token = localStorage.getItem("jwtToken");

  const mappedStatusi = {};
  for (const [grupa, vrednosti] of Object.entries(statusi)) {
    const backendGrupaKey = statusMapper[grupa];
    if (backendGrupaKey) {
      const mappedValues = {};
      for (const [key, val] of Object.entries(vrednosti)) {
        const mappedKey = statusKeyMapper[key] || key;
        mappedValues[mappedKey] = val;
      }
      mappedStatusi[backendGrupaKey] = mappedValues;
    }
  }

    const podaci = {
      godine,
      pol,
      trudnoca: pol === "Ženski" ? trudnoca : false,
      dijagnoza,
      komorbiditeti: komorbiditet,
      alergije: alergija,
      ...mappedStatusi
    };

    console.log("✅ Podaci koji se šalju:", JSON.stringify(podaci, null, 2));

    try {
      const response = await axios.post("http://localhost:8000/api/analiza/create", podaci, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      console.log("✅ Uspešan odgovor:", response.data);
      setPoruka(response.data.message);
      alert("Podaci uspešno poslati!");
      setPrikaziPreporuku(true);
      setPoruka("Podaci su uspešno sačuvani. Preporuka je prikazana.");

      setGodine(0);
      setPol("");
      setTrudnoca(false);
      setDijagnoza("");
      setKomorbiditet("");
      setAlergija("");
      setStatusi({
        "Fizioloski status": {},
        "Nutritivni status": {},
        "Psiholoski faktori": {},
        "Zivotni stil": {},
        "Genetski faktori": {},
        "Okruzenje": {}
      });

    } catch (error) {
      console.error("❌ Greška prilikom slanja:", error.response?.data || error.message);
      alert("Slanje nije uspelo. Proveri podatke ili prijavu.");
    }
  };

  const handleSendEmail = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/email/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          email: user?.email,
          subject: "Biljna terapija",
          content: preporuka
        })
      });

      if (response.ok) {
        setPoruka("✅ Preporuka uspešno poslata mejlom.");
      } else {
        const err = await response.json();
        setPoruka("❌ Slanje mejla nije uspelo: " + err.detail);
      }
    } catch (error) {
      console.error("❌ Greška pri slanju mejla:", error);
      setPoruka("⚠️ Došlo je do greške pri slanju mejla.");
    }
  };

  const handleDownloadPDF = () => {
    const element = document.createElement("a");
    const file = new Blob([preporuka], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "preporuka.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Analiza pacijenta</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaUser className="inline mr-1" />Godine:</label>
          <input
  	    type="number"
  	    value={isNaN(godine) ? "" : godine}
  	    onChange={(e) => setGodine(Number(e.target.value))}
  	    className="mt-1 p-2 border rounded w-full"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaVenusMars className="inline mr-1" />Pol:</label>
          <select
            value={pol}
            onChange={(e) => setPol(e.target.value)}
            className="mt-1 p-2 border rounded w-full"
          >
            <option value="">Odaberi</option>
            <option value="Muški">Muški</option>
            <option value="Ženski">Ženski</option>
          </select>
        </div>

        {pol === "Ženski" && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-blue-700"><FaBaby className="inline mr-1" />Da li je pacijentkinja trudna?</label>
            <select
              value={trudnoca ? "Da" : "Ne"}
              onChange={(e) => setTrudnoca(e.target.value === "Da")}
              className="mt-1 p-2 border rounded w-full"
            >
              <option value="Ne">Ne</option>
              <option value="Da">Da</option>
            </select>
          </div>
        )}

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaStethoscope className="inline mr-1" />Dijagnoza:</label>
          <select
            value={dijagnoza}
            onChange={(e) => setDijagnoza(e.target.value)}
            className="mt-1 p-2 border rounded w-full"
          >
            <option value="">Odaberi dijagnozu</option>
            <option value="Astma">Astma</option>
            <option value="Hipertenzija">Hipertenzija</option>
            <option value="Dijabetes tip 2">Dijabetes tip 2</option>
            <option value="Osteoporoza">Osteoporoza</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaHeartbeat className="inline mr-1" />Komorbiditeti:</label>
          <select
            value={komorbiditet}
            onChange={(e) => setKomorbiditet(e.target.value)}
            className="mt-1 p-2 border rounded w-full"
          >
            <option value="">Odaberi komorbiditet</option>
            <option value="Dijabetes tip 2">Dijabetes tip 2</option>
            <option value="Hipertenzija">Hipertenzija</option>
            <option value="Astma">Astma</option>
            <option value="Osteoporoza">Osteoporoza</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaAllergies className="inline mr-1" />Poznate alergije:</label>
          <select
            value={alergija}
            onChange={(e) => setAlergija(e.target.value)}
            className="mt-1 p-2 border rounded w-full"
          >
            <option value="">Odaberi alergiju</option>
            <option value="Polen">Polen</option>
            <option value="Praškovi i deterdženti">Praškovi i deterdženti</option>
            <option value="Penicilin">Penicilin</option>
            <option value="Jaja">Jaja</option>
            <option value="Riba i plodovi mora">Riba i plodovi mora</option>
            <option value="Orašasti plodovi">Orašasti plodovi</option>
            <option value="Lateks">Lateks</option>
          </select>
        </div>
      </div>

      {/* Statusi */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(statusGrupa).map(([grupa, stavke]) => (
          <div key={grupa} className="mb-4 border rounded p-3">
            <h3
              className="font-semibold mb-2 cursor-pointer text-blue-700"
              onClick={() => handleToggleGroup(grupa)}
            >
              {statusIkonice[grupa]}{grupa}
            </h3>
            {otvoreneGrupe[grupa] && stavke.map((stavka) => (
              <div key={stavka} className="mb-2">
                <label className="block text-sm font-medium text-blue-700">{stavka}:</label>
                <select
                  value={statusi?.[grupa]?.[stavka] || ""}
                  onChange={(e) => handleStatusChange(grupa, stavka, e.target.value)}
                  className="mt-1 p-2 border rounded w-full"
                >
                  <option value="">Odaberi status</option>
                  <option value="Dobar">Dobar</option>
                  <option value="Srednji">Srednji</option>
                  <option value="Loš">Loš</option>
                </select>
              </div>
            ))}
          </div>
        ))}
      </div>

      <button
        onClick={handleSubmit}
        className="mt-6 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Pošalji
      </button>
      {prikaziPreporuku && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl w-full">
            <h2 className="text-xl font-bold mb-4">Tvoja personalizovana preporuka</h2>
            <div className="overflow-y-auto max-h-80 whitespace-pre-line text-gray-800">
              {preporuka}
            </div>
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => setPrikaziPreporuku(false)}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Zatvori
              </button>
              <button
                onClick={handleDownloadPDF}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Preuzmi PDF
              </button>
              <button
                onClick={handleSendEmail}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Pošalji na e-mail
              </button>
            </div>
            {poruka && (
  	      <div className="mt-4 text-center text-red-600 font-semibold">
    		{poruka}
  	      </div>
	    )}
          </div>
        </div>
      )}
      </div>
      );

    };

export default Analiza;