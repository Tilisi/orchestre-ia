# 📖 Guide d'installation V2 — GitHub Actions + Telegram

> Mise en place complète de l'orchestre multi-usages dans le cloud gratuit, pilotable depuis ton téléphone.

---

## 🗺️ Vue d'ensemble des 4 étapes

```
1. Préparer les clés API (Gratuit)        🔑
2. Pousser le projet sur GitHub (Public)  📦  → exécution illimitée gratuite
3. Configurer les GitHub Secrets          🔐
4. (Option) Brancher le bot Telegram      📱
```

Tu peux t'arrêter à l'étape 3 : tu auras déjà un orchestre qui tourne gratuitement dans le cloud. L'étape 4 (Telegram) ajoute le confort de piloter depuis ton téléphone.

---

## ÉTAPE 1 — Obtenir les clés API (10 min)

Il te faut **au moins une** clé. Plus tu en mets, plus l'orchestre est résilient (fallback).

### 🔑 Groq (recommandé, priorité haute)
1. Va sur **https://console.groq.com**
2. Crée un compte gratuit (pas de carte bancaire)
3. Menu **API Keys** → **Create API Key**
4. Copie la clé (commence par `gsk_`)

### 🔑 Google Gemini (fallback)
1. Va sur **https://aistudio.google.com/apikey**
2. **Create API key** → copie-la (commence par `AIza`)

### 🔑 OpenRouter (dernier recours)
1. Va sur **https://openrouter.ai/keys**
2. Crée une clé (commence par `sk-or-`)
3. Des modèles gratuits sont disponibles

> 💡 Note tes clés quelque part, on va les utiliser à l'étape 3.

---

## ÉTAPE 2 — Pousser le projet sur GitHub (5 min)

### 2.1 Créer un dépôt PUBLIC

⚠️ **PUBLIC est important** : les dépôts publics ont des **minutes GitHub Actions illimitées et gratuites**.

1. Va sur **https://github.com/new**
2. Nom du dépôt : `orchestre-ia`
3. Visibilité : **Public** ⚠️
4. Ne coche PAS "Add a README" (on a déjà le nôtre)
5. **Create repository**

### 2.2 Pousser le code depuis Termux (ou ton PC)

```bash
# Dans le dossier du projet
git init
git add .
git commit -m "🎼 Orchestre IA V2"

# Vérifie que .env n'est PAS inclus (sécurité !)
git status          # .env ne doit PAS apparaître

git branch -M main
git remote add origin https://github.com/TON-NOM/orchestre-ia.git
git push -u origin main
```

> ⚠️ Si `.env` apparaît dans `git status`, NE PUSSE PAS. Le fichier `.gitignore` doit l'exclure. Vérifie-le.

---

## ÉTAPE 3 — Configurer les GitHub Secrets (5 min)

Les **secrets** stockent tes clés API de façon chiffrée. Elles sont invisibles publiquement.

1. Sur GitHub, va dans ton dépôt → **Settings** → **Secrets and variables** → **Actions**
2. Clique **New repository secret** pour chaque clé :

| Nom du secret | Valeur |
|---------------|--------|
| `GROQ_API_KEY` | ta clé Groq (`gsk_...`) |
| `GEMINI_API_KEY` | ta clé Gemini (`AIza...`) |
| `OPENROUTER_API_KEY` | ta clé OpenRouter (`sk-or-...`) |

> Tu peux n'en mettre qu'une seule (Groq suffit pour commencer).

---

## ÉTAPE 4 — Lancer ta première tâche ! 🎉

### 4.1 Via le bouton GitHub (le plus simple)

1. Va dans l'onglet **Actions** de ton dépôt
2. Clique sur **🎼 Orchestre IA** (à gauche)
3. Clique **Run workflow** (à droite)
4. Remplis :
   - **sujet** : `L'impact de l'IA sur la santé en 2026`
   - **type** : `auto` (détection intelligente)
5. Clique **Run workflow** (vert)

