"""
📊 AGENT DATA
=============
Analyse des données (CSV, texte tabulaire, listes de nombres).
Combine de VRAIES statistiques calculées en Python (moyenne,
médiane, écart-type...) avec l'intelligence du cerveau IA
pour interpréter les résultats.

Nouvel agent de la V2.
"""

import csv
import io
import statistics as stats

from orchestre.cerveau import appeler_llm
from orchestre.log import info, ok, attention, agent

SYSTEME = """Tu es un analyste de données expert.
Tu interprètes des statistiques et tu en tires des insights
actionnables. Tu expliques ce que les chiffres signifient
en termes simples, pour un public non technique.

Réponds toujours en français, avec un format Markdown clair."""


def _extraire_nombres(texte):
    """Tente d'extraire toutes les valeurs numériques d'un texte."""
    nombres = []
    for mot in texte.replace(",", " ").split():
        try:
            # gère les nombres avec un point décimal
            nombres.append(float(mot))
        except ValueError:
            continue
    return nombres


def _analyser_csv(contenu):
    """
    Analyse un contenu CSV : compte lignes/colonnes et calcule
    des statistiques sur chaque colonne numérique.
    """
    lecteur = csv.reader(io.StringIO(contenu))
    lignes = list(lecteur)
    if len(lignes) < 2:
        return None

    entetes = lignes[0]
    donnees = lignes[1:]

    rapport_lines = [
        f"- Lignes de données : {len(donnees)}",
        f"- Colonnes : {len(entetes)} → {', '.join(entetes)}",
        "",
        "Statistiques par colonne numérique :",
    ]

    # Transposer pour analyser colonne par colonne
    for col_index, entete in enumerate(entetes):
        valeurs_col = []
        for ligne in donnees:
            if col_index < len(ligne):
                try:
                    valeurs_col.append(float(ligne[col_index]))
                except ValueError:
                    pass
        if len(valeurs_col) >= 2:
            rapport_lines.append(
                f"  • {entete} : "
                f"min={min(valeurs_col):.2f}, max={max(valeurs_col):.2f}, "
                f"moyenne={stats.mean(valeurs_col):.2f}, "
                f"médiane={stats.median(valeurs_col):.2f}, "
                f"écart-type={stats.stdev(valeurs_col):.2f}"
            )

    if len(rapport_lines) <= 3:
        return None
    return "\n".join(rapport_lines)


def analyser(tache):
    """
    Analyse des données fournies par l'utilisateur.

    Argument : tache (str) — les données + la question
    Renvoie  : l'interprétation complète (str)
    """
    agent("Data", "Analyser les données et interpréter les résultats")

    # --- 1. Vraies statistiques calculées en Python ---
    stats_texte = ""

    # Tenter une analyse CSV
    analyse_csv = _analyser_csv(tache)
    if analyse_csv:
        info("Format CSV détecté — calcul des statistiques...")
        stats_texte = f"Données tabulaires (CSV) détectées :\n{analyse_csv}"
    else:
        # Sinon, extraire les nombres bruts
        nombres = _extraire_nombres(tache)
        if len(nombres) >= 2:
            info(f"{len(nombres)} valeurs numériques détectées.")
            ecart_type = stats.stdev(nombres)  # OK : >= 2 valeurs garanties
            stats_texte = (
                f"Valeurs numériques détectées ({len(nombres)}) :\n"
                f"- Min : {min(nombres):.2f}\n"
                f"- Max : {max(nombres):.2f}\n"
                f"- Moyenne : {stats.mean(nombres):.2f}\n"
                f"- Médiane : {stats.median(nombres):.2f}\n"
                f"- Écart-type : {ecart_type:.2f}"
            )
        else:
            attention("Pas assez de données numériques pour des statistiques.")

    # --- 2. Le cerveau interprète ---
    prompt = f"""Voici la demande de l'utilisateur :

{tache}
"""
    if stats_texte:
        prompt += f"""
Voici les statistiques réelles calculées par Python (à interpréter) :

{stats_texte}

Ta mission :
1. Explique clairement ce que signifient ces chiffres.
2. Identifie les tendances, anomalies ou points notables.
3. Formule des recommandations ou conclusions actionnables.
4. Si l'utilisateur posait une question précise, réponds-y."""
    else:
        prompt += """
Les données ne contiennent pas assez de nombres pour des statistiques.
Aide l'utilisateur à structurer/analyser ses données qualitativement."""

    resultat = appeler_llm(SYSTEME, prompt, temperature=0.3)

    ok("Analyse de données terminée.")
    return resultat
