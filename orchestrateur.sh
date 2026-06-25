#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#   🎼  LE CHEF D'ORCHESTRE  🎼
# ════════════════════════════════════════════════════════
#  C'est le script PRINCIPAL. Il coordonne les 3 agents :
#
#     Chercheur  →  Analyste  →  Rédacteur
#
#  Usage :
#     ./orchestrateur.sh "votre sujet de recherche"
#
#  Exemple :
#     ./orchestrateur.sh "L'impact de l'IA sur l'éducation"
# ════════════════════════════════════════════════════════

# --- Déterminer le dossier racine du projet ---
export ORCHESTRE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Charger la configuration et les utilitaires ---
source "$ORCHESTRE_ROOT/config.sh"
source "$ORCHESTRE_ROOT/lib/utils.sh"

# --- Charger les 3 agents ---
source "$ORCHESTRE_ROOT/agents/chercheur.sh"
source "$ORCHESTRE_ROOT/agents/analyseur.sh"
source "$ORCHESTRE_ROOT/agents/redacteur.sh"

# ─────────────────────────────────────────────────────────
#  Vérifier que les outils nécessaires sont installés
# ─────────────────────────────────────────────────────────
verifier_environnement() {
    log_titre "Contrôle de l'environnement"

    if ! command -v curl &>/dev/null; then
        log_erreur "curl est introuvable ! Installe-le :  pkg install curl"
        exit 1
    fi
    log_ok "curl détecté"

    if ! command -v jq &>/dev/null; then
        log_erreur "jq est introuvable ! Installe-le :  pkg install jq"
        exit 1
    fi
    log_ok "jq détecté"

    log_ok "Clé API Groq configurée"
    log_ok "Modèle : $GROQ_MODEL"
}

# ─────────────────────────────────────────────────────────
#  PROGRAMME PRINCIPAL
# ─────────────────────────────────────────────────────────
main() {
    # --- Vérifier qu'un sujet a été fourni ---
    if [ -z "$1" ]; then
        echo ""
        echo -e "${VIOLET}🎼  ORCHESTRE D'AGENTS IA${NC}"
        echo ""
        echo "Usage :"
        echo "  ./orchestrateur.sh \"votre sujet de recherche\""
        echo ""
        echo "Exemples :"
        echo "  ./orchestrateur.sh \"L'impact de l'IA sur l'éducation\""
        echo "  ./orchestrateur.sh \"Les énergies renouvelables en 2026\""
        echo "  ./orchestrateur.sh \"Comment apprendre le bash efficacement\""
        echo ""
        exit 1
    fi

    local sujet="$*"
    local horodatage=$(date +"%Y-%m-%d_%H-%M-%S")

    # --- Bannière d'accueil ---
    clear 2>/dev/null || true
    echo "" >&2
    echo -e "${VIOLET}╔══════════════════════════════════════════════╗${NC}" >&2
    echo -e "${VIOLET}║        🎼  ORCHESTRE D'AGENTS IA  🎼          ║${NC}" >&2
    echo -e "${VIOLET}║     Recherche multi-agents · Termux           ║${NC}" >&2
    echo -e "${VIOLET}╚══════════════════════════════════════════════╝${NC}" >&2
    echo "" >&2
    echo -e "${CYAN}  Sujet :${NC} $sujet" >&2
    echo -e "${CYAN}  Date  :${NC} $(date '+%d/%m/%Y à %H:%M')" >&2
    echo "" >&2

    verifier_environnement

    # ═══════════════════════════════════════════════════
    #   ÉTAPE 1/3 — LE CHERCHEUR
    # ═══════════════════════════════════════════════════
    log_titre "ÉTAPE 1/3 — Le Chercheur explore le sujet"
    local donnees_brutes
    donnees_brutes=$(agent_chercheur "$sujet")
    if [ $? -ne 0 ]; then
        log_erreur "Échec à l'étape 1. Abandon de l'orchestre."
        exit 1
    fi
    echo "$donnees_brutes" > "$TMP_DIR/01_chercheur.md"
    separateur

    # ═══════════════════════════════════════════════════
    #   ÉTAPE 2/3 — L'ANALYSTE
    # ═══════════════════════════════════════════════════
    log_titre "ÉTAPE 2/3 — L'Analyste extrait les insights"
    local analyse
    analyse=$(agent_analyste "$donnees_brutes")
    if [ $? -ne 0 ]; then
        log_erreur "Échec à l'étape 2. Abandon de l'orchestre."
        exit 1
    fi
    echo "$analyse" > "$TMP_DIR/02_analyse.md"
    separateur

    # ═══════════════════════════════════════════════════
    #   ÉTAPE 3/3 — LE RÉDACTEUR
    # ═══════════════════════════════════════════════════
    log_titre "ÉTAPE 3/3 — Le Rédacteur compose le rapport"
    local rapport
    rapport=$(agent_redacteur "$analyse" "$sujet")
    if [ $? -ne 0 ]; then
        log_erreur "Échec à l'étape 3. Abandon de l'orchestre."
        exit 1
    fi
    separateur

    # ═══════════════════════════════════════════════════
    #   SAUVEGARDE DU RAPPORT FINAL
    # ═══════════════════════════════════════════════════
    # Nettoyer le sujet pour en faire un nom de fichier valide
    local nom_fichier
    nom_fichier=$(echo "$sujet" | tr ' ' '_' | tr -cd '[:alnum:]_' | cut -c1-40)
    local fichier_final="$OUTPUT_DIR/rapport_${nom_fichier}_${horodatage}.md"
    echo "$rapport" > "$fichier_final"

    # ═══════════════════════════════════════════════════
    #   AFFICHAGE DU RÉSULTAT
    # ═══════════════════════════════════════════════════
    log_titre "📄 RAPPORT FINAL"
    echo ""
    cat "$fichier_final"    # Affiché sur STDOUT (le vrai livrable)
    echo ""
    separateur

    log_ok "Rapport sauvegardé : $fichier_final"
    echo "" >&2
    echo -e "${GRIS}  Fichiers intermédiaires :${NC}" >&2
    echo -e "${GRIS}    Recherche brute : $TMP_DIR/01_chercheur.md${NC}" >&2
    echo -e "${GRIS}    Analyse         : $TMP_DIR/02_analyse.md${NC}" >&2
    echo "" >&2
    echo -e "${VERT}  🎼 Concerto terminé avec succès !${NC}" >&2
    echo "" >&2
}

# --- C'est parti ! ---
main "$@"
