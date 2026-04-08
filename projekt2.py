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
        nazev_ukolu= input("Zadejte název úkolu: ")
        popis_ukolu= input("Zadejte popis úkolu: ")
        stav_ukolu = "nezahajeno"

        sql=("INSERT INTO task_manager (nazev, popis, stav) VALUES (%s, %s, %s)")
        hodnoty= (nazev_ukolu, popis_ukolu, stav_ukolu)        
        cursor.execute(sql, hodnoty)
        conn.commit()
        print("Úkol byl vložen.")

    except mysql.connector.Error as err:
        print(f"Chyba při vkládání úkolu: {err}")

# funkce zobrazení úkolů
def zobrazit_ukol(cursor):
    try:
        cursor.execute("SELECT * FROM task_manager WHERE stav = 'nezahajeno' or stav = 'probiha'")
        for row in cursor.fetchall():
            print(row)
    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")

#  funkce aktualizace úkolu
def aktualizovat_ukol(conn, cursor):
    zobrazit_ukol(cursor)
    # zadaní dat od uživatele
    vybrany_ukol = input("Vložte ID úkolu (číslo v prvním sloupci), který chcete aktualizovat a stiskněte enter: ")
    novy_stav = input("Vložte aktuální stav úkolu - probiha/hotovo: ")
    # podmínka platného id:
    while True:
        #uložení dat do tabulky (resp. změna starýhch)
        try:
            sql_aktualizace=("UPDATE task_manager SET stav = %s WHERE id = %s")
            hodnoty_aktualizace=(novy_stav, vybrany_ukol)
            conn.commit()
            print(f"Úkol {vybrany_ukol} byl aktualizován.")
        except mysql.connector.Error as err:
            print(f"Chyba při aktualizaci úkolu: {err}")
    

# vytvoření kurzoru
conn = pripojeni_db()
if conn is not None:
    cursor = conn.cursor()


pripojeni_db()
vytvor_tabulku(cursor)
pridat_ukol(conn, cursor)
zobrazit_ukol(cursor)
aktualizovat_ukol(conn, cursor)


