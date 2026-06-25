#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  LE CERVEAU DE L'ORCHESTRE : appel à l'API Groq
# ════════════════════════════════════════════════════════
#  Tous les agents utilisent cette fonction pour "penser".
#  Elle envoie un prompt à Groq et renvoie le texte reçu.
#
#  C'est le seul endroit du projet qui parle à internet.
# ════════════════════════════════════════════════════════

# Charger la configuration (clé API, modèle, URL)
if [ -z "$ORCHESTRE_ROOT" ]; then
    export ORCHESTRE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
source "$ORCHESTRE_ROOT/config.sh"
source "$ORCHESTRE_ROOT/lib/utils.sh"

# ─────────────────────────────────────────────────────────
#  appeler_llm : la fonction principale
# ─────────────────────────────────────────────────────────
#  Arguments :
#    $1 = prompt système   (le rôle / la personnalité de l'agent)
#    $2 = prompt utilisateur (la question ou la tâche)
#    $3 = température       (optionnel, 0 = précis, 1 = créatif)
#
#  Résultat : le texte de la réponse est écrit sur STDOUT
#             (les messages de log vont sur STDERR)
# ─────────────────────────────────────────────────────────
appeler_llm() {
    local system_prompt="$1"
    local user_prompt="$2"
    local temperature="${3:-0.7}"

    # --- Construire la requête JSON avec jq ---
    # jq gère automatiquement les guillemets et caractères spéciaux,
    # ce qui évite les bugs d'échappement. Très important !
    local payload
    payload=$(jq -n \
        --arg model "$GROQ_MODEL" \
        --arg sys "$system_prompt" \
        --arg usr "$user_prompt" \
        --argjson temp "$temperature" \
        '{
            "model": $model,
            "messages": [
                {"role": "system", "content": $sys},
                {"role": "user",   "content": $usr}
            ],
            "temperature": $temp
        }')

    # --- Message pendant que l'agent réfléchit ---
    echo -ne "${JAUNE}   ⏳ Réflexion en cours...${NC}" >&2

    # --- Envoyer la requête à l'API Groq ---
    local reponse
    reponse=$(curl -s --max-time 120 \
        "$GROQ_URL" \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload")

    echo -e " ${VERT}✓${NC}" >&2

    # --- Vérifier s'il y a une erreur renvoyée par l'API ---
    local erreur
    erreur=$(echo "$reponse" | jq -r '.error.message // empty' 2>/dev/null)
    if [ -n "$erreur" ]; then
        log_erreur "L'API Groq a renvoyé une erreur :"
        log_erreur "   $erreur"
        return 1
    fi

    # --- Extraire le texte de la réponse ---
    local contenu
    contenu=$(echo "$reponse" | jq -r '.choices[0].message.content' 2>/dev/null)

    # --- Vérifier qu'on a bien reçu quelque chose ---
    if [ -z "$contenu" ] || [ "$contenu" = "null" ]; then
        log_erreur "Réponse vide ou invalide de l'API."
        log_erreur "Réponse brute : $reponse"
        return 1
    fi

    # --- Renvoyer le contenu (sur STDOUT, donc capturable) ---
    echo "$contenu"
}

# ─────────────────────────────────────────────────────────
#  poser_question : raccourci pour une question simple
# ─────────────────────────────────────────────────────────
poser_question() {
    local question="$1"
    local role="${2:-Tu es un assistant utile qui répond en français.}"
    appeler_llm "$role" "$question" 0.7
}
