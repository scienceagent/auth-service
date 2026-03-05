# src/auth/authenticator.py
"""
Modul de autentificare pentru serviciul de gestionare a utilizatorilor.

Acest modul ofera functionalitate de verificare a credentialelor utilizatorilor
prin compararea parolelor hash-uite stocate cu cele furnizate la autentificare.
"""

import hashlib


# Simularea bazei de date a utilizatorilor
# NOTA: Intr-o aplicatie reala, aceasta ar fi o baza de date externa (PostgreSQL, MySQL etc.)
# Parolele sunt stocate EXCLUSIV ca hash-uri SHA-256, niciodata in text clar.
USERS_DB = {
    "alice": hashlib.sha256("parola_alice_123".encode()).hexdigest(),
    "bob":   hashlib.sha256("parola_bob_456".encode()).hexdigest(),
}


def authenticate_user(username: str, password: str) -> bool:
    """
    Verifica daca combinatia username/password este valida.

    Functia calculeaza hash-ul SHA-256 al parolei furnizate si il compara
    cu hash-ul stocat in baza de date. Username-urile sunt case-sensitive.

    Args:
        username (str): Numele de utilizator.
        password (str): Parola in text clar furnizata de utilizator.

    Returns:
        bool: True daca autentificarea reuseste, False in orice alt caz.

    Examples:
        >>> authenticate_user("alice", "parola_alice_123")
        True
        >>> authenticate_user("alice", "parola_gresita")
        False
    """
    # Validare: campuri goale sunt respinse imediat
    if not username or not password:
        return False

    # Verificarea existentei utilizatorului in baza de date
    if username not in USERS_DB:
        return False

    # Calcularea hash-ului parolei furnizate si compararea cu cel stocat
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return USERS_DB[username] == password_hash