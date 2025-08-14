// 📁 Analiza.jsx (refaktor: realne preporuke iz backenda, bez statičkog teksta)
import React, { useState, useEffect } from "react";
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

// Helper: formatiranje JSON preporuke u plain text (za e-mail / TXT fallback)
function formatPreporukaAsText(p) {
  if (!p) return "";
  const L = (arr) => (arr && arr.length ? arr.map((x) => ` - ${x}`).join("\n") : " (nema)");
  return (
    `Preporuka za: ${p.bolest || "—"}\n\n` +
    `Biljke:\n${L(p.biljke)}\n\n` +
    `Suplementi:\n${L(p.suplementi)}\n\n` +
    `Literatura:\n${L(p.literatura)}\n` +
    (p.napomena ? `\nNapomena:\n${p.napomena}\n` : "")
  );
}

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

  // UI/feedback stanja
  const [prikaziPreporuku, setPrikaziPreporuku] = useState(false);
  const [poruka, setPoruka] = useState("");
  const [greska, setGreska] = useState("");

  // Dinamičke liste iz backenda
  const [dijagnozeLista, setDijagnozeLista] = useState([]);
  const [ucitavanjeDijagnoza, setUcitavanjeDijagnoza] = useState(false);
  const [greskaDijagnoze, setGreskaDijagnoze] = useState("");

  // 🔑 Novo: realna preporuka iz backenda (JSON objekat) + tekstualni format za e-mail / TXT fallback
  const [preporukaJson, setPreporukaJson] = useState(null);
  const [preporukaText, setPreporukaText] = useState("");

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
    "Kognitivna funkcija": "mentalna_jacina", // ako backend očekuje upravo ovaj ključ

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

  // Učitavanje dijagnoza iz backenda (CSV → servis → API)
  useEffect(() => {
    const fetchDijagnoze = async () => {
      try {
        setUcitavanjeDijagnoza(true);
        setGreskaDijagnoze("");
        const { data } = await axios.get("http://localhost:8000/api/preporuka/dijagnoze");
        let lista = Array.isArray(data?.dijagnoze) ? data.dijagnoze : [];
        lista = lista
          .filter(Boolean)
          .map((x) => (typeof x === "string" ? x.trim() : String(x)))
          .filter((x) => x.length > 0)
          .sort((a, b) => a.localeCompare(b, "sr", { sensitivity: "base" }));
        setDijagnozeLista(lista);
      } catch (e) {
        setGreskaDijagnoze(e?.response?.data?.detail || "Ne mogu da preuzmem spisak dijagnoza.");
      } finally {
        setUcitavanjeDijagnoza(false);
      }
    };

    fetchDijagnoze();
  }, []);

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
    const tokenLS = localStorage.getItem("jwtToken");

    // Mapiranje statusa u backend ključeve
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

    setGreska("");
    setPoruka("");
    setPreporukaJson(null);
    setPreporukaText("");

    try {
      // 1) (Opcionalno) Sačuvaj analizu
      const saveResp = await axios.post("http://localhost:8000/api/analiza/create", podaci, {
        headers: {
          Authorization: `Bearer ${tokenLS || token || ""}`,
          "Content-Type": "application/json"
        }
      });
      console.log("✅ Uspešan odgovor (save):", saveResp.data);

      // 2) Preuzmi preporuku za izabranu dijagnozu (stabilan JSON)
      const recResp = await axios.get("http://localhost:8000/api/preporuka", {
        params: { bolest: dijagnoza }
      });

      setPreporukaJson(recResp.data);
      setPreporukaText(formatPreporukaAsText(recResp.data));

      setPoruka("Podaci su uspešno sačuvani. Preporuka je prikazana.");
      setPrikaziPreporuku(true);

      // (Opcionalno) reset polja forme
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
      console.error("❌ Greška:", error?.response?.data || error?.message);
      setGreska(error?.response?.data?.detail || "Greška pri slanju ili preuzimanju preporuke.");
      setPrikaziPreporuku(true); // prikaži modal sa porukom o grešci
    }
  };

  const handleSendEmail = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/email/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token || ""}`
        },
        body: JSON.stringify({
          email: user?.email,
          subject: "Biljna terapija",
          content: preporukaText || formatPreporukaAsText(preporukaJson)
        })
      });

      if (response.ok) {
        setPoruka("✅ Preporuka uspešno poslata mejlom.");
      } else {
        const err = await response.json();
        setPoruka("❌ Slanje mejla nije uspelo: " + (err?.detail || "Nepoznata greška"));
      }
    } catch (error) {
      console.error("❌ Greška pri slanju mejla:", error);
      setPoruka("⚠️ Došlo je do greške pri slanju mejla.");
    }
  };

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function fallbackDownloadText() {
    const text = preporukaText || formatPreporukaAsText(preporukaJson) || "Nema preporuke.";
    const blob = new Blob([text], { type: "text/plain" });
    downloadBlob(blob, "preporuka.txt");
  }

  const handleDownloadPDF = async () => {
    // Pokušaj backendskog PDF-a (ako je aktiviran), inače TXT fallback
    const url = `http://localhost:8000/api/preporuka/pdf?bolest=${encodeURIComponent(dijagnoza || (preporukaJson?.bolest || ""))}`;

    try {
      const res = await fetch(url);
      const ct = res.headers.get("content-type") || "";

      if (res.ok && ct.includes("application/pdf")) {
        const blob = await res.blob();
        const fname = `preporuka_${(dijagnoza || preporukaJson?.bolest || "dijagnoza").replace(/\s+/g, "_")}.pdf`;
        downloadBlob(blob, fname);
      } else {
        // Backend PDF nije aktiviran (501) ili nije PDF → TXT fallback
        fallbackDownloadText();
      }
    } catch (e) {
      console.error("PDF download greška:", e);
      fallbackDownloadText();
    }
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
            required
            disabled={ucitavanjeDijagnoza}
          >
            <option value="">{ucitavanjeDijagnoza ? "Učitavanje..." : "Odaberi dijagnozu"}</option>
            {dijagnozeLista.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
          {greskaDijagnoze && (
            <div className="text-red-600 text-sm mt-1">{greskaDijagnoze}</div>
          )}
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-700"><FaHeartbeat className="inline mr-1" />Komorbiditeti:</label>
          <select
            value={komorbiditet}
            onChange={(e) => setKomorbiditet(e.target.value)}
            className="mt-1 p-2 border rounded w-full"
            disabled={ucitavanjeDijagnoza}
          >
            <option value="">{ucitavanjeDijagnoza ? "Učitavanje..." : "Odaberi komorbiditet"}</option>
            {dijagnozeLista
              .filter((d) => d !== dijagnoza)
              .map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
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

            <div className="overflow-y-auto max-h-80 text-gray-800">
              {greska && (
                <div className="text-red-600 mb-3">{greska}</div>
              )}

              {/* Ako imamo realan JSON → prikaži lepo formatirano */}
              {preporukaJson ? (
                <div className="space-y-3">
                  <div>
                    <div className="font-semibold">Dijagnoza</div>
                    <div>{preporukaJson.bolest}</div>
                  </div>

                  <div>
                    <div className="font-semibold">Biljke</div>
                    {preporukaJson.biljke?.length ? (
                      <ul className="list-disc list-inside">
                        {preporukaJson.biljke.map((b, i) => <li key={i}>{b}</li>)}
                      </ul>
                    ) : (
                      <div className="text-sm text-gray-500">(nema)</div>
                    )}
                  </div>

                  <div>
                    <div className="font-semibold">Suplementi</div>
                    {preporukaJson.suplementi?.length ? (
                      <ul className="list-disc list-inside">
                        {preporukaJson.suplementi.map((s, i) => <li key={i}>{s}</li>)}
                      </ul>
                    ) : (
                      <div className="text-sm text-gray-500">(nema)</div>
                    )}
                  </div>

                  <div>
                    <div className="font-semibold">Literatura</div>
                    {preporukaJson.literatura?.length ? (
                      <ul className="list-disc list-inside">
                        {preporukaJson.literatura.map((l, i) => <li key={i}>{l}</li>)}
                      </ul>
                    ) : (
                      <div className="text-sm text-gray-500">(nema)</div>
                    )}
                  </div>

                  {preporukaJson.napomena && (
                    <div>
                      <div className="font-semibold">Napomena</div>
                      <p className="whitespace-pre-line">{preporukaJson.napomena}</p>
                    </div>
                  )}
                </div>
              ) : (
                // Placeholder samo kada nemamo realnu preporuku
                <p className="whitespace-pre-line text-gray-700">
                  Sistem je u fazi provere funkcionalnosti. Vaši podaci su uspešno obrađeni.
                  Uskoro će biti dostupne personalizovane preporuke koje uključuju biljke, suplemente,
                  ishranu i druge savete. Ova poruka je informativna i ne predstavlja medicinski savet.
                </p>
              )}
            </div>

            <div className="mt-6 flex flex-wrap gap-2 justify-between">
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
              <div className="mt-4 text-center text-red-600 font-semibold">{poruka}</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Analiza;
