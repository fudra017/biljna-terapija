import requests

# URL tvoje login rute (lokalni server)
url = "http://127.0.0.1:8000/api/auth/login"

# Login podaci – koristi podatke iz baze
data = {
    "username": "fudra07@gmail.com",
    "password": "ledra123"
}

# Headers za form-url-encoded
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Pošalji zahtev
response = requests.post(url, data=data, headers=headers)

# Prikaži ceo odgovor
print("📥 Status:", response.status_code)
print("📦 Raw JSON:", response.text)

# Ako uspešno, parsiraj kao JSON i prikaži detaljno
if response.status_code == 200:
    try:
        json_data = response.json()
        print("\n🔍 access_token:", json_data.get("access_token"))
        print("🔍 token_type:", json_data.get("token_type"))
        print("👤 user:", json_data.get("user"))
    except Exception as e:
        print("❌ JSON parse error:", e)