### 4.2 Voir le résultat

- Clique sur la run qui vient de se lancer (point jaune)
- Attends ~1-2 minutes que les agents travaillent
- Le résultat est dans les **logs** de l'étape "Exécuter l'orchestre"
- Un fichier téléchargeable `resultat.md` est dans les **Artifacts** en bas

**Tu as un orchestre IA qui tourne sur un serveur gratuit !** 🚀

---

## ÉTAPE 5 (option) — Brancher le bot Telegram

Pour piloter l'orchestre en message depuis ton téléphone.

### 5.1 Créer le bot Telegram

1. Ouvre Telegram, cherche **@BotFather**
2. Envoie `/newbot`
3. Donne un nom (ex: `Mon Orchestre IA`)
4. Donne un identifiant (ex: `mon_orchestre_ia_bot`)
5. **Copie le token** reçu (`1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`)

### 5.2 Obtenir ton Chat ID

1. Cherche **@userinfobot** sur Telegram
2. Envoie `/start`
3. **Copie ton Id** (un nombre comme `123456789`)

### 5.3 Ajouter les secrets Telegram sur GitHub

Dans **Settings → Secrets → Actions**, ajoute :
- `TELEGRAM_BOT_TOKEN` → ton token
- `TELEGRAM_CHAT_ID` → ton Id

> Maintenant, à chaque fois qu'une tâche tourne sur GitHub, le **rapport t'est envoyé directement sur Telegram** ! 📱

### 5.4 Déclencher les tâches depuis Telegram

Pour lancer une tâche en envoyant un message (sans ouvrir GitHub), tu peux :

**Option simple — en local sur Termux :**
```bash
cp .env.example .env
# Édite .env : TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
#              GITHUB_TOKEN, GITHUB_REPO, BOT_MODE=cloud
pip install -r requirements.txt
python3 bot/telegram_bot.py
```
Ton téléphone reste allumé, le bot écoute, et à chaque message il déclenche GitHub Actions. Le rapport revient sur Telegram.

**Le token GitHub** : crée-le sur github.com/settings/tokens (droits `repo` + `workflow`).

---

## ✅ Checklist finale V2

- [ ] Au moins une clé API obtenue (Groq recommandé)
- [ ] Dépôt GitHub **public** créé
- [ ] Code poussé (sans le `.env` !)
- [ ] Secrets GitHub configurés
- [ ] Première tâche lancée via **Run workflow**
- [ ] (option) Bot Telegram créé
- [ ] (option) Secrets Telegram ajoutés → rapports reçus sur le téléphone

---

## 🧪 Tester en local (sans GitHub)

Si tu veux tester vite fait sur Termux avant le cloud :

```bash
pkg install python git
git clone https://github.com/TON-NOM/orchestre-ia.git
cd orchestre-ia
pip install -r requirements.txt
cp .env.example .env
nano .env          # ajoute GROQ_API_KEY au minimum

# Test direct :
./chef.sh "Analyse l'impact de l'IA sur l'éducation"

# Test avec un type forcé :
./chef.sh --type code "Écris une fonction Python de tri rapide"
```

---

## ❓ Dépannage V2

**Le workflow GitHub échoue avec "Aucun fournisseur d'API disponible"**
→ Vérifie que tu as bien ajouté les secrets (étape 3) avec les BONS noms (`GROQ_API_KEY`, etc.)

**"dépendances manquantes" en local**
→ `pip install -r requirements.txt`

**Le bot Telegram ne répond pas**
→ Vérifie le token et le chat_id dans `.env`. Le bot doit tourner en continu ( laisse la fenêtre Termux ouverte, ou héberge-le).

**L'API renvoie une erreur 429 (rate limit)**
→ Trop de requêtes. Attends 1 min. Le fallback multi-API aide beaucoup ici.

**Erreur d'import Python (`ModuleNotFoundError: orchestre`)**
→ Lance toujours les commandes depuis la racine du projet, ou utilise `./chef.sh`.
