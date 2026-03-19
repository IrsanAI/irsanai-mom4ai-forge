"""Bio-Komponenten-Bibliothek – alle Reiche des Lebens als Vorlage"""

BIO_COMPONENTS = {
    "ameisen_schwarm": {"dezentral": 0.95, "kollektiv_intelligenz": 0.90, "plastizitaet": 0.85},
    "bienen_schwarm": {"dezentral": 0.88, "kollektiv_intelligenz": 0.92, "plastizitaet": 0.80},
    "myzel_netz": {"dezentral": 0.97, "kollektiv_intelligenz": 0.75, "plastizitaet": 0.98},
    "mensch_gehirn": {"dezentral": 0.60, "kollektiv_intelligenz": 0.85, "plastizitaet": 0.95},
    "slime_mold": {"dezentral": 0.99, "kollektiv_intelligenz": 0.70, "plastizitaet": 0.99},
    "quorum_sensing": {"dezentral": 0.92, "kollektiv_intelligenz": 0.88, "plastizitaet": 0.90},
}

def get_component(name: str):
    return BIO_COMPONENTS.get(name.lower(), BIO_COMPONENTS["ameisen_schwarm"])