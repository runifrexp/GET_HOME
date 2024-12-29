import pandas as pd

# Carica il file CSV
file_name = 'return_data.csv'
data = pd.read_csv(file_name)

# Seleziona solo le colonne utili
data_cleaned = data[[
    'ZONA FERMATA PRINCIPALE:', 
    'INDIRIZZO FERMATA PRINCIPALE:es: via Cesare Battisti, 56, Silea', 
    'IN QUANTI SIETE', 
    'ORARIO RITORNO', 
    'COORDINATE',
    'per completare la registrazione lascia NOME COGNOME e NUMERO DI TELEFONO: es: Marco Rossi 3456858481',
    'DA DOVE PARTI? (nome/indirizzo/organizzatori festa)'
]].copy()

# Rinomina le colonne per semplificare
data_cleaned.columns = ['Zona', 'IndirizzoPrincipale', 'NumeroPersone', 'Orario', 'Coordinate', 'Nomi', 'Partenza']

# Rimuovi righe con valori mancanti
data_cleaned = data_cleaned.dropna()

# Converte l'orario in formato standard
data_cleaned['Orario'] = pd.to_datetime(
    data_cleaned['Orario'], format='%H.%M.%S', errors='coerce'
).dt.time

# Crea un dizionario: indirizzo -> lista di persone
people_dict = data_cleaned.set_index('IndirizzoPrincipale')['Nomi'].to_dict()

# Salva i dati puliti
data_cleaned.to_csv('dati_puliti.csv')

print(data_cleaned)
