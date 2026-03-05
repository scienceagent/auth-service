# tests/test_token_generator.py
"""
Suita de teste unitare pentru modulul src.auth.token_generator.

Testele acopera generarea, verificarea si expirarea token-urilor JWT,
inclusiv scenariile de eroare (token expirat, token falsificat).
"""

import pytest
import time
import jwt as pyjwt
from src.auth.token_generator import generate_token, verify_token


class TestGenerateToken:
    """Teste pentru functia generate_token()."""

    def test_returneaza_string_nenul(self):
        """Functia trebuie sa returneze un string non-gol."""
        token = generate_token("user_001")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_are_format_jwt_trei_segmente(self):
        """Un token JWT valid are exact 3 segmente separate prin punct."""
        token = generate_token("user_001")
        segmente = token.split(".")
        assert len(segmente) == 3, \
            f"JWT trebuie sa aiba 3 segmente, dar are {len(segmente)}"

    def test_payload_contine_user_id_corect(self):
        """Token-ul generat trebuie sa contina identificatorul utilizatorului."""
        token = generate_token("user_grigore_42")
        payload = verify_token(token)
        assert payload["sub"] == "user_grigore_42"

    def test_doi_utilizatori_diferiti_genereaza_tokeni_diferiti(self):
        """Token-uri pentru utilizatori diferiti trebuie sa fie distincte."""
        token_alice = generate_token("alice")
        token_bob   = generate_token("bob")
        assert token_alice != token_bob

    def test_expiry_hours_implicit_este_24(self):
        """Token-ul cu parametrii impliciti trebuie sa expire dupa ~24 de ore."""
        import datetime
        token = generate_token("user_001")
        payload = verify_token(token)
        exp_time = datetime.datetime.utcfromtimestamp(payload["exp"])
        iat_time = datetime.datetime.utcfromtimestamp(payload["iat"])
        diferenta_ore = (exp_time - iat_time).total_seconds() / 3600
        assert 23.9 < diferenta_ore < 24.1, \
            f"Expiarea asteptata ~24h, dar este {diferenta_ore:.2f}h"


class TestVerifyToken:
    """Teste pentru functia verify_token()."""

    def test_token_valid_returneaza_payload(self):
        """Verificarea unui token valid trebuie sa returneze payload-ul corect."""
        token = generate_token("user_test_99")
        payload = verify_token(token)
        assert payload["sub"] == "user_test_99"

    def test_token_expirat_ridica_exceptie(self):
        """
        Un token generat cu expiry_hours=0 expira imediat.
        Verificarea sa trebuie sa ridice ExpiredSignatureError.
        """
        token = generate_token("user_001", expiry_hours=0)
        time.sleep(1)  # Asteptam 1 secunda pentru a garanta expirarea
        with pytest.raises(pyjwt.ExpiredSignatureError):
            verify_token(token)

    def test_token_falsificat_ridica_exceptie(self):
        """Un string care nu este un JWT valid trebuie sa ridice InvalidTokenError."""
        token_fals = "acesta.nu.este.un.token.jwt.valid.deloc"
        with pytest.raises(pyjwt.exceptions.DecodeError):
            verify_token(token_fals)

    def test_token_modificat_ridica_exceptie(self):
        """Un token cu payload modificat manual trebuie respins (semnatura invalida)."""
        import base64, json
        token = generate_token("user_001")
        header, payload_b64, signature = token.split(".")

        # Decodificam payload-ul si modificam user_id
        padding = 4 - len(payload_b64) % 4
        payload_decoded = json.loads(
            base64.urlsafe_b64decode(payload_b64 + "=" * padding)
        )
        payload_decoded["sub"] = "UTILIZATOR_FALS_ADMIN"

        # Re-encodam payload-ul modificat
        payload_modified = base64.urlsafe_b64encode(
            json.dumps(payload_decoded).encode()
        ).rstrip(b"=").decode()

        token_manipulat = f"{header}.{payload_modified}.{signature}"

        with pytest.raises(pyjwt.InvalidSignatureError):
            verify_token(token_manipulat)