import tkinter as tk
from tkinter import messagebox, filedialog # Importálva a filedialog
import os
import re

def nev_konvertalas(nev):
    
    nev = nev.strip()
    
    reszek = re.split(r'[ \-]', nev)
    
    if len(reszek) < 2:
        return None

    vezeteknev_reszei = reszek[:-1]
    vezeteknev = '.'.join(vezeteknev_reszei)
    
    keresztnev = reszek[-1]
    
    def karakter_normalizalas(karakter):
        if karakter in 'áÁ': return 'a'
        if karakter in 'éÉ': return 'e'
        if karakter in 'íÍ': return 'i'
        if karakter in 'óÓöÖőŐúÚüÜűŰ': return 'o' if karakter in 'óÓőŐ' else 'u'
        return karakter.lower()

    def nev_normalizalas(n):
        return ''.join(karakter_normalizalas(k) for k in n)

    normalizalt_vezeteknev = nev_normalizalas(vezeteknev.replace(' ', '-'))
    normalizalt_keresztnev = nev_normalizalas(keresztnev)

    email_cim = f"{normalizalt_vezeteknev}.{normalizalt_keresztnev}@premontrei-zsambek.edu.hu"
    
    email_cim = email_cim.replace('--', '-')
    
    return email_cim

# ÚJ FÜGGVÉNY a fájl kiválasztására
def fajl_valasztas():
    fajl_eleresi_ut = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Válassza ki a bemeneti TXT fájlt"
    )
    if fajl_eleresi_ut:
        beviteli_mezo_fajlnev.delete(0, tk.END)
        beviteli_mezo_fajlnev.insert(0, fajl_eleresi_ut)
        
def fajl_feldolgozas():
    
    bemeneti_fajlnev = beviteli_mezo_fajlnev.get().strip()
    
    if not bemeneti_fajlnev:
        messagebox.showerror("Hiba", "Kérem adja meg a bemeneti fájl nevét!")
        return

    if not os.path.exists(bemeneti_fajlnev):
        messagebox.showerror("Hiba", f"A fájl nem található: {bemeneti_fajlnev}")
        return

    try:
        
        with open(bemeneti_fajlnev, 'r', encoding='utf-8') as bemeneti_fajl:
            nevek = [sor.strip() for sor in bemeneti_fajl if sor.strip()]

        konvertalt_emailek = []
        konverzio_hibak = 0
        
        
        for nev in nevek:
            email = nev_konvertalas(nev)
            if email:
                konvertalt_emailek.append(email)
            else:
                konverzio_hibak += 1
                print(f"Hiba a konvertálásnál: '{nev}'")

        
        alap_nev, kiterjesztes = os.path.splitext(bemeneti_fajlnev)
        kimeneti_fajlnev = f"{alap_nev}_emailek{kiterjesztes}"

        
        with open(kimeneti_fajlnev, 'w', encoding='utf-8') as kimeneti_fajl:
            for email in konvertalt_emailek:
                kimeneti_fajl.write(email + '\n')

        
        sikeres_uzenet = (
            f"Sikeres konvertálás!\n"
            f"Feldolgozott nevek: {len(nevek)}\n"
            f"Létrehozott e-mail címek: {len(konvertalt_emailek)}\n"
            f"Konverziós hibák (kihagyva): {konverzio_hibak}\n"
            f"Az eredmény a(z) **{kimeneti_fajlnev}** fájlba lett mentve."
        )
        messagebox.showinfo("Siker", sikeres_uzenet)

    except Exception as hiba:
        messagebox.showerror("Hiba", f"Feldolgozási hiba történt: {hiba}")


# GUI Beállítások
gyoker_ablak = tk.Tk()
gyoker_ablak.title("📧 Premontrei E-mail Konvertáló")
gyoker_ablak.geometry("450x200") # Ablak méret növelése az új gomb miatt

cimke_fajlnev = tk.Label(gyoker_ablak, text="Bemeneti TXT fájl kiválasztása:")
cimke_fajlnev.pack(pady=5)

beviteli_mezo_fajlnev = tk.Entry(gyoker_ablak, width=50)
beviteli_mezo_fajlnev.pack(pady=5, padx=10)

# ÚJ GOMB a fájl kiválasztására
gomb_fajl_valasztas = tk.Button(gyoker_ablak, text="Fájl kiválasztása...", command=fajl_valasztas)
gomb_fajl_valasztas.pack(pady=5)

gomb_konvertalas = tk.Button(gyoker_ablak, text="Konvertálás és Mentés", command=fajl_feldolgozas, bg="#007bff", fg="white", font=('Arial', 10, 'bold')) # Szín megváltoztatása
gomb_konvertalas.pack(pady=10)

gyoker_ablak.mainloop()