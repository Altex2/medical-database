# THIS TEXT IS IN ROMANIAN.... 


Realizati o aplicatie, destinata unui cabinet medical, care sa permita gestionarea electronica a retetelor medicale emise pacientilor:
Baza de date trebuie sa stocheze:
-	Lista pacientilor
-	Lista retetelor emise si continutul acestora

Informatiile pacientilor care vor fi stocate in baza de date sunt:
-	Nume
-	Prenume
-	Data nasterii

Informatiile, cu privire la retetele emise, care vor fi stocate in baza de date sunt:
-	Serie reteta – camp de tip string (Exemplu: NPHGDV)
-	Nr reteta – camp de tip numeric (Exemplu: 4387
-	Data emitere reteta
-	Medicamente incluse pe retete. Pentru fiecare medicament ne intereseaza sa avem inregistrat in baza de date urmatoarele informatii:
o	Denumire medicament
o	Cantitate prescrisa
o	Dozaj (Exemplu: 3 capsule/zi)
Aplicatia trebuie sa permita, prin intermediul interfetei utilizator, urmatoarele operatii:
-	Afisare lista pacienti cu posibilitatea de adaugare/modificare pacienti

-	Afisare lista retete cu posibilitatea de adaugare/modificare retete

-	Afisare raport medicamente prescrise intr-o anumita perioada. Utilizatorul va avea posibilitatea sa selecteze un interval calendaristic pentru care doreste rularea raportului (exemplu: de la 01.01.2021 pana la 31.01.2021). Raportul va trebui sa afiseze cate unitati, din fiecare medicament, au fost prescrise in perioada data. 
Exemplu de raport:
Denumire medicament	Cantitate prescrisa
Aspirina	14
Nurofen	23
Vitamina C	8

Raportul poate fi afisat sub forma unui grid intr-o fereastra.

-	Afisarea unui raport care sa prezinte lista pacientilor inregistrati si numarul total de retete emise pt fiecare in perioada de timp data. Utilizatorul va avea posibilitatea sa selecteze un interval calendaristic pentru care doreste rularea raportului (exemplu: de la 01.01.2021 pana la 31.01.2021).
Exemplu de raport:
Nume pacient	Prenume pacient	Total retete emise
POPESCU	ION	2
VASILESCU	PETRE	5
NASTASE	MARIA	0


Nota:
Se dorese ca, in cazul in care serverul bazei de date are un timp de raspuns mare, sa nu se blocheze interfata utilizatorului.
