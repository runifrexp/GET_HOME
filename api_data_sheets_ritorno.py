import requests
import csv

# Configurazioni
API_KEY = ""  # Inserisci qui la tua chiave API
SPREADSHEET_ID = "143HgVSjT76Y38Lq4ZXSUQmw7ammbo5OT5k8LqYcmK04"  # ID del tuo Google Sheets
COLUMN_D_RANGE = "'Risposte del modulo 1'!D2:D1000"  # Colonna D (Indirizzi destinazione)
COLUMN_F_RANGE = "'Risposte del modulo 1'!F2:F1000"  # Colonna F (Numero di Persone)
COLUMN_I_RANGE = "'Risposte del modulo 1'!I2:I1000"  # Colonna I (Nome e Numero di Telefono)
COLUMN_B_RANGE = "'Risposte del modulo 1'!B2:B1000"  # Colonna B (Autista)
COLUMN_J_RANGE = "'Risposte del modulo 1'!J2:J1000"  # Colonna J (Festa di partenza)
COLUMN_G_RANGE = "'Risposte del modulo 1'!G2:G1000"  # Colonna G (Orario Desiderato)


# Feste e relative coordinate
feste = {
    "Festa Villani (Rovarè)": [45.678133561178804, 12.401392678558162],
    "Festa Martini (Istrana)": [45.65617075144528, 12.094269383482416],
    "Festa Morandin": [45.68808383977507, 12.362454539306622],
    "Perchè no? (Istrana)": [45.67915872772207, 12.077284342329024]
}

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
        writer.writerow([
            "Autista", "Nome", "Cognome", "Numero di Telefono", "Indirizzo",
            "Numero di Persone", "Festa Partenza", "Latitudine_Partenza", "Longitudine_Partenza",
            "Latitudine_Destinazione", "Longitudine_Destinazione", "Orario_Desiderato"
        ])
        # Dati
        writer.writerows(data)
    print(f"File CSV '{filename}' aggiornato!")

# Funzione per rimuovere i secondi
def format_time(time_str):
    """Rimuove i secondi da un orario."""
    if isinstance(time_str, str) and "." in time_str:  # Se il formato include secondi (es. 4.30.00)
        return time_str.split(".")[0]  # Mantieni solo ore:minuti
    return time_str  # Restituisci l'orario così com'è se non ci sono secondi

# Script principale aggiornato
def main():
    # Step 1: Ottieni i dati dalle colonne
    indirizzi = get_google_sheet_data(COLUMN_D_RANGE)  # Colonna D (Indirizzi destinazione)
    numero_persone = get_google_sheet_data(COLUMN_F_RANGE)  # Colonna F (Numero di Persone)
    nomi_telefoni = get_google_sheet_data(COLUMN_I_RANGE)  # Colonna I (Nome e Numero di Telefono)
    autisti = get_google_sheet_data(COLUMN_B_RANGE)  # Colonna B (Autista)
    feste_partenza = get_google_sheet_data(COLUMN_J_RANGE)  # Colonna J (Festa di partenza)
    orari_desiderati = get_google_sheet_data(COLUMN_G_RANGE)  # Colonna G (Orario Desiderato)

    # Step 2: Allinea i dati (considerando il numero massimo di righe)
    risultati = []
    max_rows = max(len(indirizzi), len(numero_persone), len(nomi_telefoni), len(autisti), len(feste_partenza), len(orari_desiderati))
    for i in range(max_rows):
        indirizzo = indirizzi[i][0] if i < len(indirizzi) and indirizzi[i] else None
        persone = numero_persone[i][0] if i < len(numero_persone) and numero_persone[i] else None
        nome_telefono = nomi_telefoni[i][0] if i < len(nomi_telefoni) and nomi_telefoni[i] else None
        autista = autisti[i][0] if i < len(autisti) and autisti[i] else None
        festa_partenza = feste_partenza[i][0] if i < len(feste_partenza) and feste_partenza[i] else None
        orario_desiderato = format_time(orari_desiderati[i][0]) if i < len(orari_desiderati) and orari_desiderati[i] else None

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
        if not (autista and nome and cognome and telefono and indirizzo and persone and festa_partenza and orario_desiderato):
            continue

        # Geocodifica destinazione
        if indirizzo:
            latitudine, longitudine = geocode_address(indirizzo)
        else:
            latitudine, longitudine = None, None

        # Coordinate della festa di partenza
        lat_partenza, lon_partenza = feste.get(festa_partenza, (None, None))

        riga = [
            autista, nome, cognome, telefono, indirizzo, persone,
            festa_partenza, lat_partenza, lon_partenza, latitudine, longitudine, orario_desiderato
        ]

        print(riga)  # Stampa la riga elaborata
        risultati.append(riga)
        
    # Step 3: Salva i risultati nel CSV
    save_to_csv(risultati)

# Esegui lo script
if __name__ == "__main__":
    main()
