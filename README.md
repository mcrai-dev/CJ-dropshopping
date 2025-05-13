# CJ Dropshipping FastAPI Backend

Ce projet est une API backend en Python (FastAPI) pour consommer l’API officielle de CJ Dropshipping.

## Fonctionnalités principales
- Authentification et génération de token d’accès CJ Dropshipping
- Stockage temporaire du token pour les appels suivants
- Endpoints prêts à étendre pour la gestion de produits, commandes, sourcing, etc.

## Prérequis
- Python 3.8+
- Compte CJ Dropshipping (avec email et mot de passe ou appKey/appSecret selon la méthode d’authentification)

## Installation
```bash
git clone https://github.com/mcrai-dev/CJ-dropshopping.git
cd CJ-dropshopping
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement du serveur
```bash
uvicorn main:app --reload
```

## Utilisation
### 1. Obtenir un token d’accès
POST `/get-access-token`
```json
{
  "email": "votre_email_cj",
  "password": "votre_mot_de_passe_ou_hash"
}
```
Réponse :
```json
{
  "accessToken": "...",
  ...
}
```

### 2. Utiliser le token pour les autres appels (produits, commandes, etc.)

> **Note :** Le token est stocké en mémoire et utilisé automatiquement par les autres endpoints du backend.

## Personnalisation
- Ajoutez vos propres endpoints pour produits, commandes, sourcing, etc. en utilisant le token CJ.
- Pour la production, sécurisez la gestion du token (stockage, rafraîchissement, etc.).

## Dépendances principales
- fastapi
- uvicorn
- requests
- pydantic

## Auteur
- Laydam Mcrai
- [github.com/mcrai-dev/CJ-dropshopping](https://github.com/mcrai-dev/CJ-dropshopping)

---

**N’hésitez pas à ouvrir une issue ou un ticket pour toute question ou amélioration !**
# CJ-dropshopping
# CJ-dropshopping
