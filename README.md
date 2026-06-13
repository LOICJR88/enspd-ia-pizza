# 🍕 ENSPD IA PIZZA - Assistant Vocal de Commande

## Description
Système d'IA conversationnelle (NLP) pour la prise de commandes de pizza,
développé pour le restaurant fictif **ENSPD IA PIZZA**.
L'IA comprend le langage naturel (français) pour gérer commandes, modifications,
annulations et calcul du prix, via une API Flask et une interface Excel.

## Architecture
Client (Excel / Voix)

|

v

API Flask (app.py)

|

v

Moteur NLP (nlp/intents.py)

|

v

Panier en mémoire (session_id)
## Structure du projet
enspd-ia-pizza/

├── app.py                 # API Flask principale

├── nlp/

│   ├── init.py

│   └── intents.py          # Moteur NLP (intents + entités)

├── data/

│   └── menu.json            # Menu, tailles, extras

├── excel/

│   ├── commande_pizza.xlsx  # Interface Excel

│   ├── macro.vba            # Macro VBA d'appel API

│   └── powerquery.txt        # Alternative Power Query

└── README.md
## Installation locale
```bash
pip install flask flask-cors pandas openpyxl
python app.py
```
L'API démarre sur `http://localhost:5000`

## Endpoints API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page d'accueil / liste des endpoints |
| GET | `/menu` | Retourne le menu complet (JSON) |
| POST | `/order` | Envoie un texte client, retourne intent + réponse |
| GET | `/cart/<session_id>` | Récupère le panier d'une session |
| POST | `/cart/<session_id>/clear` | Vide le panier d'une session |

### Exemple de requête `/order`
```json
POST /order
{
  "session_id": "client1",
  "text": "Je veux une grande margherita avec des olives"
}
```

### Exemple de réponse
```json
{
  "session_id": "client1",
  "intent": "commander",
  "entites": {
    "pizza": "margherita",
    "taille": "grande",
    "quantite": 1,
    "extras": ["olives"]
  },
  "message": "1 x pizza margherita (grande) ajoutée(s) au panier pour 6300 FCFA.",
  "panier": [...]
}
```

## Intentions (Intents) gérées
- `saluer` : salutations
- `menu` : affichage du menu
- `commander` : ajouter une pizza au panier
- `modifier` : modifier le dernier article (taille, extras, pizza)
- `annuler` : retirer le dernier article
- `prix` : calculer le total du panier
- `confirmer` : valider la commande et vider le panier
- `fallback` : intention non reconnue

## Entités extraites
- **pizza** : margherita, reine, vegetarienne, quatre fromages, pepperoni
- **taille** : petite, moyenne, grande, extra-large
- **quantite** : nombre (chiffres ou lettres : "deux", "trois"...)
- **extras** : olives, fromage supplementaire, champignons, oignons, pepperoni, ananas

## Intégration Excel
1. Démarrer l'API Flask (via Colab + ngrok, ou en local)
2. Copier l'URL publique (ngrok) de l'API
3. Ouvrir `excel/commande_pizza.xlsx`
4. Insérer la macro VBA (`excel/macro.vba`) dans Alt+F11, en remplaçant l'URL
   OU configurer Power Query avec `excel/powerquery.txt`
5. Saisir le message client en B4, exécuter la macro, voir la réponse en B5

## Tests réalisés
Voir la section "Tests fonctionnels" du rapport. Tous les scénarios suivants
ont été validés :
- Commande simple
- Commande multi-pizza
- Modification de taille
- Ajout d'extras
- Calcul de prix
- Annulation
- Confirmation
- Gestion du fallback

## Auteurs
Projet réalisé dans le cadre du cours "Amélioration de l'Assistance à la
Clientèle avec Des Services Vocaux" - ENSPD.

## Inspiration
Basé sur le template [Sheng-Kai-IBM/Embeddable-AI-Voice-Ordering](https://github.com/Sheng-Kai-IBM/Embeddable-AI-Voice-Ordering)
