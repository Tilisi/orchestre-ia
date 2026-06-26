#!/data/data/com.termux/files/usr/bin/bash
# ════════════════════════════════════════════════════════
#  SCRIPT D'INSTALLATION — TERMUX
# ════════════════════════════════════════════════════════
#  À lancer UNE SEULE FOIS après avoir cloné le dépôt.
#
#     bash install.sh
#
#  Il installe les dépendances et prépare l'environnement.
# ════════════════════════════════════════════════════════

set -e  # Arrêter dès qu'une commande échoue

echo ""
echo "📦  Installation de l'Orchestre IA pour Termux"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- 1. Mettre à jour Termux ---
echo "▶ Étape 1/4 : Mise à jour des paquets..."
pkg update -y && pkg upgrade -y
echo ""

# --- 2. Installer les dépendances ---
echo "▶ Étape 2/4 : Installation de curl, jq, git..."
pkg install -y curl jq git
echo ""

# --- 3. Rendre les scripts exécutables ---
echo "▶ Étape 3/4 : Activation des scripts..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$SCRIPT_DIR"/orchestrateur.sh
chmod +x "$SCRIPT_DIR"/install.sh
chmod +x "$SCRIPT_DIR"/config.sh
chmod +x "$SCRIPT_DIR"/agents/*.sh
chmod +x "$SCRIPT_DIR"/skills/*.sh
chmod +x "$SCRIPT_DIR"/lib/*.sh
echo "   ✓ Scripts activés"
echo ""

# --- 4. Préparer le fichier .env ---
echo "▶ Étape 4/4 : Configuration..."
mkdir -p "$SCRIPT_DIR/output"

if [ ! -f "$SCRIPT_DIR/.env" ]; then
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo "   ✓ Fichier .env créé (à partir du modèle)"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  ACTION REQUISE !"
    echo ""
    echo "   Tu dois ajouter ta clé API Groq :"
    echo ""
    echo "   nano $SCRIPT_DIR/.env"
    echo ""
    echo "   Remplace la ligne :"
    echo "     GROQ_API_KEY=gsk_colle_ta_cle_ici"
    echo "   par ta vraie clé (gratuite sur https://console.groq.com)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "   ✓ .env déjà présent — configuration conservée"
fi

echo ""
echo "✅  Installation terminée !"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PROCHAINES ÉTAPES :"
echo ""
echo "  1. Ajoute ta clé API :   nano .env"
echo "  2. Lance une recherche : ./orchestrateur.sh \"ton sujet\""
echo ""
echo "  Exemple :"
echo "     ./orchestrateur.sh \"L'avenir de l'intelligence artificielle\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
