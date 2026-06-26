"""
🔍 AGENT CHERCHEUR  (avec vrai scraping web)
============================================
Explore un sujet, récupère du vrai contenu sur le web via
DuckDuckGo, scrape réellement les pages trouvées, puis synthétise le tout avec le cerveau IA.
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

_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
}


def chercher_web(requete, max_extraits=5):
    """
    Effectue une recherche web sur DuckDuckGo, extrait les vrais liens,
    et scrape le contenu de ces pages.
    """
    info(f"Recherche web : « {requete} »")
    try:
        url = "https://html.duckduckgo.com/html/"
        params = {"q": requete, "kl": "fr-fr"}
        reponse = requests.post(url, data=params, headers=_HEADERS, timeout=15)
        reponse.raise_for_status()
    except Exception as e:
        attention(f"Recherche web (DuckDuckGo) impossible ({e}). On continue sans web.")
        return ""

    soupe = BeautifulSoup(reponse.text, "html.parser")
    liens = []
    
    # Extraire les URL réelles des résultats
    for a in soupe.find_all("a", class_="result__url"):
        href = a.get("href", "")
        if href.startswith("http") and "duckduckgo" not in href:
            if href not in liens:
                liens.append(href)

    if not liens:
        attention("Aucun lien exploitable trouvé. Extraction de fallback.")
        texte = soupe.get_text(separator="\n")
        return texte[:2000]
        
    ok(f"{len(liens)} liens web trouvés. Scraping des 2 premiers...")
    textes_scrapes = []
    
    # Scraper les 2 premières URLs
    for lien in liens[:2]:
        try:
            r = requests.get(lien, headers=_HEADERS, timeout=10)
            if r.status_code == 200:
                s = BeautifulSoup(r.text, "html.parser")
                # Supprimer les balises inutiles
                for elem in s(["script", "style", "nav", "footer", "header"]):
                    elem.extract()
                texte_propre = s.get_text(separator="\n")
                # Nettoyer les espaces multiples
                lignes = [ligne.strip() for ligne in texte_propre.splitlines() if ligne.strip()]
                texte_final = "\n".join(lignes)
                
                # Garder 3000 caractères par page pour éviter la saturation du contexte
                textes_scrapes.append(f"--- SOURCE : {lien} ---\n{texte_final[:3000]}")
        except Exception as e:
            attention(f"Impossible de lire {lien} ({e})")
            continue

    if not textes_scrapes:
        return "Aucun contenu web extrait."

    ok("Pages web analysées avec succès.")
    return "\n\n".join(textes_scrapes)


def chercher(sujet):
    agent("Chercheur", "Explorer le sujet + recherche web réelle")
    contexte_web = chercher_web(sujet)

    prompt = f"""Sujet de recherche : {sujet}

Voici des extraits récents récupérés sur le web (DuckDuckGo + Scraping) :
{contexte_web}

À partir de tes propres connaissances ET de ces extraits web,
rédige un dossier de recherche complet sur le sujet.
Ignore les menus et textes techniques parasites du web (ex: 'accepter les cookies')."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.3)
    ok("Recherche terminée — dossier compilé.")
    return resultat
