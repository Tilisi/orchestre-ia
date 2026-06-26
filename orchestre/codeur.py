"""
💻 AGENT CODEUR
===============
Spécialiste du code : génère, explique, corrige ou optimise
du code dans n'importe quel langage. Nouvel agent de la V2.
"""

from orchestre.cerveau import appeler_llm
from orchestre.log import ok, agent

SYSTEME = """Tu es un ingénieur logiciel expert et pédagogue.
Tu écris du code propre, commenté et idiomatique, dans n'importe
quel langage. Tu expliques toujours ton raisonnement de façon
claire, comme un mentor patient.

Règles :
- Réponds en français (commentaires et explications).
- Le code lui-même reste dans son langage d'origine.
- Inclus toujours des commentaires explicatifs.
- Termine par une brève explication du fonctionnement."""


def coder(tache):
    """
    Génère, explique ou corrige du code selon la demande.

    Argument : tache (str) — la demande de l'utilisateur
    Renvoie  : le code + explications (str)
    """
    agent("Codeur", "Générer / expliquer / corriger du code")

    prompt = f"""Voici la demande de l'utilisateur :

{tache}

Ta mission :
1. Si c'est une demande de création : écris le code complet et fonctionnel.
2. Si c'est une demande d'explication : explique le code pas à pas.
3. Si c'est une demande de correction : identifie le bug et corrige-le.

ATTENTION SÉCURITÉ :
Si le code généré interagit avec le système d'exploitation, ajoute toujours
un avertissement clair invitant l'utilisateur à ne pas l'exécuter aveuglément.

Fournis :
- Le code dans un bloc Markdown avec le bon langage (```python, ```bash, etc.)
- Des commentaires clairs dans le code
- Une explication finale du fonctionnement et d'éventuels conseils

Sois rigoureux et professionnel."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.3)

    ok("Code généré avec succès.")
    return resultat
