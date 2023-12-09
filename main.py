import sqlite3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

conn = sqlite3.connect('cabinet_medical.db')

cursor = conn.cursor()

def afiseaza_pacienti():
    cursor.execute("SELECT * FROM pacienti")
    pacienti = cursor.fetchall()
    lista_pacienti.delete(0, tk.END)  
    for pacient in pacienti:
        lista_pacienti.insert(tk.END, f"{pacient[0]}. {pacient[1]} {pacient[2]}, Data nașterii: {pacient[3]}")

def adauga_pacient():
    nume = nume_entry.get()
    prenume = prenume_entry.get()
    data_nasterii = data_nasterii_calendar.get_date()

    if not nume or not prenume or not data_nasterii:
        messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
        return
    
    cursor.execute("INSERT INTO pacienti (nume, prenume, data_nasterii) VALUES (?, ?, ?)", (nume, prenume, data_nasterii))
    conn.commit()
    afiseaza_pacienti()
    messagebox.showinfo("Informație", "Pacient adăugat cu succes.")

def modifica_pacient():
    try:
        id_pacient = int(id_pacient_entry.get())
        nume = nume_entry.get()
        prenume = prenume_entry.get()
        data_nasterii = data_nasterii_calendar.get_date()

        if not id_pacient or not nume or not prenume or not data_nasterii:
            messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
            return

        cursor.execute("UPDATE pacienti SET nume=?, prenume=?, data_nasterii=? WHERE id=?",
                       (nume, prenume, data_nasterii, id_pacient))
        conn.commit()
        afiseaza_pacienti()
        messagebox.showinfo("Informație", "Pacient modificat cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare", f"ID invalid sau date introduse greșit.\nDetalii eroare: {e}")


def sterge_pacient():
    try:
        id_pacient = int(id_pacient_entry.get())
        cursor.execute("SELECT * FROM pacienti WHERE id=?", (id_pacient,))
        pacient = cursor.fetchone()
        if pacient is not None:
            cursor.execute("DELETE FROM pacienti WHERE id=?", (id_pacient,))
            conn.commit()
            afiseaza_pacienti()
            messagebox.showinfo("Informație", "Pacient șters cu succes.")
        else:
            messagebox.showwarning("Avertisment", "Nu există niciun pacient cu ID-ul specificat.")
    except Exception as e:
        messagebox.showerror("Eroare", f"A apărut o eroare.\nDetalii eroare: {e}")


def afiseaza_retete():
    cursor.execute("SELECT * FROM retete")
    retete = cursor.fetchall()
    lista_retete.delete(0, tk.END)  

    global id_retea_globala

    for reteta in retete:
        lista_retete.insert(tk.END, f"{reteta[0]}. Serie: {reteta[1]}, Număr: {reteta[2]}, Data emiterii: {reteta[3]}")
        cursor.execute("SELECT * FROM medicamente WHERE reteta_id=?", (reteta[0],))
        medicamente = cursor.fetchall()
        for medicament in medicamente:
            lista_retete.insert(tk.END, f"        Medicament: {medicament[1]}, Cantitate prescrisă: {medicament[2]}, Dozaj: {medicament[3]}")
        cursor.execute("SELECT pacienti.nume, pacienti.prenume "
                       "FROM pacienti "
                       "INNER JOIN retete ON pacienti.id = retete.pacient_id "
                       "WHERE retete.id=?", (reteta[0],))
        pacient = cursor.fetchone()
        if pacient is not None:
            lista_retete.insert(tk.END, f"    ID Pacient: {reteta[4]}, Nume Pacient: {pacient[0]}, Prenume Pacient: {pacient[1]}")
        else:
            lista_retete.insert(tk.END, f"    Pacientul nu a fost găsit.")


def adauga_reteta():
    serie = serie_entry.get()
    nr = nr_entry.get()
    data_emitere = data_emitere_calendar.get_date()
    id = identificare_pacient.get()

    if not serie or not nr or not data_emitere or not id:
        messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
        return


    cursor.execute("SELECT id FROM pacienti WHERE id=?", (id,))
    pacient = cursor.fetchone()

    if pacient is not None:
        cursor.execute("INSERT INTO retete (serie, nr, data_emitere ,pacient_id) VALUES (?, ?, ?, ?)", (serie, nr, data_emitere, id))
        conn.commit()

        cursor.execute("SELECT last_insert_rowid()")
        reteta_id = cursor.fetchone()[0]

        afiseaza_retete()
        messagebox.showinfo("Informație", "Rețetă adăugată cu succes.")
        return reteta_id
    else:
        messagebox.showerror("Eroare", "ID-ul pacientului nu există în baza de date.")



