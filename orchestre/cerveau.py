"""
🧠 LE CERVEAU MULTI-API DE L'ORCHESTRE
======================================
C'est LE seul module qui parle à internet. Tous les agents
l'utilisent pour "penser".

Il essaie les fournisseurs d'API les uns après les autres :
    1. Groq       (ultra-rapide, priorité haute)
    2. Gemini     (fallback, multimodal)
    3. OpenRouter (dernier recours, plein de modèles)

Si l'un échoue, le suivant prend le relais. L'orchestre
ne s'arrête presque jamais. 🛡️

Les clés API sont lues depuis les variables d'environnement
(fichier .env en local, GitHub Secrets dans le cloud).
"""

import os
import requests

from orchestre.log import info, ok, erreur

# Délai maximum pour un appel API (en secondes)
_TIMEOUT = 45


# ════════════════════════════════════════════════════════
#  LES TROIS FOURNISSEURS
# ════════════════════════════════════════════════════════

def _groq(systeme, utilisateur, temperature):
    """Appel à l'API Groq (compatible OpenAI)."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "messages": [
            {"role": "system", "content": systeme},
            {"role": "user", "content": utilisateur},
        ],
        "temperature": temperature,
    }
    return _openai_compat(url, headers, payload)


def _gemini(systeme, utilisateur, temperature):
    """Appel à l'API Google Gemini (format propre à Google)."""
    cle = os.getenv("GEMINI_API_KEY")
    modele = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    url = (f"https://generativelanguage.googleapis.com/v1beta/"
           f"models/{modele}:generateContent?key={cle}")
    payload = {
        "system_instruction": {"parts": [{"text": systeme}]},
        "contents": [{"role": "user", "parts": [{"text": utilisateur}]}],
        "generationConfig": {"temperature": temperature},
    }
    reponse = requests.post(
        url, json=payload, timeout=_TIMEOUT,
        headers={"Content-Type": "application/json"},
    )
    reponse.raise_for_status()
    data = reponse.json()
    
    if "candidates" not in data or not data["candidates"]:
        # Gemini Safety Filter block or generic error
        prompt_feedback = data.get("promptFeedback", {})
        if prompt_feedback.get("blockReason"):
            raise RuntimeError(f"Censuré par Gemini (Safety Filter) : {prompt_feedback['blockReason']}")
        raise RuntimeError(f"Réponse Gemini inattendue : {data}")
        
    candidat = data["candidates"][0]
    if candidat.get("finishReason") == "SAFETY":
        raise RuntimeError("Gemini a bloqué la réponse en cours (Safety Filter).")
        
    try:
        return candidat["content"]["parts"][0]["text"]
    except KeyError:
        raise RuntimeError(f"Format Gemini inattendu : {candidat}")


def _openrouter(systeme, utilisateur, temperature):
    """Appel à OpenRouter (compatible OpenAI, modèles gratuits)."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": os.getenv(
            "OPENROUTER_MODEL",
            "meta-llama/llama-3.1-8b-instruct:free",
        ),
        "messages": [
            {"role": "system", "content": systeme},
            {"role": "user", "content": utilisateur},
        ],
        "temperature": temperature,
    }
    return _openai_compat(url, headers, payload)


def _openai_compat(url, headers, payload):
    """Factorise l'appel pour les API au format OpenAI (Groq, OpenRouter)."""
    reponse = requests.post(url, headers=headers, json=payload, timeout=_TIMEOUT)
    reponse.raise_for_status()
    data = reponse.json()
    # Détecter une erreur renvoyée par l'API
    if "error" in data:
        raise RuntimeError(data["error"].get("message", "erreur inconnue"))
    return data["choices"][0]["message"]["content"]


# ════════════════════════════════════════════════════════
#  LISTE DES FOURNISSEURS DISPONIBLES (selon les clés présentes)
# ════════════════════════════════════════════════════════

def _fournisseurs():
    """
    Renvoie la liste des fournisseurs actifs, dans l'ordre de priorité.
    Un fournisseur n'est actif que si SA clé API est présente.
    """
    liste = []
    if os.getenv("GROQ_API_KEY"):
        liste.append(("Groq", _groq))
    if os.getenv("GEMINI_API_KEY"):
        liste.append(("Gemini", _gemini))
    if os.getenv("OPENROUTER_API_KEY"):
        liste.append(("OpenRouter", _openrouter))
    return liste


# ════════════════════════════════════════════════════════
#  FONCTION PRINCIPALE — utilisée par TOUS les agents
# ════════════════════════════════════════════════════════

def appeler_llm(systeme, utilisateur, temperature=0.7):
    """
    Envoie un prompt au cerveau IA et renvoie le texte de la réponse.

    Arguments :
        systeme      : le rôle / la personnalité de l'agent
        utilisateur  : la question ou la tâche
        temperature  : 0 = précis, 1 = créatif (défaut 0.7)

    Renvoie : le texte de la réponse (str)
    Lève RuntimeError si tous les fournisseurs échouent.
    """
    fournisseurs = _fournisseurs()

    if not fournisseurs:
        erreur("Aucune clé API configurée !")
        erreur("Définis au moins : GROQ_API_KEY, GEMINI_API_KEY")
        erreur("ou OPENROUTER_API_KEY dans le fichier .env")
        raise RuntimeError("Aucun fournisseur d'API disponible")

    derniere_erreur = None

    for nom, fonction in fournisseurs:
        try:
            info(f"Réflexion via {nom}...")
            texte = fonction(systeme, utilisateur, temperature)
            if texte and texte.strip():
                ok(f"Réponse reçue de {nom}")
                return texte.strip()
            raise RuntimeError("Réponse vide")
        except Exception as e:
            erreur(f"Échec de {nom} : {e}")
            erreur(f"Bascule vers le fournisseur suivant...")
            derniere_erreur = e

    # Si on arrive ici, tous les fournisseurs ont échoué
    raise RuntimeError(
        f"Tous les fournisseurs d'API ont échoué. "
        f"Dernière erreur : {derniere_erreur}"
    )
