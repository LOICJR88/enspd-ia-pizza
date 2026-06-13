
"""
Module NLP - ENSPD IA PIZZA
Classification d'intentions et extraction d'entités (approche basée règles)
"""
import re
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "data", "menu.json"), encoding="utf-8") as f:
    MENU = json.load(f)

PIZZAS = list(MENU["pizzas"].keys())
TAILLES = list(MENU["tailles"].keys())
EXTRAS = list(MENU["extras"].keys())

# Nombres en lettres -> chiffres
NUM_WORDS = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4,
    "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10
}

INTENT_PATTERNS = {
    "commander": [r"je veux", r"je voudrais", r"commander", r"ajoute", r"donne[- ]moi", r"prendre"],
    "modifier": [r"change", r"modifie", r"remplace", r"plutot"],
    "annuler": [r"annule", r"annulation", r"supprime", r"retire"],
    "prix": [r"prix", r"combien", r"total", r"cout", r"coute"],
    "confirmer": [r"confirme", r"valide", r"c'est tout", r"finaliser", r"terminer"],
    "saluer": [r"bonjour", r"salut", r"bonsoir", r"hello"],
    "menu": [r"menu", r"quelles pizzas", r"que proposez", r"liste"]
}


def detecter_intent(texte):
    texte = texte.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, texte):
                return intent
    return "fallback"


def extraire_quantite(texte):
    texte = texte.lower()
    # Chiffres
    match = re.search(r"\b(\d+)\b", texte)
    if match:
        return int(match.group(1))
    # Nombres en lettres
    for mot, val in NUM_WORDS.items():
        if re.search(r"\b" + mot + r"\b", texte):
            return val
    return 1


def extraire_pizza(texte):
    texte = texte.lower()
    for pizza in PIZZAS:
        if pizza in texte:
            return pizza
    return None


def extraire_taille(texte):
    texte = texte.lower()
    for taille in TAILLES:
        if taille in texte:
            return taille
    return "moyenne"  # taille par défaut


def extraire_extras(texte):
    texte = texte.lower()
    trouves = []
    for extra in EXTRAS:
        if extra in texte:
            trouves.append(extra)
    return trouves


def analyser(texte):
    """
    Fonction principale du moteur NLP.
    Retourne un dictionnaire avec intent + entités extraites.
    """
    intent = detecter_intent(texte)
    resultat = {
        "intent": intent,
        "texte_original": texte,
        "entites": {
            "pizza": extraire_pizza(texte),
            "taille": extraire_taille(texte),
            "quantite": extraire_quantite(texte),
            "extras": extraire_extras(texte)
        }
    }
    return resultat


def calculer_prix(item):
    """ Calcule le prix d'un article du panier """
    pizza = item["pizza"]
    taille = item["taille"]
    quantite = item["quantite"]
    extras = item.get("extras", [])

    prix_base = MENU["pizzas"][pizza]["prix_base"]
    prix_taille = MENU["tailles"][taille]
    prix_extras = sum(MENU["extras"][e] for e in extras)

    prix_unitaire = prix_base + prix_taille + prix_extras
    return prix_unitaire * quantite
