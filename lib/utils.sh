#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  FONCTIONS UTILITAIRES
# ════════════════════════════════════════════════════════
#  Couleurs, messages, séparateurs.
#  IMPORTANT : toutes les fonctions d'affichage écrivent
#  sur STDERR (>&2), pour ne pas polluer les données
#  renvoyées par les agents via STDOUT.
# ════════════════════════════════════════════════════════

# Codes de couleur ANSI
export ROUGE='\033[0;31m'
export VERT='\033[0;32m'
export JAUNE='\033[1;33m'
export BLEU='\033[0;34m'
export VIOLET='\033[0;35m'
export CYAN='\033[0;36m'
export GRIS='\033[0;90m'
export NC='\033[0m'  # Remettre la couleur normale

# --- Message d'information ---
log_info() {
    echo -e "${BLEU}[ℹ]${NC} $1" >&2
}

# --- Message de succès ---
log_ok() {
    echo -e "${VERT}[✓]${NC} $1" >&2
}

# --- Message d'erreur ---
log_erreur() {
    echo -e "${ROUGE}[✗]${NC} $1" >&2
}

# --- Grand titre de section ---
log_titre() {
    echo "" >&2
    echo -e "${VIOLET}══════════════════════════════════════════${NC}" >&2
    echo -e "${VIOLET}  $1${NC}" >&2
    echo -e "${VIOLET}══════════════════════════════════════════${NC}" >&2
}

# --- Présentation d'un agent qui commence à travailler ---
log_agent() {
    local nom="$1"
    local mission="$2"
    echo "" >&2
    echo -e "${CYAN}🤖 Agent : $nom${NC}" >&2
    echo -e "${CYAN}   Mission : $mission${NC}" >&2
    echo -e "${GRIS}   ────────────────────────────────────${NC}" >&2
}

# --- Ligne séparatrice ---
separateur() {
    echo -e "${GRIS}──────────────────────────────────────────${NC}" >&2
}
