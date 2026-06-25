#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  SKILL : RECHERCHE WEB  🔎
# ════════════════════════════════════════════════════════
#  Une "compétence" (skill) réutilisable : effectue une
#  recherche sur le web via DuckDuckGo et renvoie du texte.
#
#  Les skills sont des briques que n'importe quel agent peut
#  utiliser. C'est l'extensibilité de l'orchestre !
#
#  Usage direct :
#     ./skills/recherche_web.sh "intelligence artificielle"
# ════════════════════════════════════════════════════════

# --- Déterminer la racine du projet ---
if [ -z "$ORCHESTRE_ROOT" ]; then
    export ORCHESTRE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
source "$ORCHESTRE_ROOT/config.sh"
source "$ORCHESTRE_ROOT/lib/utils.sh"

# ─────────────────────────────────────────────────────────
#  skill_recherche_web : cherche sur DuckDuckGo
# ─────────────────────────────────────────────────────────
#  Argument : $1 = la requête de recherche
#  Résultat  : texte brut des résultats (sur STDOUT)
# ─────────────────────────────────────────────────────────
skill_recherche_web() {
    local requete="$1"

    # Encoder la requête pour l'URL (les espaces → +)
    local encodee
    encodee=$(echo "$requete" | tr ' ' '+')

    log_info "Recherche web : « $requete »"

    # --- Récupérer la page de résultats (DuckDuckGo Lite) ---
    local page
    page=$(curl -s --max-time 15 \
        -A "Mozilla/5.0 (Linux; Android 14)" \
        "https://lite.duckduckgo.com/lite/?q=$encodee&kl=fr-fr")

    # --- Extraire le texte utile ---
    # 1. Supprimer les balises HTML
    # 2. Convertir les entités HTML courantes
    # 3. Supprimer les lignes vides et le bruit
    # 4. Garder les 30 premières lignes (titres + extraits)
    local texte
    texte=$(echo "$page" | \
        sed 's/<[^>]*>//g' | \
        sed 's/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&nbsp;/ /g; s/&#39;/'\''/g; s/&quot;/"/g' | \
        grep -v '^[[:space:]]*$' | \
        grep -viE 'duckduckgo|privacy|newsletter|about|javascript|cookie' | \
        head -30)

    if [ -z "$texte" ]; then
        log_erreur "Aucun résultat web trouvé pour : $requete"
        return 1
    fi

    local nb_lignes=$(echo "$texte" | wc -l | tr -d ' ')
    log_ok "$nb_lignes lignes de résultats récupérées."
    echo "$texte"
}

# --- Si on lance ce script directement, on exécute la recherche ---
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    if [ -z "$1" ]; then
        echo "Usage : ./skills/recherche_web.sh \"votre recherche\""
        exit 1
    fi
    skill_recherche_web "$1"
fi
