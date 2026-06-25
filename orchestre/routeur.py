"""
🔀 LE ROUTEUR
=============
C'est l'aiguilleur de l'orchestre. Il examine la demande de
l'utilisateur et détermine quel(s) agent(s) activer.

Il utilise le cerveau IA pour classifier la tâche en :
    - "recherche"  → Chercheur → Analyste → Rédacteur
    - "code"       → Codeur
    - "data"       → Data → Rédacteur
    - "contenu"    → Rédacteur (article, post, email...)
    - "autre"      → Rédacteur (réponse directe)

En cas d'incertitude de l'IA, il retombe sur "recherche"
(par défaut, le plus complet).
"""

from orchestre.cerveau import appeler_llm
from orchestre.log import info, ok, attention

SYSTEME = """Tu es un routeur (classifier). Tu analyses une demande
et tu renvoies UN SEUL mot parmi :
- recherche  (explorer un sujet, comprendre, synthétiser des infos)
- code       (écrire, expliquer, corriger du code ou un script)
- data       (analyser des données, des chiffres, un CSV)
- contenu    (rédiger un article, un post, un email, un texte créatif)

Tu réponds UNIQUEMENT par ce mot, rien d'autre. Pas de phrase,
pas de ponctuation, juste le mot."""

# Mots-clés pour un pré-filtre rapide (évite un appel API si évident)
_MOTS_CLES = {
    "code": ["code", "script", "fonction", "bug", "python", "bash", "javascript",
             "html", "css", "java", "programme", "compiler", "erreur code",
             "algorithme", "regex"],
    "data": ["csv", "données", "statistique", "moyenne", "médiane",
             "analyse de données", "tableau", "chiffres", "excel"],
    "contenu": ["article", "post", "email", "rédige", "écris un texte",
                "newsletter", "slogan", "bio", "description produit"],
}


def _classification_rapide(tache):
    """
    Classification par mots-clés (gratuite, sans appel API).
    Renvoie un type si évident, sinon None.
    """
    tache_basse = tache.lower()
    for type_tache, mots in _MOTS_CLES.items():
        if any(mot in tache_basse for mot in mots):
            return type_tache
    return None


def router(tache):
    """
    Détermine le type de tâche.

    Argument : tache (str)
    Renvoie  : un type parmi {"recherche", "code", "data", "contenu", "autre"}
    """
    # --- 1. Essayer la classification rapide ---
    type_rapide = _classification_rapide(tache)
    if type_rapide:
        info(f"Type détecté (mots-clés) : {type_rapide}")
        return type_rapide

    # --- 2. Sinon, demander au cerveau ---
    try:
        info("Classification par IA en cours...")
        reponse = appeler_llm(SYSTEME, tache, temperature=0.0)
        type_ia = reponse.strip().lower().split()[0]  # 1er mot
        # Nettoyer (enlever ponctuation éventuelle)
        type_ia = "".join(c for c in type_ia if c.isalpha())
        types_valides = {"recherche", "code", "data", "contenu"}
        if type_ia in types_valides:
            ok(f"Type détecté (IA) : {type_ia}")
            return type_ia
        attention(f"Classification IA floue (« {reponse} »). Défaut : recherche.")
    except Exception as e:
        attention(f"Classification IA impossible ({e}). Défaut : recherche.")

    return "recherche"
