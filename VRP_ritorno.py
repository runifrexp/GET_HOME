import pandas as pd
import googlemaps
import math

# Inizializza il client Google Maps
API_KEY = "AIzaSyChwz6_vr2JTgTx7KzZtfgPtHDyHSDmJ-k"
gmaps_client = googlemaps.Client(key=API_KEY)

# Feste
feste = [
    {"nome": "Festa Villani (Rovarè)", "coordinate": [45.678133561178804, 12.401392678558162], "colore": "orange"},
    {"nome": "Festa Martini (Istrana)", "coordinate": [45.65617075144528, 12.094269383482416], "colore": "blue"},
    {"nome": "Festa Morandin", "coordinate": [45.68808383977507, 12.362454539306622], "colore": "green"},
    {"nome": "Perchè no? (Istrana)", "coordinate": [45.67915872772207, 12.077284342329024], "colore": "magenta"}
]

# Leggi il file CSV delle destinazioni
file_name = "dati_ritorno.csv"  # Sostituisci con il percorso corretto
df = pd.read_csv(file_name)

# Filtra solo le destinazioni
destinazioni = df[['Cognome', 'Latitudine', 'Longitudine']]

# Estrai le coordinate di origini e destinazioni
origins = [festa['coordinate'] for festa in feste]
destination_coordinates = list(zip(destinazioni['Latitudine'], destinazioni['Longitudine']))

# Funzione per dividere le destinazioni in batch
def split_into_batches(data, batch_size):
    """Divide una lista in batch di dimensione specificata."""
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

# Calcola la matrice delle distanze con batch
def calculate_distance_matrix_in_batches(origins, destinations, batch_size=25):
    """Crea una matrice delle distanze stradali usando Google Maps API, rispettando i limiti di batch."""
    batches = split_into_batches(destinations, batch_size)
    distance_matrix = []
    
    for origin in origins:
        origin_row = []
        for batch in batches:
            result = gmaps_client.distance_matrix(
                origins=[origin],
                destinations=batch,
                mode="driving"
            )
            origin_row.extend(
                element['distance']['value'] / 1000 if 'distance' in element else None
                for element in result['rows'][0]['elements']
            )
        distance_matrix.append(origin_row)
    return distance_matrix

# Calcola la matrice delle distanze
distance_matrix = calculate_distance_matrix_in_batches(origins, destination_coordinates)

# Crea un DataFrame per visualizzare i risultati
distance_df = pd.DataFrame(
    distance_matrix,
    index=[festa['nome'] for festa in feste],  # Nomi delle feste come indice
    columns=destinazioni['Cognome']  # Cognome come intestazione delle colonne
)

# Visualizza la matrice
print(distance_df)

# Salva la matrice in un file CSV per analisi successive
distance_df.to_csv("matrice_distanze_feste_destinazioni.csv", index=True)