def adauga_medicament():
    denumire = denumire_medicament_entry.get()
    cantitate = cantitate_prescrisa_entry.get()
    dozaj = dozaj_entry.get()

    reteta_id = id_retea_globala

    if not denumire or not cantitate or not dozaj:
        messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
        return    

    cursor.execute("INSERT INTO medicamente (denumire, cantitate_prescrisa, dozaj, reteta_id) VALUES (?, ?, ?, ?)",
                   (denumire, cantitate, dozaj, reteta_id))
    conn.commit()
    afiseaza_retete()
    messagebox.showinfo("Informație", "Medicament adăugat cu succes.")


def modifica_reteta():
    try:
        id_reteta = int(id_reteta_entry.get())
        serie = serie_entry.get()
        nr = nr_entry.get()
        data_emitere = data_emitere_calendar.get_date()
        noul_id_pacient = int(identificare_pacient.get())

        if not id_reteta or not serie or not nr or not data_emitere or not noul_id_pacient:
            messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
            return

        cursor.execute("SELECT id FROM pacienti WHERE id=?", (noul_id_pacient,))
        pacient = cursor.fetchone()

        if pacient is not None:
            cursor.execute("UPDATE retete SET serie=?, nr=?, data_emitere=?, pacient_id=? WHERE id=?", (serie, nr, data_emitere, noul_id_pacient, id_reteta))
            conn.commit()

            cursor.execute("SELECT last_insert_rowid()")
            reteta_id = cursor.fetchone()[0]

            afiseaza_retete()
            messagebox.showinfo("Informație", "Rețetă modificată cu succes.")
        else:
            messagebox.showerror("Eroare", "ID-ul pacientului nu există în baza de date.")
    except Exception as e:
        messagebox.showerror("Eroare", f"ID invalid sau date introduse greșit.\nDetalii eroare: {e}")


def sterge_reteta():
    try:
        id_reteta = int(id_reteta_entry.get())
        cursor.execute("SELECT * FROM retete WHERE id=?", (id_reteta,))
        reteta = cursor.fetchone()
        if reteta is not None:
            cursor.execute("DELETE FROM retete WHERE id=?", (id_reteta,))
            cursor.execute("DELETE FROM medicamente WHERE reteta_id=?", (id_reteta,))
            conn.commit()
            afiseaza_retete()
            messagebox.showinfo("Informație", "Rețetă ștearsă cu succes.")
        else:
            messagebox.showwarning("Avertisment", "Nu există nicio rețetă cu ID-ul specificat.")
    except Exception as e:
        messagebox.showerror("Eroare", f"A apărut o eroare.\nDetalii eroare: {e}")

def genereaza_raport_medicamente():
    data_inceput = raport_medicamente_data_inceput_calendar.get_date()
    data_sfarsit = raport_medicamente_data_sfarsit_calendar.get_date()
    cursor.execute("SELECT medicamente.denumire, SUM(medicamente.cantitate_prescrisa) "
                   "FROM medicamente "
                   "INNER JOIN retete ON medicamente.reteta_id = retete.id "
                   "WHERE retete.data_emitere BETWEEN ? AND ? "
                   "GROUP BY medicamente.denumire",
                   (data_inceput, data_sfarsit))
    
    raport_medicamente = cursor.fetchall()

    raport_text_medicamente.delete(1.0, tk.END)  
    raport_text_medicamente.insert(tk.END, "Denumire medicament\tCantitate prescrisă\n")
    for linie in raport_medicamente:
        raport_text_medicamente.insert(tk.END, f"{linie[0]}\t\t\t{linie[1]}\n")


def genereaza_raport_pacienti():
    data_inceput = raport_pacienti_data_inceput_calendar.get_date()
    data_sfarsit = raport_pacienti_data_sfarsit_calendar.get_date()

    cursor.execute("SELECT pacienti.nume, pacienti.prenume, COUNT(retete.id) "
                   "FROM pacienti "
                   "LEFT JOIN retete ON pacienti.id = retete.pacient_id "
                   "WHERE retete.data_emitere BETWEEN ? AND ? "
                   "GROUP BY pacienti.id",
                   (data_inceput, data_sfarsit))

    raport_pacienti = cursor.fetchall()

    raport_pacienti_text.delete(1.0, tk.END)
    raport_pacienti_text.insert(tk.END, "Nume pacient\tPrenume pacient\tTotal retete emise\n")
    for linie in raport_pacienti:
        nume, prenume, total_retete = linie
        raport_pacienti_text.insert(tk.END, f"{nume}\t\t{prenume}\t\t{total_retete}\n")


