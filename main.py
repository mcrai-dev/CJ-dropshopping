from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import requests
import time

app = FastAPI(title="CJ Dropshipping E-commerce API")

CJ_API_BASE = "https://developers.cjdropshipping.com"
CJ_TOKEN_ENDPOINT = f"{CJ_API_BASE}/api2.0/v1/authentication/getAccessToken"

# Stockage du token CJ en mémoire
cj_access_token = None
cj_token_expiry = 0

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/get-access-token")
def get_access_token(auth: AuthRequest):
    data = {"email": auth.email, "password": auth.password}
    resp = requests.post(CJ_TOKEN_ENDPOINT, json=data)
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'obtention du token: {resp.text}")
    resp_json = resp.json()
    if resp_json.get("code") != 200 or not resp_json.get("data"):
        raise HTTPException(status_code=502, detail=f"Erreur d'authentification CJ: {resp.text}")
    # Stocker le token et l'expiration en mémoire
    global cj_access_token, cj_token_expiry
    cj_access_token = resp_json["data"]["accessToken"]
    expires_in = resp_json["data"].get("expiresIn", 7200)
    cj_token_expiry = int(time.time()) + expires_in - 60
    return resp_json["data"]

# Helper pour obtenir un token valide
def get_valid_token():
    global cj_access_token, cj_token_expiry
    if not cj_access_token or int(time.time()) > cj_token_expiry:
        raise HTTPException(status_code=401, detail="Token CJ manquant ou expiré. Merci d'appeler /get-access-token.")
    return cj_access_token

# Helper pour appeler l'API CJ Dropshipping
def cj_api_get(endpoint: str, params: dict = {}):
    token = get_valid_token()
    headers = {"CJ-Access-Token": token}
    url = f"{CJ_API_BASE}{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Erreur API CJ: {response.text}")
    return response.json()


@app.get("/products", summary="Liste des produits")
def list_products(keyword: Optional[str] = Query(None), page: int = 1, pageSize: int = 10):
    """
    Retourne une liste de produits CJ Dropshipping.
    """
    params = {"keyword": keyword, "page": page, "pageSize": pageSize}
    data = cj_api_get("/api2.0/v1/product/list", params)
    return data

@app.get("/products/{product_id}", summary="Détail d'un produit")
def product_detail(product_id: str):
    data = cj_api_get(f"/api2.0/v1/product/{product_id}")
    return data

@app.post("/cart/add", summary="Ajouter un produit au panier")
def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append({"product_id": product_id, "quantity": quantity})
    return {"message": "Produit ajouté au panier", "cart": carts[user_id]}

@app.get("/cart", summary="Voir le panier")
def view_cart(user_id: str):
    return {"cart": carts.get(user_id, [])}

@app.post("/order", summary="Créer une commande (achat)")
def create_order(user_id: str):
    cart = carts.get(user_id, [])
    if not cart:
        raise HTTPException(status_code=400, detail="Le panier est vide.")
    # Ici, on simulerait l'appel à l'API de création de commande CJ
    # (À implémenter selon la doc CJ Dropshipping)
    # On vide le panier après commande
    carts[user_id] = []
    return {"message": "Commande créée", "order": cart}
