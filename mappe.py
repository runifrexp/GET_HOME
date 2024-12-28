import folium
from folium import LayerControl

# Crea una mappa centrata a Treviso
mappa = folium.Map(location=[45.6669, 12.242], zoom_start=12)

# Aggiungi i luoghi delle feste
feste = [
    {"nome": "Festa Villani (Cavriè)", "coordinate": [45.70111, 12.36806], "colore": "red"},
    {"nome": "Festa Martini (Istrana)", "coordinate": [45.65617075144528, 12.094269383482416], "colore": "blue"},
    {"nome": "Festa Morandin", "coordinate": [45.68808383977507, 12.362454539306622], "colore": "purple"},
    {"nome": "Perchè no? (Istrana)", "coordinate": [45.67915872772207, 12.077284342329024], "colore": "lightblue"}
]

# Aggiungi i marker e le fasce sulla mappa
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
        radius=10000,  # Raggio in metri
        color=festa["colore"],
        fill=True,
        fill_opacity=0.3
    ).add_to(layer_0_10)
    layer_0_10.add_to(mappa)

    # Fascia 10-17 km
    layer_10_17 = folium.FeatureGroup(name=f"{festa['nome']} - Fascia 10-17 km")
    folium.Circle(
        location=festa["coordinate"],
        radius=17000,  # Raggio in metri
        color=festa["colore"],
        fill=True,
        fill_opacity=0.2
    ).add_to(layer_10_17)
    layer_10_17.add_to(mappa)

    # Fascia 17-25 km
    layer_17_25 = folium.FeatureGroup(name=f"{festa['nome']} - Fascia 17-25 km")
    folium.Circle(
        location=festa["coordinate"],
        radius=25000,  # Raggio in metri
        color=festa["colore"],
        fill=True,
        fill_opacity=0.1
    ).add_to(layer_17_25)
    layer_17_25.add_to(mappa)

# Aggiungi il controllo dei layer
LayerControl().add_to(mappa)

# Salva la mappa come file HTML
mappa.save("mappa_feste_interattiva.html")

print("Mappa salvata come 'mappa_feste_interattiva.html'. Aprila con un browser per visualizzarla!")
