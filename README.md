# 🎼 Orchestre d'Agents IA — V1 + V2

> Un orchestre d'**agents IA multi-usages** qui collaborent pour faire de la recherche, générer du code, analyser des données et créer du contenu. En **bash pur** (V1) ou **bash + Python** (V2), exécutable sur **Termux**, dans le **cloud gratuit** (GitHub Actions), et pilotable depuis ton téléphone via **Telegram**.

---

## 🆚 Deux versions disponibles

| | **V1 — Bash pur** | **V2 — Multi-usages + Cloud** |
|---|---|---|
| **Langage** | Bash uniquement | Bash + Python |
| **Cerveau** | Groq seul | Multi-API avec **fallback** (Groq→Gemini→OpenRouter) |
| **Usages** | Recherche uniquement | Recherche + Code + Data + Contenu |
| **Web** | Scraping basique | Scraping web réel (BeautifulSoup) |
| **Exécution** | Termux (téléphone) | Termux **+ GitHub Actions** (gratuit illimité) |
| **Pilotage** | Terminal | Terminal + **Bot Telegram** |
| **Niveau** | Débutant | Intermédiaire |

> 👉 **Débutant ?** Commence par la [V1](#v1--bash-pur-termux). Tu comprends les bases.
> 👉 **Tu veux le système complet ?** Va direct à la [V2](#v2--multi-usages--cloud).

---

## 🏗️ Architecture V2

```
┌──────────────────────────────────────────────────────────┐
│            📱 TON REDMI 14 (ou n'importe quel appareil)    │
│         Tu écris une tâche à ton Bot Telegram              │
└────────────────────────┬─────────────────────────────────┘
                         │ message Telegram
                         ▼
┌──────────────────────────────────────────────────────────┐
│              🔵 GITHUB (dépôt public — gratuit illimité)   │
│   • Code versionné     • Secrets sécurisés (clés API)     │
│   • GitHub Actions = moteur de calcul sur serveur Ubuntu  │
│                                                            │
│     🔀 Routeur → 🤖 Agents → 🧠 Cerveau multi-API          │
└──────────────────────────────────────────────────────────┘
```

### Le cerveau multi-API (fallback)
Si un fournisseur tombe, le suivant prend le relais. **L'orchestre ne s'arrête jamais.**
```
Groq (rapide) ──échec──▶ Gemini ──échec──▶ OpenRouter
```

### Les 5 agents multi-usages
| Agent | Rôle | Exemple |
|-------|------|---------|
| 🔀 **Routeur** | Détecte le type de tâche | *automatique* |
| 🔍 **Chercheur** | Explore + scraping web réel | "L'impact de l'IA sur la santé" |
| 🧠 **Analyste** | Extrait les insights | *enchaîne après le chercheur* |
| ✍️ **Rédacteur** | Compose rapports/articles | "Rédige un article sur le climat" |
| 💻 **Codeur** | Génère/explique/corrige du code | "Script Python pour trier une liste" |
| 📊 **Data** | Vraies stats Python + interprétation | "Analyse ce CSV de ventes" |

---

## 🚀 V2 — Démarrage rapide

> 📖 **Guide complet pas à pas : [`docs/V2_INSTALL.md`](docs/V2_INSTALL.md)**

### Option A — GitHub Actions (le plus puissant, recommandé)

```bash
# 1. Crée un dépôt PUBLIC sur GitHub (gratuit, exécution illimitée)
# 2. Pousse le code :
git init && git add . && git commit -m "Orchestre IA V2"
git remote add origin https://github.com/TON-NOM/orchestre-ia.git
git push -u origin main

# 3. Ajoute tes clés API dans :
#    Settings → Secrets and variables → Actions
#    (GROQ_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY)

# 4. Va dans l'onglet "Actions" → "🎼 Orchestre IA" → "Run workflow"
#    Entre ton sujet... et c'est tout ! Le serveur gratuit fait le reste.
```

### Option B — Local sur Termux

```bash
pkg install python          # installer Python
pip install -r requirements.txt   # dépendances
cp .env.example .env        # puis édite .env avec tes clés
./chef.sh "Analyse l'impact de l'IA sur la santé"
```

### Option C — Bot Telegram (pilote depuis ton téléphone)

```bash
# Configure TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID dans .env
BOT_MODE=local python3 bot/telegram_bot.py
# Puis écris à ton bot depuis Telegram !
```

---

## 📁 Structure du projet

```
orchestre-ia/
├── # ═══ V2 : Multi-usages + Cloud (bash + Python) ═══
├── orchestre/                 ← 🧠 package Python (le cœur)
│   ├── cerveau.py             ← multi-API avec fallback
│   ├── routeur.py             ← détection du type de tâche
│   ├── chercheur.py           ← 🔍 + scraping web réel
│   ├── analyseur.py           ← 🧠
│   ├── redacteur.py           ← ✍️
│   ├── codeur.py              ← 💻
│   ├── data_agent.py          ← 📊 (vraies statistiques Python)
│   ├── chef.py                ← 🎼 orchestration
│   └── __main__.py            ← CLI (python -m orchestre)
├── chef.sh                    ← wrapper bash → appelle Python
├── bot/telegram_bot.py        ← 📱 pilotage depuis Telegram
├── .github/workflows/
│   └── orchestre.yml          ← ⚙️ workflow GitHub Actions
├── requirements.txt           ← dépendances Python
│
├── # ═══ V1 : Bash pur (Termux) ═══
├── v1_legacy/
│   ├── orchestrateur.sh      ← chef d'orchestre V1
│   ├── config.sh / install.sh
│   ├── lib/{utils.sh, llm.sh}
│   ├── agents/{chercheur.sh, analyseur.sh, redacteur.sh}
│   └── skills/recherche_web.sh
│
├── docs/
│   ├── INSTALL.md             ← guide V1 (Termux)
│   ├── V2_INSTALL.md          ← guide V2 (GitHub + Telegram)
│   └── V2_ARCHITECTURE.md     ← analyse & comparatif des infras
├── .env.example               ← modèle de config (toutes les clés)
└── output/                    ← rapports générés
```

---

## 🔑 Obtenir les clés API (toutes gratuites)

| Fournisseur | URL | À quoi ça sert |
|-------------|-----|----------------|
| **Groq** ⭐ | https://console.groq.com | Cerveau principal (ultra-rapide) |
| **Google Gemini** | https://aistudio.google.com/apikey | Fallback (multimodal) |
| **OpenRouter** | https://openrouter.ai/keys | Dernier recours (plein de modèles) |
| **Telegram** | @BotFather sur Telegram | Créer le bot |
| **GitHub Token** | github.com/settings/tokens | Déclencher les workflows |

---

## 💡 Exemples d'utilisation (V2)

```bash
# 🔍 Recherche approfondie (avec vrai scraping web)
./chef.sh "Les énergies renouvelables en Afrique en 2026"

# 💻 Génération de code
./chef.sh "Écris un script Python pour surveiller un site web"

# 📊 Analyse de données (CSV)
./chef.sh --fichier ventes.csv --type data

# ✍️ Création de contenu
./chef.sh "Rédige un article de blog sur l'apprentissage automatique"

# Forcer un type précis
./chef.sh --type code "Explique-moi les décorateurs Python"
```

---

## ⚠️ Limites honnêtes

- **Arena.ai** ne propose pas d'API publique de type "prompt → réponse" utilisable comme cerveau (voir [`docs/V2_ARCHITECTURE.md`](docs/V2_ARCHITECTURE.md)). On utilise donc Groq/Gemini/OpenRouter à la place.
- **GitHub Actions** : pas de réponses instantanées 24/7 (délais possibles). Pour du temps réel, il faudrait un VPS (Oracle Cloud free tier : 2 CPU / 12 Go).
- **Pas de GPU gratuit** pour faire tourner des modèles géants en local.

---

## V1 — Bash pur (Termux)

La V1 reste disponible et fonctionnelle dans le dossier `v1_legacy/`. Idéale pour apprendre les bases du multi-agent en bash.

```bash
cd v1_legacy
bash install.sh              # installation
nano ../.env                 # ajouter GROQ_API_KEY
./orchestrateur.sh "ton sujet"
```

Documentation V1 : [`docs/INSTALL.md`](docs/INSTALL.md)

---

## 📜 Licence

Projet libre — utilise-le, modifie-le, partage-le ! 🎵

*Construit avec ❤️ — Termux + GitHub + Telegram, 100% gratuit.*
