#!/usr/bin/env python3
"""
🎯 POINT D'ENTRÉE CLI de l'orchestre
=====================================
Usage :
    python3 -m orchestre "votre tâche"
    python3 -m orchestre --sujet "L'impact de l'IA sur l'éducation"
    python3 -m orchestre --fichier donnees.csv --type data

Ce module peut être appelé :
    - en local (Termux)       → via chef.sh ou directement
    - dans le cloud (GitHub)  → via le workflow Actions
    - par le bot Telegram     → importé depuis bot/telegram_bot.py
"""

import sys
import os
import argparse
from dotenv import load_dotenv

def _charger_env():
    """Charge le fichier .env proprement."""
    chemin_env = os.path.join(os.getcwd(), ".env")
    if os.path.exists(chemin_env):
        load_dotenv(chemin_env)


# Charger les variables d'environnement du fichier .env
# (avec python-dotenv si dispo, sinon manuellement)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    _charger_env()


def main():
    """Fonction principale du CLI."""
    parseur = argparse.ArgumentParser(
        prog="orchestre",
        description="🎼 Orchestre d'agents IA multi-usages",
    )
    parseur.add_argument(
        "tache", nargs="*", help="La tâche à accomplir (texte libre)",
    )
    parseur.add_argument(
        "-s", "--sujet", help="La tâche (alternative à l'argument positionnel)",
    )
    parseur.add_argument(
        "-f", "--fichier",
        help="Lire la tâche depuis un fichier (ex: données.csv)",
    )
    parseur.add_argument(
        "-t", "--type",
        choices=["recherche", "code", "data", "contenu"],
        help="Forcer le type de tâche (ignore le routeur)",
    )
    parseur.add_argument(
        "--sans-sauvegarde", action="store_true",
        help="Ne pas sauvegarder le résultat dans output/",
    )

    args = parseur.parse_args()

    # --- Déterminer la tâche ---
    tache = None
    if args.sujet:
        tache = args.sujet
    elif args.fichier:
        try:
            with open(args.fichier, encoding="utf-8") as f:
                tache = f.read()
        except FileNotFoundError:
            print(f"❌ Fichier introuvable : {args.fichier}", file=sys.stderr)
            sys.exit(1)
    elif args.tache:
        tache = " ".join(args.tache)

    if not tache:
        parseur.print_help()
        print("\nExemples :")
        print('  python3 -m orchestre "Analyse l\'impact de l\'IA sur la santé"')
        print('  python3 -m orchestre --fichier ventes.csv --type data')
        print('  python3 -m orchestre "Écris un script Python pour trier une liste"')
        sys.exit(1)

    # --- Importer ici pour que le chargement du .env ait lieu avant ---
    from orchestre import chef
    from orchestre.log import titre, separateur, erreur, info

    # --- Bannière ---
    titre("🎼 ORCHESTRE D'AGENTS IA — V2")
    info(f"Tâche : {tache[:80]}{'...' if len(tache) > 80 else ''}")
    separateur()

    # --- Forcer le type si demandé ---
    if args.type:
        import orchestre.routeur as routeur
        # Contournement : on simule la classification du routeur
        info(f"Type forcé par l'utilisateur : {args.type.upper()}")
        # On monkey-patch la fonction router pour qu'elle renvoie le type forcé
        routeur.router = lambda t: args.type

    # --- Exécution ---
    try:
        resultat = chef.executer(tache)
    except Exception as e:
        erreur(f"Échec de l'orchestre : {e}")
        sys.exit(1)

    # --- Sauvegarde ---
    if not args.sans_sauvegarde:
        chef.sauvegarder(resultat, tache)

    # --- Affichage du résultat (sur STDOUT = le vrai livrable) ---
    titre("📄 RÉSULTAT")
    print()
    print(resultat)
    print()
    separateur()
    info("Concerto terminé avec succès ! 🎉")


if __name__ == "__main__":
    main()
