#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  AGENT RÉDACTEUR  ✍️
# ════════════════════════════════════════════════════════
#  Rôle : transformer l'analyse en un rapport final clair,
#  engageant et bien structuré. C'est lui qui produit le
#  livrable que l'utilisateur va lire.
#
#  C'est le violoncelle de l'orchestre.
# ════════════════════════════════════════════════════════

source "$ORCHESTRE_ROOT/lib/utils.sh"
source "$ORCHESTRE_ROOT/lib/llm.sh"

REDACTEUR_SYSTEME="Tu es un rédacteur professionnel chevronné.
Tu transformes des analyses brutes en rapports magnifiquement
rédigés : clairs, engageants, bien structurés et accessibles.

Ton style :
- Professionnel mais jamais ennuyeux.
- Phrases fluides et rythmées.
- Format Markdown impeccable.
- Tu réponds toujours en français."

# ─────────────────────────────────────────────────────────
#  agent_redacteur : rédige le rapport final
# ─────────────────────────────────────────────────────────
#  Arguments : $1 = l'analyse, $2 = le sujet original
#  Résultat   : le rapport final en Markdown (sur STDOUT)
# ─────────────────────────────────────────────────────────
agent_redacteur() {
    local analyse="$1"
    local sujet="$2"

    log_agent "Rédacteur" "Composer le rapport final"

    local prompt="Sujet de recherche original : $sujet

Voici l'analyse préparée par l'agent analyste :

$analyse

Rédige maintenant un RAPPORT DE RECHERCHE professionnel
au format Markdown. Ce rapport doit inclure :

- Un titre principal percutant (niveau #)
- Une introduction qui pose le contexte et l'enjeu
- 3 à 5 sections avec sous-titres (niveau ##) couvrant
  les points clés de l'analyse
- Des listes à puces quand c'est pertinent pour la lisibilité
- Une conclusion avec synthèse et perspectives d'avenir

Le rapport doit faire entre 500 et 1000 mots.
Il doit être fluide, bien organisé et agréable à lire.
N'utilise PAS de délimiteur de code au début ou à la fin."

    local resultat
    resultat=$(appeler_llm "$REDACTEUR_SYSTEME" "$prompt" 0.7)

    if [ $? -ne 0 ]; then
        log_erreur "Le rédacteur n'a pas pu compléter sa mission."
        return 1
    fi

    local nb_mots=$(echo "$resultat" | wc -w | tr -d ' ')
    log_ok "Rapport rédigé — $nb_mots mots."
    echo "$resultat"
}
