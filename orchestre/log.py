"""
🎨 Utilitaires d'affichage
===========================
Tous les messages vont sur STDERR (erreur standard) afin de
ne pas polluer STDOUT, qui sert uniquement aux vraies données
(le rapport final). Même principe qu'en bash V1.
"""

import sys

# --- Codes couleur ANSI (jolis sur terminal) ---
_ROUGE = "\033[0;31m"
_VERT = "\033[0;32m"
_JAUNE = "\033[1;33m"
_BLEU = "\033[0;34m"
_VIOLET = "\033[0;35m"
_CYAN = "\033[0;36m"
_GRIS = "\033[0;90m"
_NC = "\033[0m"  # remet la couleur normale

# Détecte si on écrit dans un vrai terminal (sinon, pas de couleur)
_COULEUR = sys.stderr.isatty()


def _peindre(couleur, texte):
    """Applique une couleur si on est sur un vrai terminal."""
    if _COULEUR:
        return f"{couleur}{texte}{_NC}"
    return texte


def info(msg):
    """Message d'information (bleu)."""
    print(_peindre(_BLEU, f"[ℹ] {msg}"), file=sys.stderr)


def ok(msg):
    """Message de succès (vert)."""
    print(_peindre(_VERT, f"[✓] {msg}"), file=sys.stderr)


def erreur(msg):
    """Message d'erreur (rouge)."""
    print(_peindre(_ROUGE, f"[✗] {msg}"), file=sys.stderr)


def attention(msg):
    """Message d'avertissement (jaune)."""
    print(_peindre(_JAUNE, f"[⚠] {msg}"), file=sys.stderr)


def titre(msg):
    """Grand titre de section (violet)."""
    barre = "═" * 42
    print("", file=sys.stderr)
    print(_peindre(_VIOLET, barre), file=sys.stderr)
    print(_peindre(_VIOLET, f"  {msg}"), file=sys.stderr)
    print(_peindre(_VIOLET, barre), file=sys.stderr)


def agent(nom, mission):
    """Présente un agent qui commence à travailler."""
    print("", file=sys.stderr)
    print(_peindre(_CYAN, f"🤖 Agent : {nom}"), file=sys.stderr)
    print(_peindre(_CYAN, f"   Mission : {mission}"), file=sys.stderr)
    print(_peindre(_GRIS, "   " + "─" * 36), file=sys.stderr)


def separateur():
    """Ligne séparatrice grise."""
    print(_peindre(_GRIS, "─" * 42), file=sys.stderr)
