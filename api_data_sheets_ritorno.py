import requests
import csv

# Configurazioni
API_KEY = "AIzaSyChwz6_vr2JTgTx7KzZtfgPtHDyHSDmJ-k"  # Inserisci qui la tua chiave API
SPREADSHEET_ID = "143HgVSjT76Y38Lq4ZXSUQmw7ammbo5OT5k8LqYcmK04"  # ID del tuo Google Sheets
COLUMN_D_RANGE = "'Risposte del modulo 1'!D2:D1000"  # Colonna D (Indirizzi)
COLUMN_F_RANGE = "'Risposte del modulo 1'!F2:F1000"  # Colonna F (Numero di Persone)
COLUMN_I_RANGE = "'Risposte del modulo 1'!I2:I1000"  # Colonna I (Nome e Numero di Telefono)
COLUMN_B_RANGE = "'Risposte del modulo 1'!B2:B1000"  # Colonna B (Autista)

# Funzione per ottenere i dati da una colonna specifica
def get_google_sheet_data(range_name):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_name}?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('values', [])
    else:
        print(f"Errore nella lettura del Google Sheet (Range: {range_name}): {response.status_code}")
        return []

# Funzione per geocodificare un indirizzo
def geocode_address(address):
    if not address:
        return None, None
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK":
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# Funzione per salvare i dati in un file CSV
def save_to_csv(data, filename="dati_ritorno.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Intestazioni CSV
        writer.writerow(["Autista", "Nome", "Cognome", "Numero di Telefono", "Indirizzo", "Numero di Persone", "Latitudine", "Longitudine"])
        # Dati
        writer.writerows(data)
    print(f"File CSV '{filename}' aggiornato!")

# Script principale
def main():
    # Step 1: Ottieni i dati dalle colonne
    indirizzi = get_google_sheet_data(COLUMN_D_RANGE)  # Colonna D
    numero_persone = get_google_sheet_data(COLUMN_F_RANGE)  # Colonna F
    nomi_telefoni = get_google_sheet_data(COLUMN_I_RANGE)  # Colonna I
    autisti = get_google_sheet_data(COLUMN_B_RANGE)  # Colonna B

    # Step 2: Allinea i dati (considerando il numero massimo di righe)
    risultati = []
    max_rows = max(len(indirizzi), len(numero_persone), len(nomi_telefoni), len(autisti))
    for i in range(max_rows):
        indirizzo = indirizzi[i][0] if i < len(indirizzi) and indirizzi[i] else None
        persone = numero_persone[i][0] if i < len(numero_persone) and numero_persone[i] else None
        nome_telefono = nomi_telefoni[i][0] if i < len(nomi_telefoni) and nomi_telefoni[i] else None
        autista = autisti[i][0] if i < len(autisti) and autisti[i] else None

        if nome_telefono:
            # Dividi Nome, Cognome e Numero di Telefono
            nome_telefono_split = nome_telefono.split()
            if len(nome_telefono_split) >= 3:  # Almeno Nome, Cognome e Telefono
                nome = nome_telefono_split[0]
                cognome = nome_telefono_split[1]
                telefono = " ".join(nome_telefono_split[2:])
            else:
                nome, cognome, telefono = None, None, None
        else:
            nome, cognome, telefono = None, None, None

        # Escludi righe con dati mancanti
        if not (autista and nome and cognome and telefono and indirizzo and persone):
            continue

        if indirizzo:
            latitudine, longitudine = geocode_address(indirizzo)
        else:
            latitudine, longitudine = None, None

        risultati.append([autista, nome, cognome, telefono, indirizzo, persone, latitudine, longitudine])

    # Step 3: Salva i risultati nel CSV
    save_to_csv(risultati)

# Esegui lo script
if __name__ == "__main__":
    main()
