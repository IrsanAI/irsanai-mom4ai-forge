"""Bio-Komponenten-Bibliothek – alle Reiche des Lebens als Vorlage"""
# Erweiterung BIO_COMPONENTS – neue Arten für mehr Vielfalt & verrückte Namen
BIO_COMPONENTS.update({
    "libellen_schwarm":      {"plastizitaet": 0.92, "dezentral": 0.96},   # extrem schnell, wendig, kollektiv
    "bakterien_biofilm":     {"plastizitaet": 0.88, "dezentral": 0.99},   # anpassungsfähig, kolonieartig
    "tiefsee_leuchtnetz":    {"plastizitaet": 0.75, "dezentral": 0.82},   # biolumineszenz, signalbasiert
    "pilz_ektomykorrhiza":   {"plastizitaet": 0.94, "dezentral": 0.97},   # wurzelnetz-erweiterung
    "ameisen_blattschneider": {"plastizitaet": 0.68, "dezentral": 0.91},  # Landwirtschaft, Pilzzucht
    "honigbienentanz":       {"plastizitaet": 0.62, "dezentral": 0.85},   # präzise Kommunikation
    "schwarmfisch":          {"plastizitaet": 0.80, "dezentral": 0.94},   # schnelle kollektive Entscheidung
    "vogel_formation":       {"plastizitaet": 0.58, "dezentral": 0.89},   # Langstrecken-Navigation
    "termite_klimakammer":   {"plastizitaet": 0.72, "dezentral": 0.93},   # gigantische Strukturen
    "oktopus_kamouflage":    {"plastizitaet": 0.98, "dezentral": 0.99},   # adaptive Intelligenz
    "pflanzen_woodwideweb":  {"plastizitaet": 0.91, "dezentral": 0.96},   # Ressourcenteilung
    "elefanten_matriarchat": {"plastizitaet": 0.82, "dezentral": 0.65},   # Gedächtnis, soziale Bindung
    "wolf_rudel_jagd":       {"plastizitaet": 0.78, "dezentral": 0.72},   # Koordination, Hierarchie
    "korallen_symbiose":     {"plastizitaet": 0.67, "dezentral": 0.78},   # langsame, stabile Netze
    "muecken_wolke":         {"plastizitaet": 0.85, "dezentral": 0.95},   # chaotisch, aber kollektiv
    "algen_bluete":          {"plastizitaet": 0.70, "dezentral": 0.88},   # explosionsartiges Wachstum
    "virus_mutationsdruck":  {"plastizitaet": 0.99, "dezentral": 0.97},   # extrem schnelle Evolution
    "schnecken_chemospur":   {"plastizitaet": 0.65, "dezentral": 0.80},   # Pfadfindung, chemisch
    "fledermaus_echolot":    {"plastizitaet": 0.81, "dezentral": 0.84},   # räumliche Intelligenz
    "kaktus_wasserspeicher": {"plastizitaet": 0.55, "dezentral": 0.60},   # Überleben unter Extrembedingungen
})

def get_component(name: str):
    return BIO_COMPONENTS.get(name.lower(), BIO_COMPONENTS["ameisen_schwarm"])