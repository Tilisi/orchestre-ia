#!/usr/bin/env python3
"""
🚀 POINk D'ENTRÉE CLOUD — Bot Telegram + Keep-alive
====================================================
Lance EN MÊME TEMPS :
  1. Le serveur web keep-alive (empêche Render d'endormir)
  2. Le bot Telegram (écoute tes messages et exécute l'orchestre)

Ce fichier est utilisé par Render/Koyeb pour démarrer le bot.
Le bot tourne en MODE LOCAL : il exécute l'orchestre directement
sur le serveur cloud (pas besoin de GitHub Actions).

Variables d'environnement requises :
  - TELEGRAM_BOT_TOKEN
  - GROQ_API_KEY (ou GEMINI_API_KEY / OPENROUTER_API_KEY)
  - TELEGRAM_CHAT_ID (optionnel, pour restreindre l'accès)
"""

import os
import sys

# Permettre l'import du package orchestre/
_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJET not in sys.path:
    sys.path.insert(0, _PROJET)

# Charger le .env manuellement si présent (en local)
_ENV = os.path.join(_PROJET, ".env")
if os.path.exists(_ENV):
    with open(_ENV, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#") and "=" in ligne:
                k, _, v = ligne.partition("=")
                k = k.strip()
                v = v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                    v = v[1:-1]
                os.environ.setdefault(k, v)

import telebot
from orchestre.log import info, ok, erreur
from bot.keepalive import demarrer_keepalive

# --- Configuration ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID_AUTORISE = os.getenv("TELEGRAM_CHAT_ID", "")
PORT = int(os.getenv("PORT", "10000"))

if not TOKEN:
    print("ERREUR: TELEGRAM_BOT_TOKEN manquant")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)


# ════════════════════════════════════════════════════════
#  KEEP-ALIVE (empêche le cloud d'endormir le bot)
# ════════════════════════════════════════════════════════
demarrer_keepalive(PORT)
ok(f"Serveur keep-alive démarré sur le port {PORT}")


# ════════════════════════════════════════════════════════
#  COMMANDES DU BOT
# ════════════════════════════════════════════════════════

def _autorise(message):
    if not CHAT_ID_AUTORISE:
        return True
    return str(message.chat.id) == str(CHAT_ID_AUTORISE)


def _envoyer(chat_id, texte):
    texte = texte or "(vide)"
    limite = 4000
    if len(texte) <= limite:
        bot.send_message(chat_id, texte)
        return
    morceaux = [texte[i:i + limite] for i in range(0, len(texte), limite)]
    total = len(morceaux)
    for i, m in enumerate(morceaux, start=1):
        bot.send_message(chat_id, "(part {}/{})\n\n{}".format(i, total, m))


def _executer_orchestre(sujet):
    """Exécute l'orchestre directement sur le serveur cloud."""
    try:
        from orchestre import chef
        resultat = chef.executer(sujet)
        chef.sauvegarder(resultat, sujet)
        return True, resultat
    except Exception as e:
        return False, "Erreur: {}".format(e)


@bot.message_handler(commands=["start", "aide", "help"])
def cmd_aide(message):
    if not _autorise(message):
        return
    texte = (
        "🎼 *Orchestre d'Agents IA*\n\n"
        "Envoie-moi une tâche, je m'occupe du reste :\n\n"
        "🔍 *Recherche* : « Analyse l'impact de l'IA sur l'éducation »\n"
        "💻 *Code* : « Écris un script Python pour trier une liste »\n"
        "📊 *Data* : « Analyse ces données : 12, 45, 78, 23, 56 »\n"
        "✍️ *Contenu* : « Rédige un article sur le climat »\n\n"
        "🔬 Chaque rapport est relu par un *agent Critique*.\n"
        "_L'orchestre tourne directement sur ce serveur cloud._"
    )
    bot.reply_to(message, texte, parse_mode="Markdown")


@bot.message_handler(commands=["status"])
def cmd_status(message):
    if not _autorise(message):
        return
    nb_fournisseurs = 0
    if os.getenv("GROQ_API_KEY"): nb_fournisseurs += 1
    if os.getenv("GEMINI_API_KEY"): nb_fournisseurs += 1
    if os.getenv("OPENROUTER_API_KEY"): nb_fournisseurs += 1
    bot.reply_to(message, "🎼 Bot en ligne.\nCerveaux disponibles : {}".format(nb_fournisseurs))


@bot.message_handler(func=lambda m: True)
def traiter_tache(message):
    """Traite n'importe quel message comme une tâche."""
    if not _autorise(message):
        bot.reply_to(message, "Tu n'es pas autorise a utiliser ce bot.")
        return

    sujet = (message.text or "").strip()
    if not sujet:
        return

    info("Tache recue de {} : {}...".format(message.chat.id, sujet[:60]))
    bot.reply_to(message, "🔄 Je traite : « {}... »\nLes agents travaillent...".format(sujet[:60]))

    succes, reponse = _executer_orchestre(sujet)
    _envoyer(message.chat.id, reponse)
    if succes:
        ok("Tache traitee avec succes.")


# ════════════════════════════════════════════════════════
#  DÉMARRAGE
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    info("🚀 Démarrage du bot cloud + keep-alive")
    info("En attente de messages Telegram...")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        info("Arrêt du bot.")
