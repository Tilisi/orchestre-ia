#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  AGENT CHERCHEUR  🔍
# ════════════════════════════════════════════════════════
#  Rôle : explorer le sujet, le découper en sous-questions
#  et rassembler un maximum d'informations pertinentes.
#
#  C'est le 1er violon de l'orchestre.
# ════════════════════════════════════════════════════════

source "$ORCHESTRE_ROOT/lib/utils.sh"
source "$ORCHESTRE_ROOT/lib/llm.sh"

# La personnalité / les instructions du chercheur
CHERCHEUR_SYSTEME="Tu es un agent de recherche expert et méthodique.
Ta mission est d'explorer un sujet en profondeur, de le découper
en sous-questions clés, puis de rassembler des informations
détaillées et factuelles pour chacune.

Règles :
- Réponds toujours en français.
- Sois factuel, précis et complet.
- Donne des chiffres, des dates, des exemples concrets.
- Structure ta réponse avec des titres (##)."

# ─────────────────────────────────────────────────────────
#  agent_chercheur : lance la recherche
# ─────────────────────────────────────────────────────────
#  Argument : $1 = le sujet de recherche
#  Résultat  : les données collectées (sur STDOUT)
# ─────────────────────────────────────────────────────────
agent_chercheur() {
    local sujet="$1"

    log_agent "Chercheur" "Explorer en profondeur le sujet"

    local prompt="Voici le sujet de recherche à explorer :

━━━ $sujet ━━━

Ta mission, étape par étape :
1. Décompose ce sujet en 4 à 6 sous-questions essentielles.
2. Pour chaque sous-question, rédige une réponse détaillée
   en t'appuyant sur tes connaissances (faits, chiffres, exemples).
3. Si le sujet implique des évolutions récentes, donne les
   tendances actuelles.
4. Termine par une section « Points clés » listant les 5
   découvertes les plus importantes.

Utilise le format Markdown avec un titre ## pour chaque sous-question."

    local resultat
    resultat=$(appeler_llm "$CHERCHEUR_SYSTEME" "$prompt" 0.4)

    if [ $? -ne 0 ]; then
        log_erreur "Le chercheur n'a pas pu compléter sa mission."
        return 1
    fi

    local nb_mots=$(echo "$resultat" | wc -w | tr -d ' ')
    log_ok "Recherche terminée — $nb_mots mots collectés."
    echo "$resultat"
}
