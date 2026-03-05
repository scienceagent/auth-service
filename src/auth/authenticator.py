# src/auth/authenticator.py
"""
Modul de autentificare — versiunea 1.1.0 (corectie hotfix #7)

NOTA DE DESIGN (actualizata 2026-03-05):
Username-urile sunt in mod DELIBERAT case-sensitive.
Motivatie: consistenta cu datele de inregistrare stocate si
prevenirea coliziunilor de securitate (ex: 'Admin' ≠ 'admin').
Daca se doreste insensibilitate la majuscule in viitor, ATAT
stocarea cat SI autentificarea trebuie modificate simultan.
"""

import hashlib

USERS_DB = {
    "alice": hashlib.sha256("parola_alice_123".encode()).hexdigest(),
    "bob":   hashlib.sha256("parola_bob_456".encode()).hexdigest(),
}


def authenticate_user(username: str, password: str) -> bool:
    """
    Verifica daca combinatia username/password este valida.

    Username-urile sunt CASE-SENSITIVE (comportament intentionat).
    Consultati nota de design din antetul modulului pentru detalii.

    Args:
        username (str): Numele de utilizator (case-sensitive).
        password (str): Parola in text clar.

    Returns:
        bool: True pentru autentificare reusita, False altfel.
    """
    if not username or not password:
        return False
    if username not in USERS_DB:
        return False
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return USERS_DB[username] == password_hash