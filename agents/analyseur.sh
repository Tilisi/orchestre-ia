#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  AGENT ANALYSTE  🧠
# ════════════════════════════════════════════════════════
#  Rôle : prendre les données brutes du chercheur et en
#  extraire les insights, les tendances et les points clés.
#  Il ajoute de la valeur analytique (le "pourquoi").
#
#  C'est l'alto de l'orchestre.
# ════════════════════════════════════════════════════════

source "$ORCHESTRE_ROOT/lib/utils.sh"
source "$ORCHESTRE_ROOT/lib/llm.sh"

ANALYSTE_SYSTEME="Tu es un analyste stratégique expert.
Tu prends des informations brutes et tu en extraits l'essentiel :
tendances, patterns, insights profonds, implications.

Tu ne te contentes jamais de répéter : tu ajoutes toujours
une couche d'analyse et de réflexion critique.

Réponds toujours en français."

# ─────────────────────────────────────────────────────────
#  agent_analyste : analyse les données du chercheur
# ─────────────────────────────────────────────────────────
#  Argument : $1 = les données brutes collectées
#  Résultat  : l'analyse structurée (sur STDOUT)
# ─────────────────────────────────────────────────────────
agent_analyste() {
    local donnees="$1"

    log_agent "Analyste" "Extraire les insights des données collectées"

    local prompt="Voici les informations collectées par l'agent chercheur :

$donnees

Ta mission d'analyse :
1. Identifie les 5 à 8 insights les plus importants.
2. Pour chacun, explique POURQUOI c'est important et quelles
   en sont les implications.
3. Mets en évidence les tendances et patterns qui se dégagent.
4. Signale les points faibles, contradictions ou incertitudes.
5. Termine par une synthèse en 3 phrases maximum.

Sois critique, perspicace et ajoute de la valeur au-delà
des faits bruts. Utilise le format Markdown avec des titres ##."

    local resultat
    resultat=$(appeler_llm "$ANALYSTE_SYSTEME" "$prompt" 0.5)

    if [ $? -ne 0 ]; then
        log_erreur "L'analyste n'a pas pu compléter sa mission."
        return 1
    fi

    log_ok "Analyse terminée — insights extraits."
    echo "$resultat"
}
