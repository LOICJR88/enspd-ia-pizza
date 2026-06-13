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


## Phase 1 — Analyse du template GitHub (Sheng-Kai-IBM/Embeddable-AI-Voice-Ordering)

Le dépôt officiel a été cloné et analysé. Constats :

- Le template utilise **Watson Speech-to-Text / Text-to-Speech** via des
  endpoints `sn-watson-stt` / `sn-watson-tts` réservés à l'environnement
  **IBM Skills Network Labs** — non accessibles publiquement, donc non
  réutilisables tels quels hors de ce lab.
- Architecture multi-pages séquentielle (adresse → garniture → confirmation),
  extraction par mots-clés simples, sans gestion de panier ni d'intents
  multiples (pas de modification/annulation/fallback).
- Pas d'API JSON réutilisable : la logique métier est mêlée au rendu HTML.

**Choix retenu** : conserver le **principe d'architecture** (Flask +
commande vocale de pizza) mais réimplémenter avec :
- un moteur NLP maison plus complet (8 intents, 4 types d'entités, panier,
  fallback),
- une API REST JSON découplée et réutilisable,
- la reconnaissance vocale via la **Web Speech API du navigateur**
  (gratuite, sans dépendance cloud propriétaire), assurant la même
  fonctionnalité "commande par la voix" de manière portable et reproductible.

## Interface Web (Chat + Voix)

Une interface de chat est servie directement par Flask à la racine `/` :

- Champ texte pour taper une commande
- Bouton micro 🎤 (reconnaissance vocale en français via Web Speech API,
  compatible Chrome/Edge)
- Affichage en temps réel du panier et du total
- Appelle en arrière-plan l'API `/order` et `/cart/<session_id>`

Accès : ouvrir l'URL ngrok (ou localhost:5000 en local) dans Chrome/Edge.

## Endpoints mis à jour

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Interface de chat (HTML + voix) |
| GET | `/api` | Informations API (JSON) |
| GET | `/menu` | Menu complet (JSON) |
| POST | `/order` | Traite un message client |
| GET | `/cart/<session_id>` | Panier d'une session |
| POST | `/cart/<session_id>/clear` | Vide le panier |
