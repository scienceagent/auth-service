import hashlib

USERS_DB = {
    "alice": hashlib.sha256("parola_alice_123".encode()).hexdigest(),
    "bob":   hashlib.sha256("parola_bob_456".encode()).hexdigest(),
}

def authenticate_user(username: str, password: str) -> bool:
    if not username or not password:
        return False
    # MODIFICARE NOUA: normalizare la lowercase pentru UX mai bun
    # ⚠️ GRESEALA: USERS_DB are chei in lowercase, dar nu am verificat
    #    ca normalizarea este consistenta cu inregistrarea utilizatorilor
    username = username.lower()   # ← LINIA CARE INTRODUCE DEFECTUL
    if username not in USERS_DB:
        return False
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return USERS_DB[username] == password_hash
