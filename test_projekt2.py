import pytest
from unittest.mock import patch
import mysql.connector
from projekt2 import pridat_ukol, aktualizovat_ukol, odstranit_ukol

# priprava dat
@pytest.fixture(scope="function")
def db_spojeni():
    # Připojíme se do skutečné databáze
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="1111")
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS test_projekt2_db")
    cursor.execute("USE test_projekt2_db")
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

    # předání databáze testům
    yield conn, cursor 

    # úklid po testech
    cursor.execute("DROP DATABASE test_projekt2_db")
    conn.commit()
    cursor.close()
    conn.close()
    


# pozitivní test funkce pridat_ukol
@patch('builtins.input', side_effect=["TEST_UKOL_1", "Toto je testovaci popis"])
def test_pridat_ukol_pozitivni(mock_input, db_spojeni):
    conn, cursor = db_spojeni

    pridat_ukol(conn, cursor) 
    
    cursor.execute("SELECT nazev, popis, stav FROM task_manager WHERE nazev = 'TEST_UKOL_1'")
    vysledek =  cursor.fetchone()
    
    # ověření, že se něco uložilo do tabulky
    assert vysledek is not None; f"Měl tam být náš úkol, ale je to prázdné."
    
    #ověření, zda se tam uložily námi zadané hodnoty a zda stav je nezahajeno
    assert vysledek[0] == "TEST_UKOL_1"
    assert vysledek[1] == "Toto je testovaci popis"
    assert vysledek[2] == "nezahajeno"



# negativní test funkce pridat_ukol - zkusíme zadat prázdný vstup
@patch('builtins.input', side_effect=["", "test_ukol_spravny", "", "test popis spravny"])
def test_pridat_ukol_negativni(mock_input, db_spojeni):
    conn, cursor = db_spojeni

    pridat_ukol(conn, cursor) 
    
    cursor.execute("SELECT nazev, popis, stav FROM task_manager WHERE nazev = 'test_ukol_spravny'")
    vysledek =  cursor.fetchone()

    assert vysledek is not None
    
    # ověření, že prázdné vstupy se do tabulky neuložily,
    # takže výsledky v prvním řádku jsou test_ukol_spravny a 
    # test popis spravny
    assert vysledek[0] == "test_ukol_spravny"
    assert vysledek[1] == "test popis spravny"
    assert vysledek[2] == "nezahajeno"


# poizitivní test pro funkci aktiualizovat_ukol
@patch('builtins.input', side_effect=["test_ukol_1", "test popis spravny", "1", "probiha"])
def test_aktualizovat_ukol_pozitivni(mock_input, db_spojeni):
    conn, cursor = db_spojeni
    pridat_ukol(conn, cursor) 

    aktualizovat_ukol(conn, cursor)

    cursor.execute("SELECT nazev, popis, stav FROM task_manager WHERE nazev = 'test_ukol_1'")
    vysledek =  cursor.fetchone()

    assert vysledek is not None
    assert vysledek[2] == "probiha"


# negativní test pro funkci aktualizovat ukol
@patch('builtins.input', side_effect=["test_ukol_1", "test popis spravny", "jedna", "1", "probiha"])
def test_aktualizovat_ukol_negativni(mock_input, db_spojeni):
    conn, cursor = db_spojeni
    pridat_ukol(conn, cursor) 

    aktualizovat_ukol(conn, cursor)

    cursor.execute("SELECT nazev, popis, stav FROM task_manager WHERE nazev = 'test_ukol_1'")
    vysledek =  cursor.fetchone()

    assert vysledek is not None
    assert vysledek[2] == "probiha"


# pozitivní test pro funkci odstranit ukol
@patch('builtins.input', side_effect=["vynest_kos", "at to tu nesmrdi!", "1"])
def test_odstranit_ukol_pozitivni(mock_input, db_spojeni):
    conn, cursor = db_spojeni
    pridat_ukol(conn, cursor) 

    odstranit_ukol(conn, cursor)

    cursor.execute("SELECT * FROM task_manager")
    vysledek = cursor.fetchone()

    assert vysledek is None, f"mělo to být prázdné, ale je tam {vysledek}"



# negativni test pro odstranit_ukol
@patch('builtins.input', side_effect=["vynest_kos", "at to tu nesmrdi!", "jedna", "1"])
def test_odstranit_ukol_negativni(mock_input, db_spojeni):
    conn, cursor = db_spojeni
    pridat_ukol(conn, cursor) 

    odstranit_ukol(conn, cursor)

    cursor.execute("SELECT * FROM task_manager")
    vysledek = cursor.fetchone()

    assert vysledek is None, f"mělo to být prázdné, ale je tam {vysledek}"
