"""
✍️ AGENT RÉDACTEUR
==================
Transforme une analyse en un rapport/article final clair,
engageant et bien structuré. C'est lui qui produit le livrable.

C'est le violoncelle de l'orchestre.
"""

from orchestre.cerveau import appeler_llm
from orchestre.log import ok, agent

SYSTEME = """Tu es un rédacteur professionnel chevronné.
Tu transformes des analyses brutes en textes magnifiquement
rédigés : clairs, engageants, bien structurés et accessibles.

Ton style :
- Professionnel mais jamais ennuyeux.
- Phrases fluides et rythmées.
- Format Markdown impeccable.
- Tu réponds toujours en français."""


def rediger(analyse, sujet):
    """
    Rédige un rapport final à partir de l'analyse.

    Arguments :
        analyse : l'analyse préparée par l'analyste (str)
        sujet   : le sujet original (str)
    Renvoie  : le rapport final en Markdown (str)
    """
    agent("Rédacteur", "Composer le rapport final")

    prompt = f"""Sujet original : {sujet}

Voici l'analyse préparée par l'agent analyste :

{analyse}

Rédige un RAPPORT professionnel au format Markdown :
- Un titre principal percutant (niveau #)
- Une introduction qui pose le contexte et l'enjeu
- 3 à 5 sections avec sous-titres (niveau ##)
- Des listes à puces quand c'est pertinent
- Une conclusion avec synthèse et perspectives

Entre 500 et 1000 mots. Fluide et agréable à lire.
N'utilise PAS de délimiteur de code (``` ) au début ou à la fin."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.7)

    nb_mots = len(resultat.split())
    ok(f"Rapport initial rédigé — {nb_mots} mots.")
    return resultat


def corriger(rapport, feedback):
    """
    Applique les corrections demandées par le critique.
    """
    agent("Rédacteur", "Corriger le rapport selon les retours du critique")

    prompt = f"""Voici le rapport initial :\n{rapport}\n\nVoici les retours du critique :\n{feedback}\n\nTa mission :\nRéécris la VERSION FINALE de ce rapport en appliquant strictement ces corrections.\nAméliore ce qui a été pointé du doigt.\nGarde le format Markdown clair et aéré. Ne mets pas de commentaires, donne juste le texte final."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.5)
    nb_mots = len(resultat.split())
    ok(f"Rapport final corrigé — {nb_mots} mots.")
    return resultat
