import folium
import pandas as pd

def crea_mappa(csv_file="dati_andata.csv", output_file="mappe/andata/mappa_andata.html"):
    # Leggi il file CSV
    dati = pd.read_csv(csv_file)

    # Palette di colori predefiniti ben distinguibili
    palette_colori = [
        "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#FFD433",
        "#33FFF0", "#A133FF", "#FFB533", "#8DFF33", "#FF3380"
    ]

    # Assegna un colore fisso a ciascun autista
    autisti = dati['Autista'].unique()
    colori = {autista: palette_colori[i % len(palette_colori)] for i, autista in enumerate(autisti)}

    # Crea la mappa centrata sulla media delle coordinate
    media_lat = dati['Latitudine'].mean()
    media_lng = dati['Longitudine'].mean()
    mappa = folium.Map(location=[media_lat, media_lng], zoom_start=10)

    # Aggiungi i punti alla mappa
    for _, row in dati.iterrows():
        if pd.notna(row['Latitudine']) and pd.notna(row['Longitudine']):
            popup_info = (
                f"<b>Nome:</b> {row['Nome']} {row['Cognome']}<br>"
                f"<b>Telefono:</b> {row['Numero di Telefono']}<br>"
                f"<b>Indirizzo:</b> {row['Indirizzo']}<br>"
                f"<b>Numero di Persone:</b> {row['Numero di Persone']}<br>"
                f"<b>Autista:</b> {row['Autista']}"
            )
            folium.CircleMarker(
                location=[row['Latitudine'], row['Longitudine']],
                radius=10,  # Dimensione del marker
                color=colori[row['Autista']],  # Colore del bordo
                fill=True,
                fill_color=colori[row['Autista']],  # Colore del riempimento
                fill_opacity=0.7,
                popup=popup_info
            ).add_to(mappa)

    # Aggiungi legenda
    legenda_html = "<div style='position: fixed; bottom: 50px; left: 50px; width: 300px; background-color: white; border: 2px solid black; z-index: 1000; padding: 10px;'>"
    legenda_html += "<h4>Autisti</h4>"
    for autista, colore in colori.items():
        legenda_html += f"<div style='display: flex; align-items: center;'><div style='width: 20px; height: 20px; background-color: {colore}; margin-right: 10px;'></div>{autista}</div>"
    legenda_html += "</div>"
    mappa.get_root().html.add_child(folium.Element(legenda_html))

    # Salva la mappa
    mappa.save(output_file)
    print(f"Mappa salvata in {output_file}!")

# Chiamata della funzione
crea_mappa()
