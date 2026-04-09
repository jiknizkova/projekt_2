import pytest
from unittest.mock import patch
import mysql.connector
from projekt2 import pridat_ukol

# priprava dat
@pytest.fixture(scope="function")
def db_spojeni():
    # Připojíme se do skutečné databáze
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="1111", database="sys")
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS test_projekt2_db")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_manager (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100),
                popis VARCHAR(200),
                stav ENUM('nezahajeno', 'probiha', 'hotovo'),
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
                   ''')
    conn.commit()
    yield conn, cursor 
    


# pozitivní test funkce pridat_ukol
@patch('builtins.input', side_effect=["TEST_UKOL", "Toto je testovací popis"])
def test_pridat_ukol_pozitivni(mock_input, db_spojeni):
    conn, cursor = db_spojeni
    
    # Zjistíme, kolik záznamů je v databázi již uloženo.
    cursor.execute("SELECT nazev, popis FROM task_manager WHERE nazev = 'TEST_UKOL'")
    pocet_pred = cursor.fetchall

    pridat_ukol(conn, cursor) 
    
    # Zjistíme, kolik záznamů je v databázi nyní
    cursor.execute("SELECT nazev, popis FROM task_manager WHERE nazev = 'TEST_UKOL'")
    pocet_po = cursor.fetchall()
    
    # ověření
    vysledek = pocet_po - pocet_pred
    assert len(vysledek) == 1  





    # úklid
    cursor.execute("DROP DATABASE test_projekt2_db")
    conn.commit()
    cursor.close()
    conn.close()
