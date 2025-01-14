import folium
import pandas as pd
from folium import LayerControl
import random

# Funzione per generare colori ben distinti per autisti
def generate_distinct_colors(n):
    """
    Genera una lista di colori ben distinti per n autisti.
    :param n: Numero di colori da generare
    :return: Lista di colori
    """
    # Palette di colori distinti
    base_colors = [
        "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
        "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
        "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
        "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
    ]
    if n <= len(base_colors):
        return base_colors[:n]
    else:
        # Aggiunge colori casuali se servono più di quelli nella palette
        return base_colors + [
            "#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(n - len(base_colors))
        ]

# Supponiamo di avere una lista di autisti
autisti = ["Autista1", "Autista2", "Autista3", "Autista4", "Autista5", "Autista6"]
autisti_color_map = {autista: color for autista, color in zip(autisti, generate_distinct_colors(len(autisti)))}

# Aggiungi la mappa dei colori per le feste
feste_color_map = {
    "Festa Villani (Rovarè)": "#ff5733",  # Arancione
    "Festa Martini (Istrana)": "#33c4ff",  # Blu brillante
    "Festa Morandin": "#75ff33",          # Verde brillante
    "Perchè no? (Istrana)": "#ff33f6"    # Rosa brillante
}

# Funzione per aggiungere una leggenda personalizzata
def add_legend(map_object, autisti_color_map, feste_color_map):
    """
    Aggiunge una leggenda compatta personalizzata alla mappa.
    :param map_object: Oggetto folium.Map
    :param autisti_color_map: Dizionario con autisti e i loro colori
    :param feste_color_map: Dizionario con feste e i loro colori
    """
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 180px;
        height: auto;
        background-color: white;
        border: 1px solid grey;
        border-radius: 5px;
        padding: 5px;
        z-index: 1000;
        font-size: 12px; 
        line-height: 1.4;">
        <b>Legenda:</b><br>
    """

    # Aggiungi autisti alla leggenda
    legend_html += "<u>Autisti:</u><br>"
    for autista, color in autisti_color_map.items():
        legend_html += f'<i style="background: {color}; width: 8px; height: 8px; display: inline-block; border-radius: 50%; margin-right: 5px;"></i> {autista}<br>'

    # Aggiungi feste alla leggenda
    legend_html += "<u>Feste:</u><br>"
    for festa, color in feste_color_map.items():
        legend_html += f'<i style="background: {color}; width: 8px; height: 8px; display: inline-block; border-radius: 50%; margin-right: 5px;"></i> {festa}<br>'

    legend_html += "</div>"

    map_object.get_root().html.add_child(folium.Element(legend_html))



# Funzione per creare la mappa
def crea_mappa(csv_file="dati_andata.csv", output_file="mappe/andata/mappa_combinata_andata.html"):
    """
    Combina le destinazioni di ritorno e le feste su una mappa.
    :param csv_file: Nome del file CSV con i dati dei clienti
    :param output_file: Nome del file HTML da salvare
    """
    # Leggi il file CSV dei clienti
    dati_clienti = pd.read_csv(csv_file)

    # Definisci le feste
    feste = [
        {"nome": "Festa Villani (Rovarè)", "coordinate": [45.678133561178804, 12.401392678558162], "colore": "orange"},
        {"nome": "Festa Martini (Istrana)", "coordinate": [45.65617075144528, 12.094269383482416], "colore": "blue"},
        {"nome": "Festa Morandin", "coordinate": [45.68808383977507, 12.362454539306622], "colore": "green"},
        {"nome": "Perchè no? (Istrana)", "coordinate": [45.67915872772207, 12.077284342329024], "colore": "magenta"}
    ]

    # Crea una mappa centrata a Treviso
    mappa = folium.Map(location=[45.6669, 12.242], zoom_start=12)

    # Colori per autisti
    autisti = dati_clienti['Autista'].unique()
    colori_clienti = {autista: f"#{hash(autista) % 0xFFFFFF:06x}" for autista in autisti}

    # Colori per feste
    colori_feste = {festa["nome"]: festa["colore"] for festa in feste}

    # Aggiungi i clienti alla mappa
    for _, row in dati_clienti.iterrows():
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
                radius=8,
                color=colori_clienti[row['Autista']],
                fill=True,
                fill_color=colori_clienti[row['Autista']],
                fill_opacity=0.7,
                popup=popup_info
            ).add_to(mappa)

    # Aggiungi le feste e le fasce alla mappa
    for festa in feste:
        # Marker per la festa
        layer_marker = folium.FeatureGroup(name=f"{festa['nome']} - Marker")
        folium.Marker(
            location=festa["coordinate"],
            popup=f"<b>{festa['nome']}</b>",
            tooltip=festa["nome"],
            icon=folium.Icon(color=festa["colore"], icon="info-sign")
        ).add_to(layer_marker)
        layer_marker.add_to(mappa)

        # Fascia 0-10 km
        layer_0_10 = folium.FeatureGroup(name=f"{festa['nome']} - Fascia 0-10 km")
        folium.Circle(
            location=festa["coordinate"],
            radius=10000,
            color=festa["colore"],
            fill=True,
            fill_opacity=0.3
        ).add_to(layer_0_10)
        layer_0_10.add_to(mappa)

        # Fascia 10-17 km
        layer_10_17 = folium.FeatureGroup(name=f"{festa['nome']} - Fascia 10-17 km")
        folium.Circle(
            location=festa["coordinate"],
            radius=17000,
            color=festa["colore"],
            fill=True,
            fill_opacity=0.2
        ).add_to(layer_10_17)
        layer_10_17.add_to(mappa)

        # Fascia 17-25 km
        layer_17_25 = folium.FeatureGroup(name=f"{festa['nome']} - Fascia 17-25 km")
        folium.Circle(
            location=festa["coordinate"],
            radius=25000,
            color=festa["colore"],
            fill=True,
            fill_opacity=0.1
        ).add_to(layer_17_25)
        layer_17_25.add_to(mappa)

    # Aggiungi la leggenda
    add_legend(mappa, colori_clienti, colori_feste)

    # Aggiungi il controllo dei layer
    LayerControl().add_to(mappa)

    # Salva la mappa come file HTML
    mappa.save(output_file)
    print(f"Mappa combinata salvata in '{output_file}'!")

# Esegui la funzione
crea_mappa()
