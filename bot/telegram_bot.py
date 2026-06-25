#!/usr/bin/env python3
"""
📱 BOT TELEGRAM — Pilote ton orchestre depuis ton téléphone
============================================================
Tu écris une tâche à ton bot Telegram, et l'orchestre la traite.

DEUX MODES (variable d'environnement BOT_MODE) :

  MODE = "cloud"  (recommandé, par défaut)
      Le bot déclenche un workflow GitHub Actions. Le calcul
      lourd se fait sur un serveur gratuit d'Ubuntu (GitHub).
      Le résultat t'est renvoyé automatiquement sur Telegram
      par le workflow. Idéal : le téléphone ne fait rien.

  MODE = "local"
      Le bot exécute l'orchestre directement en Python là où
      il tourne (Termux ou un serveur). Utile pour tester.

-----------------------------------------------------------------
COMMENT LANCER LE BOT :
-----------------------------------------------------------------
  1. En local sur Termux :   BOT_MODE=local  python3 bot/telegram_bot.py
  2. Mode cloud (GitHub) :   BOT_MODE=cloud  python3 bot/telegram_bot.py
  3. Hébergé 24/7 gratuit :  Voir docs/V2_INSTALL.md (Koyeb / Render)
-----------------------------------------------------------------

Variables d'environnement (.env) :
  - TELEGRAM_BOT_TOKEN   (obtenu via @BotFather)
  - TELEGRAM_CHAT_ID     (ton ID, via @userinfobot)
  Mode cloud, en plus :
  - GITHUB_TOKEN         (Personal Access Token, droits repo+workflow)
  - GITHUB_REPO          (ex: ton-nom/orchestre-ia)
"""

import os
import sys
import time
import requests

# S'assurer qu'on peut importer le package orchestre/
_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJET not in sys.path:
    sys.path.insert(0, _PROJET)

# --- Charger le .env manuellement (sans dépendance python-dotenv) ---
_GUILLEMETS = ('"', "'")  # tuple de caractères guillemets


def _charger_env(chemin):
    if not os.path.exists(chemin):
        return
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#") or "=" not in ligne:
                continue
            cle, _, val = ligne.partition("=")
            cle = cle.strip()
            val = val.strip()
            # Retirer les guillemets entourant la valeur
            if len(val) >= 2 and val[0] == val[-1] and val[0] in _GUILLEMETS:
                val = val[1:-1]
            if cle and cle not in os.environ:
                os.environ[cle] = val


_charger_env(os.path.join(_PROJET, ".env"))

# --- Importer telebot ---
try:
    import telebot
except ImportError:
    print("pyTelegramBotAPI manquant. Lance :  pip install -r requirements.txt")
    sys.exit(1)

from orchestre.log import info, ok, erreur

# --- Configuration ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID_AUTORISE = os.getenv("TELEGRAM_CHAT_ID", "")
MODE = os.getenv("BOT_MODE", "cloud").lower()

if not TOKEN:
    print("TELEGRAM_BOT_TOKEN manquant dans .env")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)


# ════════════════════════════════════════════════════════
#  UTILITAIRES
# ════════════════════════════════════════════════════════

def _autorise(message):
    """Vérifie que l'utilisateur est autorisé (sécurité)."""
    if not CHAT_ID_AUTORISE:
        return True  # pas de restriction configurée
    return str(message.chat.id) == str(CHAT_ID_AUTORISE)


def _envoyer(chat_id, texte):
    """Envoie un texte, en le découpant s'il dépasse la limite Telegram (4096)."""
    texte = texte or "(vide)"
    limite = 4000
    if len(texte) <= limite:
        bot.send_message(chat_id, texte)
        return
    morceaux = [texte[i:i + limite] for i in range(0, len(texte), limite)]
    total = len(morceaux)
    for i, morceau in enumerate(morceaux, start=1):
        bot.send_message(chat_id, "(part {}/{})\n\n{}".format(i, total, morceau))
        time.sleep(0.3)


def _declencher_github(sujet):
    """
    Déclenche le workflow GitHub Actions avec le sujet en entrée.
    Renvoie (succes: bool, message: str).
    """
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    if not token or not repo:
        return False, ("Mode cloud : GITHUB_TOKEN et GITHUB_REPO requis dans .env. "
                       "Sinon, passe en mode local (BOT_MODE=local).")

    url = "https://api.github.com/repos/{}/actions/workflows/orchestre.yml/dispatches".format(repo)
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {
        "ref": "main",
        "inputs": {"sujet": sujet[:500], "type": "auto"},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 204:
            return True, ("🚀 Tâche lancée sur GitHub Actions !\n\n"
                          "Le serveur gratuit traite ta demande.\n"
                          "Le rapport arrive ici dans ~1-2 min. ⏳")
        return False, "❌ GitHub a renvoyé {} : {}".format(resp.status_code, resp.text[:200])
    except Exception as e:
        return False, "❌ Impossible de déclencher GitHub : {}".format(e)


def _executer_local(sujet):
    """Exécute l'orchestre localement et renvoie le résultat."""
    try:
        from orchestre import chef
        resultat = chef.executer(sujet)
        chef.sauvegarder(resultat, sujet)
        return True, resultat
    except Exception as e:
        return False, "❌ Erreur lors de l'exécution : {}".format(e)


# ════════════════════════════════════════════════════════
#  COMMANDES DU BOT
# ════════════════════════════════════════════════════════

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
        "⚙️ Mode actuel : *{}*\n".format(MODE)
    )
    if MODE == "cloud":
        texte += "\n_Le calcul se fait sur GitHub Actions (gratuit)._"
    else:
        texte += "\n_Le calcul se fait localement._"
    bot.reply_to(message, texte, parse_mode="Markdown")


@bot.message_handler(commands=["mode"])
def cmd_mode(message):
    if not _autorise(message):
        return
    bot.reply_to(message, "⚙️ Mode actuel : {}\n"
                          "Change-le via BOT_MODE dans .env (cloud ou local)".format(MODE))


@bot.message_handler(func=lambda m: True)
def traiter_tache(message):
    """Traite n'importe quel message comme une tâche."""
    if not _autorise(message):
        bot.reply_to(message, "🚫 Tu n'es pas autorisé à utiliser ce bot.")
        return

    sujet = (message.text or "").strip()
    if not sujet:
        return

    info("Tâche reçue de {} : {}...".format(message.chat.id, sujet[:60]))
    bot.reply_to(message, "🔄 Je traite : « {}... »\nMode : {}".format(sujet[:60], MODE))

    if MODE == "cloud":
        succes, reponse = _declencher_github(sujet)
    else:
        succes, reponse = _executer_local(sujet)

    _envoyer(message.chat.id, reponse)
    if succes:
        ok("Tâche traitée avec succès.")


# ════════════════════════════════════════════════════════
#  DÉMARRAGE
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    info("📱 Démarrage du bot Telegram (mode : {})".format(MODE))
    info("En attente de messages... (Ctrl+C pour arrêter)")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        info("Arrêt du bot.")
