import sqlite3

#conectare
conn = sqlite3.connect('cabinet_medical.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacienti (
        id INTEGER PRIMARY KEY,
        nume TEXT,
        prenume TEXT,
        data_nasterii DATE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS retete (
        id INTEGER PRIMARY KEY,
        serie TEXT,
        nr INTEGER,
        data_emitere DATE,
        pacient_id INTEGER,
        FOREIGN KEY (pacient_id) REFERENCES pacienti(id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicamente (
        id INTEGER PRIMARY KEY,
        denumire TEXT,
        cantitate_prescrisa INTEGER,
        dozaj TEXT,
        reteta_id INTEGER,
        FOREIGN KEY (reteta_id) REFERENCES retete(id)
    )
''')


conn.commit()

## cursor.execute("INSERT INTO pacienti (nume, prenume, data_nasterii) VALUES (?, ?, ?)",
##                ("Popescu", "Ion", "1990-01-01"))

## cursor.execute("INSERT INTO retete (serie, nr, data_emitere) VALUES (?, ?, ?)",
##                ("NPHGDV", 4387, "2023-10-25"))

## reteta_id = cursor.lastrowid

## cursor.execute("INSERT INTO medicamente (denumire, cantitate_prescrisa, dozaj, reteta_id) VALUES (?, ?, ?, ?)",
##                ("Paracetamol", 20, "2 capsule/zi", reteta_id))
## cursor.execute("INSERT INTO medicamente (denumire, cantitate_prescrisa, dozaj, reteta_id) VALUES (?, ?, ?, ?)",
##                ("Ibuprofen", 30, "1 comprimat/zi", reteta_id))


conn.commit()


conn.close()