root = tk.Tk()
root.title("Cabinet Medical")


frame_pacienti = tk.LabelFrame(root, text="Gestionare Pacienți")
frame_pacienti.grid(row=0, column=0, padx=10, pady=5, sticky="w")

nume_label = tk.Label(frame_pacienti, text="Nume:")
nume_label.grid(row=0, column=0)
nume_entry = tk.Entry(frame_pacienti)
nume_entry.grid(row=0, column=1)

prenume_label = tk.Label(frame_pacienti, text="Prenume:")
prenume_label.grid(row=0, column=2)
prenume_entry = tk.Entry(frame_pacienti)
prenume_entry.grid(row=0, column=3)

data_nasterii_label = tk.Label(frame_pacienti, text="Data nașterii:")
data_nasterii_label.grid(row=0, column=4)
data_nasterii_calendar = DateEntry(frame_pacienti, date_pattern="yyyy-mm-dd")
data_nasterii_calendar.grid(row=0, column=5)

buton_adauga_pacient = tk.Button(frame_pacienti, text="Adaugă Pacient", command=adauga_pacient)
buton_adauga_pacient.grid(row=0, column=6)

buton_modifica_pacient = tk.Button(frame_pacienti, text="Modifică Pacient", command=modifica_pacient)
buton_modifica_pacient.grid(row=0, column=7)

buton_sterge_pacient = tk.Button(frame_pacienti, text="Șterge Pacient", command=sterge_pacient)
buton_sterge_pacient.grid(row=3, column=7)

id_pacient_label = tk.Label(frame_pacienti, text="ID Pacient:")
id_pacient_label.grid(row=2, column=6)
id_pacient_entry = tk.Entry(frame_pacienti)
id_pacient_entry.grid(row=2, column=7)

lista_pacienti = tk.Listbox(frame_pacienti, height=10, width=50)
lista_pacienti.grid(row=2, column=0, columnspan=9)


frame_retete = tk.LabelFrame(root, text="Gestionare Rețete")
frame_retete.grid(row=1, column=0, padx=10, pady=5, sticky="w")

serie_label = tk.Label(frame_retete, text="Serie:")
serie_label.grid(row=0, column=0)
serie_entry = tk.Entry(frame_retete)
serie_entry.grid(row=0, column=1)

nr_label = tk.Label(frame_retete, text="Număr:")
nr_label.grid(row=0, column=2)
nr_entry = tk.Entry(frame_retete)
nr_entry.grid(row=0, column=3)

data_emitere_label = tk.Label(frame_retete, text="Data emiterii:")
data_emitere_label.grid(row=0, column=4)
data_emitere_calendar = DateEntry(frame_retete, date_pattern="yyyy-mm-dd")
data_emitere_calendar.grid(row=0, column=5)

buton_adauga_reteta = tk.Button(frame_retete, text="Adaugă Rețetă", command=adauga_reteta)
buton_adauga_reteta.grid(row=0, column=6)

buton_modifica_reteta = tk.Button(frame_retete, text="Modifică Rețetă", command=modifica_reteta)
buton_modifica_reteta.grid(row=0, column=7)

buton_sterge_reteta = tk.Button(frame_retete, text="Șterge Rețetă", command=sterge_reteta)
buton_sterge_reteta.grid(row=3, column=7)

id_reteta_label = tk.Label(frame_retete, text="ID Rețetă:")
id_reteta_label.grid(row=2, column=6)
id_reteta_entry = tk.Entry(frame_retete)
id_reteta_entry.grid(row=2, column=7)

lista_retete = tk.Listbox(frame_retete, height=10, width=50)
lista_retete.grid(row=2, column=0, columnspan=9)

frame_raport_medicamente = tk.LabelFrame(root, text="Generare Raport Medicamente")
frame_raport_medicamente.grid(row=2, column=0, padx=10, pady=5, sticky="w")

