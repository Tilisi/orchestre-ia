"""
🔍 AGENT CHERCHEUR  (avec scraping web réel)
============================================
Explore un sujet, récupère du vrai contenu sur le web via
DuckDuckGo, puis synthétise le tout avec le cerveau IA.

C'est le 1er violon de l'orchestre.
"""

import requests
from bs4 import BeautifulSoup

from orchestre.cerveau import appeler_llm
from orchestre.log import info, ok, attention, agent

SYSTEME = """Tu es un agent de recherche expert et méthodique.
Ta mission est d'explorer un sujet en profondeur, de le découper
en sous-questions clés, puis de rassembler des informations
détaillées et factuelles pour chacune.

Règles :
- Réponds toujours en français.
- Sois factuel, précis et complet.
- Donne des chiffres, des dates, des exemples concrets.
- Structure ta réponse avec des titres (##)."""

# --- Entête pour se faire passer pour un navigateur ---
# (sinon certains sites refusent les requêtes de scripts)
_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Linux; Android 14; Redmi 14) "
                   "AppleWebKit/537.36 Mobile Safari/537.36")
}


def chercher_web(requete, max_extraits=5):
    """
    Effectue une recherche web sur DuckDuckGo et renvoie du texte exploitable.

    Arguments :
        requete      : la recherche à effectuer
        max_extraits : nombre maximum de résultats à garder

    Renvoie : une chaîne de texte (les extraits concaténés),
              ou une chaîne vide si rien trouvé.
    """
    info(f"Recherche web : « {requete} »")
    try:
        url = "https://lite.duckduckgo.com/lite/"
        params = {"q": requete, "kl": "fr-fr"}
        reponse = requests.get(url, params=params, headers=_HEADERS, timeout=15)
        reponse.raise_for_status()
    except Exception as e:
        attention(f"Recherche web impossible ({e}). On continue sans web.")
        return ""

    # Extraire le texte propre avec BeautifulSoup
    soupe = BeautifulSoup(reponse.text, "html.parser")
    texte = soupe.get_text(separator="\n")

    # Nettoyer : enlever les lignes vides et le bruit, garder les meilleures
    lignes = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if len(ligne) < 30:  # trop court = probablement du bruit
            continue
        if any(mot in ligne.lower() for mot in (
            "duckduckgo", "privacy", "newsletter", "javascript",
            "cookie", "about", "settings",
        )):
            continue
        lignes.append(ligne)
        if len(lignes) >= max_extraits:
            break

    if not lignes:
        attention("Aucun extrait web exploitable trouvé.")
        return ""

    ok(f"{len(lignes)} extraits web récupérés.")
    return "\n".join(f"• {l}" for l in lignes)


def chercher(sujet):
    """
    Lance la recherche complète sur un sujet.

    Étapes :
      1. Scraping web pour du contexte réel et récent
      2. Le cerveau synthétise le sujet + le contexte web

    Argument : sujet (str)
    Renvoie  : les données collectées (str)
    """
    agent("Chercheur", "Explorer le sujet + recherche web réelle")

    # --- 1. Récupérer du contexte web ---
    contexte_web = chercher_web(sujet)

    # --- 2. Construire le prompt ---
    if contexte_web:
        prompt = f"""Voici le sujet de recherche à explorer :

━━━ {sujet} ━━━

Pour t'aider, voici des extraits trouvés sur le web (contexte réel) :

{contexte_web}

Ta mission :
1. Décompose ce sujet en 4 à 6 sous-questions essentielles.
2. Pour chacune, rédige une réponse détaillée (faits, chiffres, exemples).
3. Si le sujet implique des évolutions, donne les tendances actuelles.
4. Termine par « Points clés » listant les 5 découvertes majeures.

Format Markdown avec un titre ## par sous-question."""
    else:
        prompt = f"""Voici le sujet de recherche à explorer :

━━━ {sujet} ━━━

Ta mission :
1. Décompose ce sujet en 4 à 6 sous-questions essentielles.
2. Pour chacune, rédige une réponse détaillée (faits, chiffres, exemples).
3. Termine par « Points clés » listant les 5 découvertes majeures.

Format Markdown avec un titre ## par sous-question."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.4)

    nb_mots = len(resultat.split())
    ok(f"Recherche terminée — {nb_mots} mots collectés.")
    return resultat
