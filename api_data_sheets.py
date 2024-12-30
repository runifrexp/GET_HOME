import requests
import csv

# Configurazioni
API_KEY = "AIzaSyAwUffePIA3gL_Cz2qadHa6v-RFg9MWIZc"  # Inserisci qui la tua chiave API
SPREADSHEET_ID = "143HgVSjT76Y38Lq4ZXSUQmw7ammbo5OT5k8LqYcmK04"  # ID del tuo Google Sheets
COLUMN_C_RANGE = "'Risposte del modulo 1'!C2:C1000"  # Solo colonna C (Indirizzi)
COLUMN_G_RANGE = "'Risposte del modulo 1'!G2:G1000"  # Solo colonna G (Nomi e Telefono)
COLUMN_E_RANGE = "'Risposte del modulo 1'!E2:E1000"  # Solo colonna C (Indirizzi)

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
def save_to_csv(data, filename="dati_geocodificati.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Intestazioni CSV
        writer.writerow(["Nome", "Cognome", "Numero di Telefono", "Indirizzo", "Numero di Persone", "Latitudine", "Longitudine"])
        # Dati
        writer.writerows(data)
    print(f"File CSV '{filename}' aggiornato!")

# Script principale
def main():
    # Step 1: Ottieni i dati dalle colonne
    indirizzi = get_google_sheet_data(COLUMN_C_RANGE)  # Colonna C
    nomi_telefoni = get_google_sheet_data(COLUMN_G_RANGE)  # Colonna G
    numero_persone = get_google_sheet_data(COLUMN_E_RANGE)  # Colonna E

    # Step 2: Allinea i dati (considerando il numero massimo di righe)
    risultati = []
    max_rows = max(len(indirizzi), len(nomi_telefoni), len(numero_persone))
    for i in range(max_rows):
        indirizzo = indirizzi[i][0] if i < len(indirizzi) and indirizzi[i] else None
        nome_telefono = nomi_telefoni[i][0] if i < len(nomi_telefoni) and nomi_telefoni[i] else None
        persone = numero_persone[i][0] if i < len(numero_persone) and numero_persone[i] else None

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
        if not (nome and cognome and telefono and indirizzo and persone):
            continue

        if indirizzo:
            latitudine, longitudine = geocode_address(indirizzo)
        else:
            latitudine, longitudine = None, None

        risultati.append([nome, cognome, telefono, indirizzo, persone, latitudine, longitudine])

    # Step 3: Salva i risultati nel CSV
    save_to_csv(risultati)

# Esegui lo script
if __name__ == "__main__":
    main()