raport_medicamente_data_inceput_label = tk.Label(frame_raport_medicamente, text="Data început:")
raport_medicamente_data_inceput_label.grid(row=0, column=0)
raport_medicamente_data_inceput_calendar = DateEntry(frame_raport_medicamente, date_pattern="yyyy-mm-dd")
raport_medicamente_data_inceput_calendar.grid(row=0, column=1)

raport_medicamente_data_sfarsit_label = tk.Label(frame_raport_medicamente, text="Data sfârșit:")
raport_medicamente_data_sfarsit_label.grid(row=0, column=2)
raport_medicamente_data_sfarsit_calendar = DateEntry(frame_raport_medicamente, date_pattern="yyyy-mm-dd")
raport_medicamente_data_sfarsit_calendar.grid(row=0, column=3)

buton_genereaza_raport_medicamente = tk.Button(frame_raport_medicamente, text="Generează Raport", command=genereaza_raport_medicamente)
buton_genereaza_raport_medicamente.grid(row=0, column=4)

raport_text_medicamente = tk.Text(frame_raport_medicamente, height=10, width=50)
raport_text_medicamente.grid(row=1, column=0, columnspan=5)

denumire_medicament_label = tk.Label(frame_retete, text="Denumire medicament:")
denumire_medicament_label.grid(row=1, column=0)
denumire_medicament_entry = tk.Entry(frame_retete)
denumire_medicament_entry.grid(row=1, column=1)

cantitate_prescrisa_label = tk.Label(frame_retete, text="Cantitate prescrisă:")
cantitate_prescrisa_label.grid(row=1, column=2)
cantitate_prescrisa_entry = tk.Entry(frame_retete)
cantitate_prescrisa_entry.grid(row=1, column=3)

dozaj_label = tk.Label(frame_retete, text="Dozaj:")
dozaj_label.grid(row=1, column=4)
dozaj_entry = tk.Entry(frame_retete)
dozaj_entry.grid(row=1, column=5)

buton_adauga_medicament = tk.Button(frame_retete, text="Adaugă Medicament", command=adauga_medicament)
buton_adauga_medicament.grid(row=1, column=6)

frame_raport_pacienti = tk.LabelFrame(root, text="Generare Raport Pacienți")
frame_raport_pacienti.grid(row=2, column=0, padx=10, pady=5, sticky="E")
raport_pacienti_text = tk.Text(frame_raport_pacienti, height=10, width=50)
raport_pacienti_text.grid(row=1, column=0, columnspan=5)

buton_genereaza_raport_pacienti = tk.Button(frame_raport_pacienti, text="Generează Raport", command=genereaza_raport_pacienti)
buton_genereaza_raport_pacienti.grid(row=0, column=4)

raport_pacienti_data_inceput_label = tk.Label(frame_raport_pacienti, text="Data început:")
raport_pacienti_data_inceput_label.grid(row=0, column=0)
raport_pacienti_data_inceput_calendar = DateEntry(frame_raport_pacienti, date_pattern="yyyy-mm-dd")
raport_pacienti_data_inceput_calendar.grid(row=0, column=1)

raport_pacienti_data_sfarsit_label = tk.Label(frame_raport_pacienti, text="Data sfârșit:")
raport_pacienti_data_sfarsit_label.grid(row=0, column=2)
raport_pacienti_data_sfarsit_calendar = DateEntry(frame_raport_pacienti, date_pattern="yyyy-mm-dd")
raport_pacienti_data_sfarsit_calendar.grid(row=0, column=3)





identificare_pacient = tk.Label(frame_retete, text="ID Pacient:")
identificare_pacient.grid(row=2, column=0)
identificare_pacient = tk.Entry(frame_retete)
identificare_pacient.grid(row=2, column=1)


fix_marime_chenar = tk.Label(frame_pacienti, text="                                             ")
fix_marime_chenar.grid(row=1, column=0)


fix_marime_chenar2 = tk.Label(frame_pacienti, text="                                            ")
fix_marime_chenar2.grid(row=1, column=2)

fix_marime_chenar2 = tk.Label(frame_pacienti, text="                              ")
fix_marime_chenar2.grid(row=1, column=4)

fix_marime_chenar3 = tk.Label(frame_pacienti, text="                  ")
fix_marime_chenar3.grid(row=1, column=6)

id_retea_globala = None

afiseaza_retete()
afiseaza_pacienti()

root.mainloop()

conn.close()
