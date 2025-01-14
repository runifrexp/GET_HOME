# colore associato a ogni guidatore per le mappe 

# Mappa dei colori fissi per i guidatori
COLORI_GUIDATORI = {
    "Artu": "#1f77b4",  # Blu
    "Gio": "#ff7f0e",  # Arancione
    "Ciro": "#2ca02c",  # Verde
    "Fil": "#d62728",  # Rosso
    "Dado": "#9467bd",  # Viola
    "Jaco": "#8c564b",  # Marrone
}

def get_colore(autista):
    """
    Ritorna il colore associato a un autista. 
    Se l'autista non è nella lista, ritorna un colore predefinito (nero).
    """
    return COLORI_GUIDATORI.get(autista, "#000000")  # Nero come colore predefinito
