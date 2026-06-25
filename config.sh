#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  CONFIGURATION CENTRALE DE L'ORCHESTRE IA
# ════════════════════════════════════════════════════════
#  Ce fichier est "sourcé" (chargé) par tous les autres
#  scripts. Il contient les paramètres partagés :
#  - le chemin du projet
#  - la clé API Groq
#  - le modèle à utiliser
# ════════════════════════════════════════════════════════

# --- 1. Dossier racine du projet ---
# On déduit automatiquement le dossier où se trouve ce fichier.
if [ -z "$ORCHESTRE_ROOT" ]; then
    export ORCHESTRE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# --- 2. Dossier de sortie (où les rapports sont sauvegardés) ---
export OUTPUT_DIR="$ORCHESTRE_ROOT/output"
mkdir -p "$OUTPUT_DIR"

# --- 3. Chargement de la clé API ---
# On lit le fichier .env s'il existe (il contient la clé Groq).
if [ -f "$ORCHESTRE_ROOT/.env" ]; then
    set -a
    source "$ORCHESTRE_ROOT/.env"
    set +a
fi

# --- 4. Vérification de la clé ---
if [ -z "$GROQ_API_KEY" ]; then
    echo ""
    echo "❌ ERREUR : La variable GROQ_API_KEY n'est pas définie !"
    echo ""
    echo "   Pour corriger :"
    echo "   1. Crée un fichier .env à la racine du projet"
    echo "   2. Ajoute-y la ligne :  GROQ_API_KEY=gsk_xxxxxxxxxxxx"
    echo "   3. Obtiens ta clé gratuite sur : https://console.groq.com"
    echo ""
    echo "   Ou copie le modèle :  cp .env.example .env"
    echo ""
    exit 1
fi

# --- 5. Modèle Groq à utiliser ---
# llama-3.3-70b-versatile = le plus intelligent (recommandé)
export GROQ_MODEL="${GROQ_MODEL:-llama-3.3-70b-versatile}"

# --- 6. URL de l'API Groq ---
export GROQ_URL="https://api.groq.com/openai/v1/chat/completions"

# --- 7. Dossier temporaire (fichiers intermédiaires) ---
export TMP_DIR="${TMPDIR:-/tmp}/orchestre_${USER}"
mkdir -p "$TMP_DIR"
