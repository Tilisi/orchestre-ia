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

SYSTEME = """Tu es un critique éditorial impitoyable et exigeant.
Tu relis un rapport et tu listes ses défauts : erreurs logiques, manque de clarté,
oublis, fautes, lourdeurs.

ATTENTION : NE RÉÉCRIS PAS LE TEXTE ! 
Donne UNIQUEMENT une liste à puces des points à corriger.
Ton retour doit être sous la forme :
- Le paragraphe X manque de clarté sur...
- La transition Y est abrupte...
"""


def critiquer(rapport, sujet):
    """
    Lit le rapport et fournit une liste de retours critiques (feedback).
    """
    agent("Critique", "Relire et fournir un feedback constructif")

    prompt = f"""Sujet : {sujet}

Voici le rapport actuel :
{rapport}

Ta mission : fournis tes recommandations d'amélioration sous forme de liste à puces. Ne réécris pas le rapport, pointe juste ce qu'il faut corriger."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.3)
    ok("Feedback critique généré.")
    return resultat
