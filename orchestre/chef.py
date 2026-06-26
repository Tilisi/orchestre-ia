"""
🎼 LE CHEF D'ORCHESTRE
======================
C'est lui qui coordonne tout. Il :
  1. demande au routeur quel type de tâche c'est
  2. active les bons agents, dans le bon ordre
  3. renvoie le résultat final

Pipelines selon le type de tâche :

    recherche → Chercheur → Analyste → Rédacteur
    code      → Codeur
    data      → Data → Rédacteur
    contenu   → Rédacteur
    autre     → Rédacteur (réponse directe)
"""

import os
import datetime

from orchestre import routeur, chercheur, analyseur, redacteur, codeur, data_agent, critique
from orchestre.log import titre, ok, separateur, info, erreur


def _pipeline_recherche(tache):
    """Pipeline complet pour une tâche de recherche."""
    donnees = chercheur.chercher(tache)
    analyse = analyseur.analyser(donnees)
    rapport = redacteur.rediger(analyse, tache)
    rapport = critique.critiquer(rapport, tache)  # 🔬 6e agent
    return rapport


def _pipeline_data(tache):
    """Pipeline pour une analyse de données."""
    analyse = data_agent.analyser(tache)
    rapport = redacteur.rediger(analyse, "Analyse de données")
    rapport = critique.critiquer(rapport, "Analyse de données")  # 🔬
    return rapport


def _pipeline_contenu(tache):
    """Pipeline pour la création de contenu."""
    rapport = redacteur.rediger(tache, tache)
    rapport = critique.critiquer(rapport, tache)  # 🔬
    return rapport


def _pipeline_code(tache):
    """Pipeline pour les tâches de code."""
    return codeur.coder(tache)


def _pipeline_defaut(tache):
    """Pipeline par défaut : réponse directe du rédacteur."""
    return redacteur.rediger(tache, tache)


# Table de dispatch : type → fonction
_PIPELINES = {
    "recherche": _pipeline_recherche,
    "data": _pipeline_data,
    "contenu": _pipeline_contenu,
    "code": _pipeline_code,
    "autre": _pipeline_defaut,
}


def executer(tache):
    """
    Exécute la tâche complète via le bon pipeline d'agents.

    Argument : tache (str) — la demande de l'utilisateur
    Renvoie  : le résultat final (str)
    """
    if not tache or not tache.strip():
        raise ValueError("Aucune tâche fournie.")

    # --- 1. Le routeur détermine le type ---
    titre("Détection du type de tâche")
    type_tache = routeur.router(tache)
    info(f"Tâche classée : {type_tache.upper()}")

    # --- 2. Sélection du pipeline ---
    pipeline = _PIPELINES.get(type_tache, _pipeline_defaut)
    separateur()

    # --- 3. Exécution ---
    resultat = pipeline(tache)

    if not resultat:
        raise RuntimeError("Le pipeline n'a produit aucun résultat.")

    return resultat


def sauvegarder(contenu, sujet, dossier=None):
    """
    Sauvegarde le résultat dans un fichier Markdown horodaté.

    Arguments :
        contenu : le texte à sauvegarder
        sujet   : pour générer un nom de fichier
        dossier : dossier de sortie (défaut : ./output)
    Renvoie : le chemin du fichier créé.
    """
    if dossier is None:
        dossier = os.getenv("ORCHESTRE_OUTPUT", "./output")
    os.makedirs(dossier, exist_ok=True)

    # Nom de fichier propre : on garde alphanumérique + _
    nom = "".join(c if c.isalnum() else "_" for c in sujet)[:40]
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    chemin = os.path.join(dossier, f"resultat_{nom}_{horodatage}.md")

    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)

    ok(f"Résultat sauvegardé : {chemin}")
    return chemin
