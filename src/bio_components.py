"""Bio-Komponenten-Bibliothek – alle Reiche des Lebens als Vorlage"""
# In bio_components.py – erweitere BIO_COMPONENTS
BIO_COMPONENTS = {
    "ameisen_schwarm": {"plastizitaet": 0.7, "dezentral": 0.9},
    "bienen_schwarm": {"plastizitaet": 0.6, "dezentral": 0.8},
    "myzel_netz": {"plastizitaet": 0.95, "dezentral": 0.98},
    "slime_mold": {"plastizitaet": 0.9, "dezentral": 0.95},
    "mensch_gehirn": {"plastizitaet": 0.85, "dezentral": 0.4},
    "quorum_sensing": {"plastizitaet": 0.8, "dezentral": 0.85},
    # NEU HINZUFÜGEN:
    "korallenriff": {"plastizitaet": 0.65, "dezentral": 0.75},
    "termite_bau": {"plastizitaet": 0.7, "dezentral": 0.92},
    "vogelzug": {"plastizitaet": 0.55, "dezentral": 0.88},
    "oktopus_nervensystem": {"plastizitaet": 0.98, "dezentral": 0.99},
    "pflanzenwurzelnetz": {"plastizitaet": 0.9, "dezentral": 0.97},
    "wolf_rudel": {"plastizitaet": 0.75, "dezentral": 0.7},
    "elefanten_matriarchat": {"plastizitaet": 0.8, "dezentral": 0.6},
}

def get_component(name: str):
    return BIO_COMPONENTS.get(name.lower(), BIO_COMPONENTS["ameisen_schwarm"])