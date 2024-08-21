import tkinter as tk
from tkinter import messagebox
import subprocess
from functools import partial

# Funktion für den Scrape-Button eines einzelnen Services
def scrape_service(service_key, prefix):
    url = entries[service_key].get()
    if url.startswith(prefix):
        if url:
            try:
                subprocess.run(['python', f'scraper/{service_key}_scraper.py', url], check=True)
                messagebox.showinfo("Erfolg", f"{service_key.capitalize()} erfolgreich gescraped!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Fehler", f"Fehler beim Ausführen des Skripts für {service_key}: {e}")
    elif url=="":
        pass
    else:
        messagebox.showerror("Fehler", f"Die URL für {service_key} muss mit '{prefix}' beginnen!")

# Scraping-Funktion für alle Services
def scrape_all():
    # Führe alle Scraping-Skripte aus mit entsprechendem service_key und prefix aus dem Dictionary aus und gebe eine Meldung aus
    entry =messagebox.askokcancel("Warnung", "sobald sie Ok wählen werden die scripte ausgeführt, bitte warten sie bis diese vollständig ausgeführt sind")
    if entry:
        for label, service_key, prefix in services:
            scrape_service(service_key, prefix)
        messagebox.showinfo("Fertig", "Alle befüllten Scraping-links wurden ausgeführt!")
    else: 
        pass

# Hauptfenster
root = tk.Tk()
root.title("Jobbörsen Scraper")

# Definiere das Layout
services = [
    ('Arbeitsagentur', 'arbeitsagentur', 'https://www.arbeitsagentur.de/jobsuche/search'),
    ('Indeed', 'indeed', 'https://www.indeed.de'),
    ('StepStone', 'stepstone', 'https://www.stepstone.de'),
    ('Monster', 'monster', 'https://www.monster.de'),
    ('XING Jobs', 'xing', 'https://www.xing.com/jobs'),
    ('Jobware', 'jobware', 'https://www.jobware.de'),
    ('Kimeta', 'kimeta', 'https://www.kimeta.de'),
    ('Absolventa', 'absolventa', 'https://www.absolventa.de'),
    ('Hays', 'hays', 'https://www.hays.de'),
    ('LinkedIn', 'linkedin', 'https://www.linkedin.com/jobs'),
    ('Glassdoor', 'glassdoor', 'https://www.glassdoor.de'),
    ('ZipRecruiter', 'ziprecruiter', 'https://www.ziprecruiter.de'),
    ('CareerBuilder', 'careerbuilder', 'https://www.careerbuilder.de'),
    ('SimplyHired', 'simplyhired', 'https://www.simplyhired.de'),
    ('Jooble', 'jooble', 'https://www.jooble.org'),
    ('Upwork', 'upwork', 'https://www.upwork.com'),
    ('We Work Remotely', 'weworkremotely', 'https://weworkremotely.com')
]

# Variablen und Widgets erstellen
entries = {}
for index, (label, key, prefix) in enumerate(services):
    tk.Label(root, text=f'{label} URL:').grid(row=index, column=0, padx=10, pady=5, sticky='w')
    var = tk.StringVar()
    entries[key] = var
    tk.Entry(root, textvariable=var, width=50).grid(row=index, column=1, padx=10, pady=5)
    
    # Verwende functools.partial, um die Argumente an die Funktion zu übergeben
    scrape_button = tk.Button(root, text=f'Scrape {label}', command=partial(scrape_service, key, prefix))
    scrape_button.grid(row=index, column=2, padx=10, pady=5)

# Scrape All Button
tk.Button(root, text='SCRAPE ALL', command=scrape_all, bg='red', fg='white').grid(row=len(services), column=0, columnspan=3, pady=20)

# UI starten
root.mainloop()
