"""Bio-Komponenten-Bibliothek – alle Reiche des Lebens als Vorlage."""

BIO_COMPONENTS = {
    # Kern-Komponenten (bestehende Namenskonventionen im Projekt)
    "ameisen_schwarm": {"plastizitaet": 0.72, "dezentral": 0.95},
    "bienen_schwarm": {"plastizitaet": 0.68, "dezentral": 0.88},
    "myzel_netz": {"plastizitaet": 0.90, "dezentral": 0.97},
    "quorum_sensing": {"plastizitaet": 0.74, "dezentral": 0.90},
    "mensch_gehirn": {"plastizitaet": 0.86, "dezentral": 0.62},
    "slime_mold": {"plastizitaet": 0.88, "dezentral": 0.93},
    "vogelzug": {"plastizitaet": 0.57, "dezentral": 0.84},
    "oktopus_nervensystem": {"plastizitaet": 0.95, "dezentral": 0.90},
    "korallenriff": {"plastizitaet": 0.63, "dezentral": 0.76},
    "pflanzenwurzelnetz": {"plastizitaet": 0.79, "dezentral": 0.87},
    "elefantenherde": {"plastizitaet": 0.71, "dezentral": 0.64},
    "wolf_rudel": {"plastizitaet": 0.73, "dezentral": 0.70},
    "termitenbau": {"plastizitaet": 0.70, "dezentral": 0.92},
}

# Erweiterung BIO_COMPONENTS – neue Arten für mehr Vielfalt & verrückte Namen
BIO_COMPONENTS.update({
    "libellen_schwarm": {"plastizitaet": 0.92, "dezentral": 0.96},
    "bakterien_biofilm": {"plastizitaet": 0.88, "dezentral": 0.99},
    "tiefsee_leuchtnetz": {"plastizitaet": 0.75, "dezentral": 0.82},
    "pilz_ektomykorrhiza": {"plastizitaet": 0.94, "dezentral": 0.97},
    "ameisen_blattschneider": {"plastizitaet": 0.68, "dezentral": 0.91},
    "honigbienentanz": {"plastizitaet": 0.62, "dezentral": 0.85},
    "schwarmfisch": {"plastizitaet": 0.80, "dezentral": 0.94},
    "vogel_formation": {"plastizitaet": 0.58, "dezentral": 0.89},
    "termite_klimakammer": {"plastizitaet": 0.72, "dezentral": 0.93},
    "oktopus_kamouflage": {"plastizitaet": 0.98, "dezentral": 0.99},
    "pflanzen_woodwideweb": {"plastizitaet": 0.91, "dezentral": 0.96},
    "elefanten_matriarchat": {"plastizitaet": 0.82, "dezentral": 0.65},
    "wolf_rudel_jagd": {"plastizitaet": 0.78, "dezentral": 0.72},
    "korallen_symbiose": {"plastizitaet": 0.67, "dezentral": 0.78},
    "muecken_wolke": {"plastizitaet": 0.85, "dezentral": 0.95},
    "algen_bluete": {"plastizitaet": 0.70, "dezentral": 0.88},
    "virus_mutationsdruck": {"plastizitaet": 0.99, "dezentral": 0.97},
    "schnecken_chemospur": {"plastizitaet": 0.65, "dezentral": 0.80},
    "fledermaus_echolot": {"plastizitaet": 0.81, "dezentral": 0.84},
    "kaktus_wasserspeicher": {"plastizitaet": 0.55, "dezentral": 0.60},
})


def get_component(name: str):
    return BIO_COMPONENTS.get(name.lower(), BIO_COMPONENTS["ameisen_schwarm"])
