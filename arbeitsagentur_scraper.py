from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from bs4 import BeautifulSoup
import pyautogui 
import pandas as pd
import time

# Starte Chrome im gesteuerten Modus
options = webdriver.ChromeOptions()
# starte chrome auf der rechten bildschirm hälfte
options.add_argument("--window-position=980,0")
driver = webdriver.Chrome(options=options)

# Öffne die Seite (Ersetze die URL durch die gewünschte)
driver.get("https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&wo=M%C3%B6nchengladbach&umkreis=15&berufsfeld=Biologie;IT-Netzwerktechnik,%20-Administration,%20-Organisation;IT-Systemanalyse,%20-Anwendungsberatung%20und%20-Vertrieb;Informatik;Medien-,%20Dokumentations-%20und%20Informationsdienste;Objekt-,%20Personen-,%20Brandschutz,%20Arbeitssicherheit;Softwareentwicklung%20und%20Programmierung;Technische%20Forschung%20und%20Entwicklung;Veranstaltungs-,%20Kamera-,%20Tontechnik;Verwaltung;Werbung%20und%20Marketing;%C3%9Cberwachung%20und%20Steuerung%20des%20Verkehrsbetriebs;%C3%9Cberwachung,%20Wartung%20Verkehrsinfrastruktur&zeitarbeit=true")

# Warte, bis die Seite vollständig geladen ist
time.sleep(5)  # Wartezeit je nach Internetgeschwindigkeit anpassen

# drücke enter durch pyautogui
pyautogui.press('enter')

# Drücke den Button "Weitere Ergebnisse", bis er nicht mehr angezeigt wird
while True:
    try:
        # Finde den Button
        load_more_button = driver.find_element(By.ID, "ergebnisliste-ladeweitere-button")
        
        # Scrolle zum Button
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1)  # Warte, damit das Scrolling sich setzen kann
        # Klicke den Button
        load_more_button.click()
        # Warte, bis weitere Ergebnisse geladen sind
        time.sleep(2)  # Wartezeit je nach Ladegeschwindigkeit anpassen
    except (NoSuchElementException, ElementNotInteractableException):
        # Wenn der Button nicht mehr existiert oder nicht mehr interagierbar ist, beende die Schleife
        break

# Hole den Seitenquelltext
page_source = driver.page_source

# Schließe den Browser
driver.quit()

# Nutze BeautifulSoup, um die Seite zu parsen
soup = BeautifulSoup(page_source, 'html.parser')

# Finde alle relevanten Links
job_links = soup.find_all('a', href=lambda x: x and x.startswith("https://www.arbeitsagentur.de/jobsuche/jobdetail/"))

# Daten sammeln
data = []
for link in job_links:
    try:
        job_category = link.find('div', class_='oben').text.strip()
        job_name = link.find('span', class_='mitte-links-titel').text.strip()
        company_name = link.find('div', class_='mitte-links-arbeitgeber').text.strip()
        location = link.find('span', class_='mitte-links-ort').text.strip()
        start_date = link.find('span', class_='unten-eintrittsdatum').text.strip()

        data.append(["arbeitsagentur", job_category, job_name, company_name, location, start_date, link['href']])
    except AttributeError:
        # Falls irgendein Element nicht gefunden wird, überspringen wir diesen Eintrag
        continue

# Erstelle einen DataFrame und speichere ihn als CSV
df = pd.DataFrame(data, columns=['Jobkategorie', 'Jobname', 'Unternehmensname', 'Standort', 'Startdatum', 'Link'])
df.to_csv('job_listings.csv', index=False, encoding='utf-8')

print("Daten wurden erfolgreich in job_listings.csv gespeichert")