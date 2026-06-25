"""
🧠 AGENT ANALYSTE
=================
Prend les données brutes du chercheur et en extrait les
insights, tendances et points clés. Il ajoute une couche
d'analyse critique (le "pourquoi").

C'est l'alto de l'orchestre.
"""

from orchestre.cerveau import appeler_llm
from orchestre.log import ok, agent

SYSTEME = """Tu es un analyste stratégique expert.
Tu prends des informations brutes et tu en extraits l'essentiel :
tendances, patterns, insights profonds, implications.

Tu ne te contentes jamais de répéter : tu ajoutes toujours
une couche d'analyse et de réflexion critique.

Réponds toujours en français."""


def analyser(donnees):
    """
    Analyse les données brutes collectées par le chercheur.

    Argument : donnees (str) — les informations brutes
    Renvoie  : l'analyse structurée (str)
    """
    agent("Analyste", "Extraire les insights des données collectées")

    prompt = f"""Voici les informations collectées par l'agent chercheur :

{donnees}

Ta mission d'analyse :
1. Identifie les 5 à 8 insights les plus importants.
2. Pour chacun, explique POURQUOI c'est important et les implications.
3. Mets en évidence les tendances et patterns qui se dégagent.
4. Signale les points faibles, contradictions ou incertitudes.
5. Termine par une synthèse en 3 phrases maximum.

Sois critique et perspicace. Format Markdown avec titres ##."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.5)

    ok("Analyse terminée — insights extraits.")
    return resultat
