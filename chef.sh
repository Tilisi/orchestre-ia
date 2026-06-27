#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  🎼 CHEF D'ORCHESTRE — Wrapper bash pour la V2 Python
# ════════════════════════════════════════════════════════
#  Ce script est un pont entre le bash (que tu connais) et
#  le moteur Python de la V2. Il charge le .env puis lance
#  l'orchestre.
#
#  Usage :
#     ./chef.sh "votre tâche"
#     ./chef.sh --fichier donnees.csv --type data
#
#  C'est l'équivalent de :  python3 -m orchestre "$@"
# ════════════════════════════════════════════════════════

export ORCHESTRE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Charger la configuration .env (clés API, etc.) ---
if [ -f "$ORCHESTRE_ROOT/.env" ]; then
    set -a
    source "$ORCHESTRE_ROOT/.env"
    set +a
fi

# --- Exporter le chemin de sortie ---
export ORCHESTRE_OUTPUT="${ORCHESTRE_OUTPUT:-$ORCHESTRE_ROOT/output}"
mkdir -p "$ORCHESTRE_OUTPUT"

# --- Se placer à la racine du projet (pour les imports Python) ---
cd "$ORCHESTRE_ROOT"

# --- Vérifier que Python 3 est disponible ---
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 est introuvable !"
    echo "   Installe-le :  pkg install python"
    exit 1
fi

# --- Vérifier les dépendances nécessaires au CLI local ---
# requests + bs4 : recherche web ; dotenv : chargement .env si disponible.
if ! python3 -c "import requests, bs4, dotenv" 2>/dev/null; then
    echo "⚠️  Dépendances Python manquantes. Installation..."
    pip install -r "$ORCHESTRE_ROOT/requirements.txt" || {
        echo "❌ Échec de l'installation. Lance :  pip install -r requirements.txt"
        exit 1
    }
fi

# --- Lancer l'orchestre ---
python3 -m orchestre "$@"
