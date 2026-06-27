"""
🔍 AGENT CHERCHEUR  (avec vrai scraping web)
============================================
Explore un sujet, récupère du vrai contenu sur le web via DuckDuckGo,
scrape les pages trouvées, puis synthétise avec le cerveau IA.
"""

from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlparse

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
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
}


def _normaliser_url_duckduckgo(href: str) -> str:
    """Convertit les redirections DuckDuckGo en URL cible quand possible."""
    if not href:
        return ""
    href = href.strip()
    if href.startswith("//"):
        href = "https:" + href

    parsed = urlparse(href)
    query = parse_qs(parsed.query)
    if "uddg" in query and query["uddg"]:
        return unquote(query["uddg"][0])
    return href


def _extraire_liens_duckduckgo(html: str, limite: int = 5) -> list[str]:
    """
    Extrait les liens de résultats DuckDuckGo de manière plus robuste que
    la dépendance à une seule classe CSS.
    """
    soupe = BeautifulSoup(html, "html.parser")
    liens: list[str] = []

    for a in soupe.find_all("a"):
        classes = set(a.get("class") or [])
        href = _normaliser_url_duckduckgo(a.get("href", ""))
        if not href.startswith("http"):
            continue
        host = urlparse(href).netloc.lower()
        if "duckduckgo.com" in host:
            continue

        est_resultat = bool(classes & {"result__a", "result__url"})
        # Fallback : garder aussi les liens externes présents dans la zone de résultats.
        parent_text = " ".join(a.get_text(" ", strip=True).split())
        if est_resultat or parent_text:
            if href not in liens:
                liens.append(href)
        if len(liens) >= limite:
            break
    return liens


def _nettoyer_html(html: str, limite: int = 3000) -> str:
    """Extrait un texte propre d'une page HTML."""
    soupe = BeautifulSoup(html, "html.parser")
    for elem in soupe(["script", "style", "nav", "footer", "header", "noscript"]):
        elem.extract()
    lignes = [ligne.strip() for ligne in soupe.get_text(separator="\n").splitlines() if ligne.strip()]
    return "\n".join(lignes)[:limite]


def chercher_web(requete, max_extraits=5):
    """
    Effectue une recherche web sur DuckDuckGo, extrait les liens,
    et scrape le contenu des premières pages.
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

    liens = _extraire_liens_duckduckgo(reponse.text, limite=max_extraits)
    if not liens:
        attention("Aucun lien exploitable trouvé. Extraction de fallback.")
        return _nettoyer_html(reponse.text, limite=2000)

    nb_pages = min(2, len(liens))
    ok(f"{len(liens)} liens web trouvés. Scraping des {nb_pages} premiers...")
    textes_scrapes = []

    for lien in liens[:nb_pages]:
        try:
            r = requests.get(lien, headers=_HEADERS, timeout=10)
            r.raise_for_status()
            texte_final = _nettoyer_html(r.text, limite=3000)
            if texte_final:
                textes_scrapes.append(f"--- SOURCE : {lien} ---\n{texte_final}")
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
