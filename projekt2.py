import mysql.connector

# pripojeni k databazi a ověření připojení
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1111",
            database="sys"
        )
        print("připojení úspěšné")
        return conn
    except mysql.connector.Error as err:
        print (f"chyba při připojování: {err}")
        return None
    
# vytvoreni tabulky
def vytvor_tabulku(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_manager (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100),
                popis VARCHAR(200),
                stav ENUM('nezahajeno', 'probiha', 'hotovo'),
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Tabulka 'testovaci_tabulka' byla vytvořena.")
    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")

# funkce zobrazení hlavního menu
def hlavni_menu():
    print("1. přidat úkol")
    print("2. Zobrazit úkoly")
    print("3. Aktualizovat úkol")
    print("4. Odstranit úkol")
    print("5. Ukončit program")

# funkce zadani noveho ukolu
def pridat_ukol(conn, cursor):
    try:
        # Zajištění, že název nebude prázdný
        while True:
            nazev_ukolu = input("Zadejte název úkolu: ").strip()
            if nazev_ukolu:
                break
            print("Název úkolu nesmí být prázdný!")

        # Zajištění, že popis nebude prázdný
        while True:
            popis_ukolu = input("Zadejte popis úkolu: ").strip()
            if popis_ukolu:
                break
            print("Popis úkolu nesmí být prázdný!")

        stav_ukolu = "nezahajeno"

        sql=("INSERT INTO task_manager (nazev, popis, stav) VALUES (%s, %s, %s)")
        hodnoty= (nazev_ukolu, popis_ukolu, stav_ukolu)        
        cursor.execute(sql, hodnoty)
        conn.commit()
        print("Úkol byl vložen.")

    except mysql.connector.Error as err:
        print(f"Chyba při vkládání úkolu: {err}")

# funkce zobrazení úkolů
def zobrazit_ukoly(cursor): # Zadání navíc píše zobrazit_ukoly (množné číslo)
    try:
        cursor.execute("SELECT * FROM ukoly WHERE stav = 'nezahajeno' OR stav = 'probiha'")
        seznam = cursor.fetchall()
        
        if not seznam:
            print("Seznam úkolů je momentálně prázdný.")
        else:
            for row in seznam:
                print(row)
    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")

#  funkce aktualizace úkolu
def aktualizovat_ukol(conn, cursor):
    zobrazit_ukoly(cursor)
    while True:
        vybrany_ukol = input("Vložte ID úkolu (číslo v prvním sloupci), který chcete aktualizovat a stiskněte enter: ")

        if not vybrany_ukol.isdigit():
            print("ID musí být číslo, zkuste to znovu.")
            continue
        
        while True:
            novy_stav = input("Vložte nový stav úkolu (probiha/hotovo): ").strip().lower()
            if novy_stav in ['probiha', 'hotovo']:
                break
            print("Neplatný stav! Zadejte pouze 'probiha' nebo 'hotovo'.")

        try:
            sql_aktualizace=("UPDATE task_manager SET stav = %s WHERE id = %s")
            hodnoty_aktualizace=(novy_stav, vybrany_ukol)
            cursor.execute(sql_aktualizace, hodnoty_aktualizace)
            conn.commit()

            # kontrolam jestli se změnil nějaký řádek
            if cursor.rowcount > 0:
                print(f"Úkol {vybrany_ukol} byl aktualizován.")
                break
            else:
                print(f"Úkol s ID {vybrany_ukol} neexistuje. Zkuste to znovu. ")

        except mysql.connector.Error as err:
            print(f"Chyba při aktualizaci úkolu: {err}")


# funkce odstranění úkolu:
def odstranit_ukol(conn, cursor):
    zobrazit_ukoly(cursor)
    while True:
        ukol_k_odstraneni = input("Vložte ID úkolu (číslo v prvním sloupci), který chcete smazat a stiskněte enter: ")


        if not ukol_k_odstraneni.isdigit():
            print("ID musí být číslo, zkuste to znovu.")
            continue

        try:
            # převedení input hodnoty do dict
            hodnoty_k_odstraneni = (ukol_k_odstraneni, )
            sql_odstraneni=("DELETE FROM task_manager WHERE id = %s")
            cursor.execute(sql_odstraneni, hodnoty_k_odstraneni)
            conn.commit()

            # kontrolam jestli se změnil nějaký řádek
            if cursor.rowcount > 0:
                print(f"Úkol {ukol_k_odstraneni} byl odstraněn.")
                break
            else:
                print(f"Úkol s ID {ukol_k_odstraneni} neexistuje. Zkuste to znovu. ")

        except mysql.connector.Error as err:
            print(f"Chyba při odstranění úkolu: {err}")

        

# vytvoření kurzoru
conn = pripojeni_db()
if conn is not None:
    cursor = conn.cursor()



#akce
vytvor_tabulku(cursor)

while True:
    hlavni_menu()
    akce_uzivatele = input ("Vyberte číslo od 1 do 5. ")
    print()

    if akce_uzivatele == "1":
        pridat_ukol(conn, cursor)

    elif akce_uzivatele == "2":
        zobrazit_ukoly(cursor)
       
    elif akce_uzivatele == "3":
        aktualizovat_ukol(conn, cursor)

    elif akce_uzivatele == "4":
        odstranit_ukol(conn, cursor)

    elif akce_uzivatele == "5":
        print("Program ukončen. ")
        cursor.close()
        conn.close()
        break

    else:
        print("Ajaj, zadali jste neplatnou volbu, zkuste to znovu.")


