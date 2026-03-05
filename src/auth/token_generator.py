# src/auth/token_generator.py
"""
Modul de generare si verificare a token-urilor JWT (JSON Web Tokens).

Token-urile JWT sunt utilizate pentru autentificarea fara stare (stateless)
a cererilor HTTP dupa autentificarea initiala cu username si parola.
"""

import jwt
import datetime


# Cheia secreta utilizata pentru semnarea token-urilor
# NOTA: Intr-o aplicatie reala, aceasta ar fi stocata in variabile de mediu,
# nu direct in codul sursa.
SECRET_KEY = "cheie_secreta_demo_utm_2026"
ALGORITHM = "HS256"


def generate_token(user_id: str, expiry_hours: int = 24) -> str:
    """
    Genereaza un token JWT semnat pentru utilizatorul specificat.

    Args:
        user_id (str):       Identificatorul unic al utilizatorului autentificat.
        expiry_hours (int):  Numarul de ore pana la expirarea token-ului (implicit 24).

    Returns:
        str: Token-ul JWT semnat, encodat in format Base64URL.
    """
    payload = {
        "sub": user_id,                  # Subject: identificatorul utilizatorului
        "iat": datetime.datetime.utcnow(),  # Issued At: momentul emiterii
        "exp": datetime.datetime.utcnow()  # Expiration: momentul expirarii
              + datetime.timedelta(hours=expiry_hours),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Verifica si decodifica un token JWT.

    Args:
        token (str): Token-ul JWT de verificat.

    Returns:
        dict: Payload-ul decodat ca dictionar Python.

    Raises:
        jwt.ExpiredSignatureError: Daca token-ul a expirat.
        jwt.InvalidTokenError:     Daca semnatura sau structura sunt invalide.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])