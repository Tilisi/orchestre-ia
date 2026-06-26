"""
🔬 AGENT CRITIQUE
=================
Le 6e agent de l'orchestre. Il relit le rapport du rédacteur
et l'améliore : corrige les erreurs, ajoute des nuances,
renforce la qualité.

C'est le relecteur exigeant de l'orchestre.
"""

from orchestre.cerveau import appeler_llm
from orchestre.log import ok, agent, attention

SYSTEME = """Tu es un critique éditorial exigeant et bienveillant.
Tu relis un rapport et tu l'améliores sur 3 axes :
1. La clarté et la fluidité du style.
2. La solidité des arguments (manque-t-il des nuances ?).
3. La structure et la lisibilité (titres, listes, transitions).

Tu ne détruis jamais le travail : tu le polis. Tu corriges
les répétitions, les phrases maladroites, et tu ajoutes
des transitions entre les sections.

Réponds toujours en français. Renvoie la VERSION AMÉLIORÉE
complète du rapport (pas juste tes commentaires)."""


def critiquer(rapport, sujet):
    """
    Relit et améliore le rapport final.

    Arguments :
        rapport : le rapport produit par le rédacteur (str)
        sujet   : le sujet original (str)
    Renvoie  : la version améliorée du rapport (str)
    """
    agent("Critique", "Relire et polir le rapport final")

    prompt = f"""Sujet de recherche : {sujet}

Voici le rapport à relire et améliorer :

{rapport}

Ta mission : renvoie la VERSION FINALE AMÉLIORÉE de ce rapport.

Améliore :
- La fluidité et le style (supprime les répétitions, les phrases lourdes).
- Les transitions entre sections (ajoute des phrases de liaison).
- La précision du vocabulaire.
- La conclusion (rendue plus percutante).

Garde la même structure (titres ##) et la même longueur générale.
N'utilise PAS de délimiteur de code au début ou à la fin.
Renvoie UNIQUEMENT le rapport amélioré, prêt à être lu."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.4)

    nb_mots = len(resultat.split())
    ok(f"Rapport amélioré — {nb_mots} mots (version finale).")
    return resultat
