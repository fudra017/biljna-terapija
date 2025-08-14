# app/utils/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.settings import settings


def posalji_email(preporuka: str, primaoc_email: str):
    try:
        poruka = MIMEMultipart()
        poruka["From"] = settings.EMAIL_USER
        poruka["To"] = primaoc_email
        poruka["Subject"] = "Vaša biljna preporuka"

        telo = MIMEText(preporuka, "plain", "utf-8")
        poruka.attach(telo)

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, primaoc_email, poruka.as_string())
            print("📧 Email uspešno poslat korisniku:", primaoc_email)

    except Exception as e:
        print("❌ Greška prilikom slanja emaila:", e)
