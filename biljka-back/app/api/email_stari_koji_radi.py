# app/api/email.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.api.auth_routes import get_current_user
import smtplib
from email.message import EmailMessage
from datetime import datetime  # ⬅️ DODAJ OVO

router = APIRouter()


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    content: str  # Ovo može ostati kao backup plain text

# ✅ HTML šablon funkcija
def kreiraj_html_email(preporuka: str) -> str:
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #006400;">Vaša biljna terapijska preporuka</h2>

        <p>Poštovani korisniče,</p>

        <p>Hvala što koristite aplikaciju <strong>Biljna Terapija</strong>. Na osnovu unetih podataka, 
        pripremili smo za Vas preporučenu terapiju:</p>

        <hr style="border: 0; height: 1px; background-color: #ccc;">

        <h3 style="color: #2E8B57;">🌿 Preporučene biljke i suplementi:</h3>
        <p>{preporuka}</p>

        <h3 style="color: #2E8B57;">📚 Reference i izvori:</h3>
        <p><em>Ova sekcija će sadržati stručne izvore, naučne radove i linkove kada budu dostupni.</em></p>

        <h3 style="color: #2E8B57;">🔗 Korisni linkovi:</h3>
        <ul>
          <li><a href="https://tvojadomena.com/profil" target="_blank">Vaš profil</a></li>
          <li><a href="https://tvojadomena.com/analiza" target="_blank">Pregled analiza</a></li>
        </ul>

        <p style="font-size: 0.9em; color: #666;">
          Ako imate pitanja, kontaktirajte nas putem <a href="mailto:podrska@tvojadomena.com">podrške</a>.
        </p>

        <hr style="border: 0; height: 1px; background-color: #ccc;">
        <p style="font-size: 0.8em; color: #999;">© 2025 Biljna Terapija. Sva prava zadržana.</p>
      </body>
    </html>
    """

@router.post("/email/send")
def send_email(data: EmailSchema, user=Depends(get_current_user)):
    try:
        msg = EmailMessage()
        msg["From"] = "tvoj_email@gmail.com"
        msg["To"] = data.email
        msg["Subject"] = f"Vaša biljna terapija - {datetime.now().strftime('%H:%M:%S')}"

        # Plain text fallback
        #msg.set_content(data.content)

        # HTML verzija
        html_content = kreiraj_html_email(data.content)
        msg.add_alternative(html_content, subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("fudra07@gmail.com", "pgsaylgnkzqscsdj")
            smtp.send_message(msg)

        return {"message": "Email uspešno poslat." }

    except Exception as e:
        print("❌ Email greška:", str(e))
        raise HTTPException(status_code=500, detail="Slanje emaila nije uspelo.")







#15.7.2025  Generisana lozinka za aplikaciju BiljnaTerapija. 
#EVO Je: pgsa ylgn kzqs csdj