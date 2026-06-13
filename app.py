
"""
ENSPD IA PIZZA - API Flask
Système de prise de commande de pizza par NLP
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os, json, uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from nlp.intents import analyser, calculer_prix, MENU, PIZZAS, TAILLES, EXTRAS

app = Flask(__name__)
CORS(app)

# Stockage des paniers en mémoire (clé = session_id)
PANIERS = {}


def get_panier(session_id):
    if session_id not in PANIERS:
        PANIERS[session_id] = []
    return PANIERS[session_id]


@app.route("/", methods=["GET"])
def accueil():
    return jsonify({
        "message": "Bienvenue chez ENSPD IA PIZZA !",
        "endpoints": ["/order (POST)", "/menu (GET)", "/cart/<session_id> (GET)", "/cart/<session_id>/clear (POST)"]
    })


@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU)


@app.route("/order", methods=["POST"])
def order():
    """
    Route principale : reçoit le texte du client, l'analyse avec le NLP,
    met à jour le panier et renvoie une réponse JSON.
    Body attendu : { "session_id": "abc123", "text": "Je veux une grande margherita" }
    """
    data = request.get_json(force=True)
    texte = data.get("text", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))

    if not texte:
        return jsonify({"error": "Le champ text est requis"}), 400

    analyse = analyser(texte)
    intent = analyse["intent"]
    entites = analyse["entites"]
    panier = get_panier(session_id)

    reponse = {"session_id": session_id, "intent": intent, "entites": entites}

    # --- Gestion des intentions ---
    if intent == "saluer":
        reponse["message"] = "Bonjour et bienvenue chez ENSPD IA PIZZA ! Que souhaitez-vous commander ?"

    elif intent == "menu":
        reponse["message"] = "Voici notre menu."
        reponse["menu"] = MENU

    elif intent == "commander":
        if entites["pizza"] is None:
            reponse["message"] = ("Je n'ai pas reconnu de pizza dans votre demande. "
                                   f"Nos pizzas disponibles sont : {', '.join(PIZZAS)}.")
        else:
            item = {
                "pizza": entites["pizza"],
                "taille": entites["taille"],
                "quantite": entites["quantite"],
                "extras": entites["extras"]
            }
            item["prix"] = calculer_prix(item)
            panier.append(item)
            reponse["message"] = (f"{item['quantite']} x pizza {item['pizza']} ({item['taille']}) "
                                   f"ajoutée(s) au panier pour {item['prix']} FCFA.")
            reponse["panier"] = panier

    elif intent == "modifier":
        if not panier:
            reponse["message"] = "Votre panier est vide, rien à modifier."
        else:
            dernier = panier[-1]
            if entites["taille"]:
                dernier["taille"] = entites["taille"]
            if entites["extras"]:
                dernier["extras"] = list(set(dernier.get("extras", []) + entites["extras"]))
            if entites["pizza"]:
                dernier["pizza"] = entites["pizza"]
            dernier["prix"] = calculer_prix(dernier)
            reponse["message"] = f"Commande modifiée : {dernier}"
            reponse["panier"] = panier

    elif intent == "annuler":
        if panier:
            panier.pop()
            reponse["message"] = "Le dernier article a été retiré du panier."
        else:
            reponse["message"] = "Votre panier est déjà vide."
        reponse["panier"] = panier

    elif intent == "prix":
        total = sum(item["prix"] for item in panier)
        reponse["message"] = f"Le total de votre commande est de {total} FCFA."
        reponse["total"] = total
        reponse["panier"] = panier

    elif intent == "confirmer":
        total = sum(item["prix"] for item in panier)
        reponse["message"] = (f"Commande confirmée ! Total : {total} FCFA. "
                               "Merci pour votre commande chez ENSPD IA PIZZA !")
        reponse["panier"] = panier
        reponse["total"] = total
        PANIERS[session_id] = []  # vider le panier après confirmation

    else:  # fallback
        reponse["message"] = ("Je n'ai pas compris votre demande. Vous pouvez : "
                               "commander une pizza, modifier, annuler, demander le prix ou confirmer.")

    return jsonify(reponse)


@app.route("/cart/<session_id>", methods=["GET"])
def get_cart(session_id):
    panier = get_panier(session_id)
    total = sum(item["prix"] for item in panier)
    return jsonify({"session_id": session_id, "panier": panier, "total": total})


@app.route("/cart/<session_id>/clear", methods=["POST"])
def clear_cart(session_id):
    PANIERS[session_id] = []
    return jsonify({"message": "Panier vidé", "session_id": session_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
