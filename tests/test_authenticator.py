# tests/test_authenticator.py
"""
Suita de teste unitare pentru modulul src.auth.authenticator.

Fiecare metoda de test verifica un singur comportament specific al functiei
authenticate_user(), respectand principiul unui singur assert per test.
"""

import pytest
from src.auth.authenticator import authenticate_user


class TestAuthenticateUserCazuriValide:
    """
    Grupul de teste pentru scenariile de autentificare reusita.
    Aceste teste verifica ca functia returneaza True pentru credentiale corecte.
    """

    def test_autentificare_alice_credentiale_corecte(self):
        """Autentificarea utilizatorului 'alice' cu parola corecta trebuie sa reuseasca."""
        rezultat = authenticate_user("alice", "parola_alice_123")
        assert rezultat is True, \
            "Autentificarea cu credentiale valide trebuie sa returneze True"

    def test_autentificare_bob_credentiale_corecte(self):
        """Autentificarea utilizatorului 'bob' cu parola corecta trebuie sa reuseasca."""
        rezultat = authenticate_user("bob", "parola_bob_456")
        assert rezultat is True, \
            "Autentificarea utilizatorului 'bob' cu credentiale valide trebuie sa reuseasca"


class TestAuthenticateUserCazuriInvalide:
    """
    Grupul de teste pentru scenariile de autentificare esuata.
    Aceste teste verifica ca functia returneaza False pentru orice credentiale incorecte.
    """

    def test_parola_incorecta_returneaza_false(self):
        """Parola gresita pentru un utilizator existent trebuie sa fie respinsa."""
        rezultat = authenticate_user("alice", "parola_gresita_complet")
        assert rezultat is False

    def test_utilizator_inexistent_returneaza_false(self):
        """Un utilizator care nu exista in sistem trebuie sa fie respins."""
        rezultat = authenticate_user("charlie", "orice_parola")
        assert rezultat is False

    def test_username_gol_returneaza_false(self):
        """Un username gol trebuie sa fie respins fara eroare."""
        rezultat = authenticate_user("", "parola_alice_123")
        assert rezultat is False

    def test_parola_goala_returneaza_false(self):
        """O parola goala trebuie sa fie respinsa fara eroare."""
        rezultat = authenticate_user("alice", "")
        assert rezultat is False

    def test_username_cu_majuscule_returneaza_false(self):
        """
        Username-urile sunt case-sensitive.
        'Alice' (cu A mare) ≠ 'alice' (cu a mic) — trebuie respins.
        """
        rezultat = authenticate_user("Alice", "parola_alice_123")
        assert rezultat is False

    def test_ambele_campuri_goale_returneaza_false(self):
        """Ambele campuri goale simultan trebuie sa fie respinse."""
        rezultat = authenticate_user("", "")
        assert rezultat is False

    def test_parola_corecta_utilizator_gresit(self):
        """Parola corecta a lui Alice nu trebuie sa functioneze pentru Bob."""
        rezultat = authenticate_user("bob", "parola_alice_123")
        assert rezultat is False