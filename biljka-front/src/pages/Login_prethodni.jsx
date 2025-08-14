// crs/pages/Analiza.jsx
import React, { useState } from "react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import { Navigate, useNavigate } from "react-router-dom";
//import axios from "axios";
import api from '../api/api';

export default function Analiza() {
  const navigate = useNavigate();

  // 1️⃣ AUTORIZACIJA
  const token = localStorage.getItem("jwtToken");
  if (!token) {
    return <Navigate to="/login" />;
  }

  // 2️⃣ STANJE
  const korisnik = JSON.parse(localStorage.getItem("biljnaUser"));
  const [godine, setGodine] = useState("");
  const [pol, setPol] = useState("");
  const [trudnoca, setTrudnoca] = useState("");
  const [uloga, setUloga] = useState(korisnik?.uloga || "");
  const [statusi, setStatusi] = useState({});
  const [dijagnoza, setDijagnoza] = useState("");
  const [komorbiditeti, setKomorbiditeti] = useState([]);
  const [alergije, setAlergije] = useState([]);
  const [loading, setLoading] = useState(false);

  // 3️⃣ POMOĆNA FUNKCIJA
  const grupisiStatus = (grupa) =>
    Object.entries(statusi)
      .filter(([k]) => k.startsWith(grupa))
      .map(([, v]) => v)
      .join(", ");

  // 4️⃣ SLANJE PODATAKA
  const handleSubmit = async () => {
  setLoading(true); // 🔄 Pokreće indikator slanja

  const podaci = {
    pol,
    trudnoca: pol === "Ženski" && trudnoca === "Da",
    starost: godine ? parseInt(godine, 10) : null,
    dijagnoza,
    komorbiditeti: komorbiditeti.join(", "),
    alergije: alergije.join(", "),
    fizioloski_status: grupisiStatus("Fizioloski"),
    nutritivni_status: grupisiStatus("Nutritivni"),
    psiholoski_faktori: grupisiStatus("Psiholoski"),
    zivotni_stil: grupisiStatus("Ponasanje"),
    genetski_faktori: grupisiStatus("Genetski"),
    okruzenje: grupisiStatus("Okruženje"),
  };

  console.log("handleSubmit -> podaci:", JSON.stringify(podaci, null, 2));
  console.log("JWT token koji se šalje:", token);

  try {
    const res = await api.post("/analiza/create", podaci, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    alert("Podaci uspešno poslati.");
    console.log("Server odgovor:", res.data);

    // navigate("/rezultat"); // ako budeš pravio stranicu sa rezultatima
  } catch (err) {
    console.error("Greška:", err.response?.data || err.message);
    alert("Greška pri slanju podataka na server.");
  } finally {
    setLoading(false); // ✅ Bez obzira na ishod, loader se gasi
  }
};


  // 5️⃣ HELPER ZA SELECT STATUS
  const SelectGrupa = ({ grupa, naziv }) => (
    <div className="my-2 bg-green-50 p-2 rounded-md">
      <label className="block text-sm font-medium mb-1 text-gray-700">
        {naziv}
      </label>
      <Select
        value={statusi[`${grupa} - ${naziv}`] || ""}
        onValueChange={(v) =>
          setStatusi((prev) => ({ ...prev, [`${grupa} - ${naziv}`]: v }))
        }
      >
        <SelectTrigger className="w-full max-w-xs bg-green-50">
          <SelectValue placeholder="Odaberi status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="Dobar">Dobar</SelectItem>
          <SelectItem value="Srednji">Srednji</SelectItem>
          <SelectItem value="Loš">Loš</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );

  // 6️⃣ RENDER
  return (
    <div className="p-4 max-w-screen-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">Analiza pacijenta</h1>

      {korisnik && (
        <div className="mb-4 text-green-800 font-medium">
          Dobrodošao, {korisnik.ime}! (Uloga: {uloga || "Nepoznata"})
        </div>
      )}

      {/* OSNOVNI PODACI */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Godine */}
        <div className="mb-4 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium">Godine:</label>
          <input
            type="number"
            value={godine}
            onChange={(e) => setGodine(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 w-full bg-green-50"
          />
        </div>

        {/* Pol */}
        <div className="mb-4 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium">Pol:</label>
          <select
            value={pol}
            onChange={(e) => setPol(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 w-full bg-green-50"
          >
            <option value="">Odaberi</option>
            <option value="Muški">Muški</option>
            <option value="Ženski">Ženski</option>
          </select>
        </div>

        {/* Trudnoća */}
        {pol === "Ženski" && (
          <div className="mb-4 bg-green-50 p-3 rounded-md">
            <label
              htmlFor="trudnoca"
              className="block text-sm font-medium text-gray-700"
            >
              Trudnoća
            </label>
            <select
              id="trudnoca"
              name="trudnoca"
              value={trudnoca}
              onChange={(e) => setTrudnoca(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm"
            >
              <option value="">Odaberi</option>
              <option value="Da">Da</option>
              <option value="Ne">Ne</option>
            </select>
          </div>
        )}

        {/* Dijagnoza */}
        <div className="mb-4 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Dijagnoza
          </label>
          <Select value={dijagnoza} onValueChange={setDijagnoza}>
            <SelectTrigger className="w-full bg-white border border-gray-300 px-3 py-2 rounded">
              <SelectValue placeholder="Odaberi dijagnozu" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Hipertenzija">Hipertenzija</SelectItem>
              <SelectItem value="Dijabetes tip 2">Dijabetes tip 2</SelectItem>
              <SelectItem value="Reumatoidni artritis">Reumatoidni artritis</SelectItem>
              <SelectItem value="Astma">Astma</SelectItem>
              <SelectItem value="Depresija">Depresija</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Komorbiditeti */}
        <div className="mb-4 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Komorbiditeti (ako ih ima):
          </label>
          <div className="border border-gray-300 rounded px-3 py-2 bg-white max-h-48 overflow-y-auto">
            {[
              "Dijabetes tip 2",
              "Hipertenzija",
              "Astma",
              "Osteoporoza",
              "Hronična bubrežna bolest",
              "Depresija",
            ].map((kom) => (
              <label key={kom} className="flex items-center space-x-2 mb-1">
                <input
                  type="checkbox"
                  value={kom}
                  checked={komorbiditeti.includes(kom)}
                  onChange={(e) => {
                    const value = e.target.value;
                    setKomorbiditeti((prev) =>
                      prev.includes(value)
                        ? prev.filter((v) => v !== value)
                        : [...prev, value]
                    );
                  }}
                />
                <span>{kom}</span>
              </label>
            ))}
          </div>
        </div>


        {/* Alergije */}
        <div className="mb-4 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Poznate alergije (ako ih ima):
          </label>
          <div className="border border-gray-300 rounded px-3 py-2 bg-white max-h-48 overflow-y-auto">
            {[
              "Polen",
              "Praškovi i deterdženti",
              "Penicilin",
              "Jaja",
              "Riba i plodovi mora",
              "Orašasti plodovi",
              "Lateks",
              "Ubodi insekata",
            ].map((alergija) => (
              <label key={alergija} className="flex items-center space-x-2 mb-1">
                <input
                  type="checkbox"
                  value={alergija}
                  checked={alergije.includes(alergija)}
                  onChange={(e) => {
                    const value = e.target.value;
                    setAlergije((prev) =>
                      prev.includes(value)
                        ? prev.filter((v) => v !== value)
                        : [...prev, value]
                    );
                  }}
                />
                <span>{alergija}</span>
              </label>
            ))}
          </div>
        </div>


        {/* Uloga */}
        <div className="mb-6 bg-green-50 p-3 rounded-md">
          <label className="block text-sm font-medium">Vaša uloga:</label>
          <select
            value={uloga}
            onChange={(e) => setUloga(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 w-full bg-green-50"
          >
            <option value="">Odaberi</option>
            <option value="Korisnik">Korisnik</option>
            <option value="Lekar">Lekar</option>
            <option value="Admin">Admin</option>
          </select>
        </div>
      </div>

      {/* STATUSI */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Leva kolona */}
        <div className="space-y-4">
          <Accordion type="multiple">
            <AccordionItem value="fizioloski">
              <AccordionTrigger className="text-lg">
                Fiziološki status
              </AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Fizioloski" naziv="Procena vitalnih funkcija" />
                <SelectGrupa grupa="Fizioloski" naziv="Akutna i hronična stanja" />
                <SelectGrupa grupa="Fizioloski" naziv="Laboratorijske analize" />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="nutritivni">
              <AccordionTrigger className="text-lg">
                Nutritivni status
              </AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Nutritivni" naziv="Unos makronutrijenata" />
                <SelectGrupa grupa="Nutritivni" naziv="Unos mikronutrijenata" />
                <SelectGrupa grupa="Nutritivni" naziv="Digestivno zdravlje" />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="psiholoski">
              <AccordionTrigger className="text-lg">
                Psihološki status
              </AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Psiholoski" naziv="Stres i anksioznost" />
                <SelectGrupa grupa="Psiholoski" naziv="Emocionalna stabilnost" />
                <SelectGrupa grupa="Psiholoski" naziv="Kognitivna funkcija" />
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>

        {/* Desna kolona */}
        <div className="space-y-4">
          <Accordion type="multiple">
            <AccordionItem value="ponasanje">
              <AccordionTrigger className="text-lg">Ponašanje</AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Ponasanje" naziv="Fizička aktivnost" />
                <SelectGrupa grupa="Ponasanje" naziv="Navike spavanja" />
                <SelectGrupa grupa="Ponasanje" naziv="Zavisnosti i poroci" />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="genetski">
              <AccordionTrigger className="text-lg">
                Genetski status
              </AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Genetski" naziv="Porodična anamneza" />
                <SelectGrupa grupa="Genetski" naziv="Genetska predispozicija" />
                <SelectGrupa grupa="Genetski" naziv="Hronične bolesti u porodici" />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="okruzenje">
              <AccordionTrigger className="text-lg">Okruženje</AccordionTrigger>
              <AccordionContent>
                <SelectGrupa grupa="Okruženje" naziv="Zagađenje i toksini" />
                <SelectGrupa grupa="Okruženje" naziv="Uslovi stanovanja" />
                <SelectGrupa grupa="Okruženje" naziv="Socioekonomski faktori" />
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>

      {/* DUGME sa loader-om */}
<div className="mt-6">
        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
          disabled={loading}
        >
          {loading ? "Šaljem…" : "Pošalji"}
        </button>
      </div>

    </div> {/* kraj outer wrappera */}
  );
}

