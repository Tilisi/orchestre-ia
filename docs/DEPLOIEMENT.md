# 🚀 Mise en production — GitHub + Telegram

> Guide complet, pas à pas, pour déployer ton orchestre dans le cloud gratuit et le piloter depuis ton téléphone.
> **Niveau : débutant → intermédiaire. Tout est expliqué.**

---

## 🗺️ Le plan en 6 étapes

```
ÉTAPE 1 : Créer un compte GitHub (si pas déjà)        ⏱️ 3 min
ÉTAPE 2 : Créer un dépôt PUBLIC                        ⏱️ 2 min
ÉTAPE 3 : Créer un Personal Access Token               ⏱️ 3 min
ÉTAPE 4 : Pousser le code depuis Termux                ⏱️ 5 min
ÉTAPE 5 : Configurer les Secrets (clés API)            ⏱️ 3 min
ÉTAPE 6 : Lancer + (option) brancher Telegram          ⏱️ 5 min
```

---

## ÉTAPE 1 — Compte GitHub

Si tu en as déjà un, passe à l'étape 2.

1. Va sur **https://github.com/signup**
2. Crée ton compte (email + mot de passe)
3. Valide ton email

---

## ÉTAPE 2 — Créer un dépôt PUBLIC ⚠️

> ⚠️ **PUBLIC est OBLIGATOIRE** pour avoir les GitHub Actions **gratuits et illimités**.
> En privé, tu n'as que 2000 min/mois.

1. Va sur **https://github.com/new**
2. **Repository name** : `orchestre-ia`
3. **Description** (option) : `🎼 Orchestre d'agents IA multi-usages`
4. Visibilité : sélectionne **Public** ⚠️
5. Ne coche RIEN d'autre (pas de README, pas de .gitignore — on a déjà les nôtres)
6. Clique **Create repository**

GitHub t'affiche une page avec des commandes. Garde-la ouverte.

---

## ÉTAPE 3 — Personal Access Token ⚠️ (PIÈGE FRÉQUENT)

> 💡 Depuis 2021, GitHub **n'accepte plus les mots de passe** pour pousser du code.
> Il te faut un **token** (une sorte de mot de passe temporaire).

1. Va sur **https://github.com/settings/tokens**
2. Clique **Generate new token** → **Generate new token (classic)**
3. **Note** : `orchestre-push` (pour t'en souvenir)
4. **Expiration** : `90 days` (ou `No expiration` si tu préfères)
5. ⚠️ **Scopes** : coche ces cases :
   - ✅ `repo` (TOUT le bloc — permet de pousser le code)
   - ✅ `workflow` (permet de mettre à jour les GitHub Actions)
6. Clique tout en bas **Generate token**
7. ⚠️ **COPIE LE TOKEN TOUT DE SUITE** (`ghp_xxxxxxxxxxxx`)
   > Il ne sera plus jamais affiché ! Si tu le perds, tu devras en recréer un.

---

## ÉTAPE 4 — Pousser le code depuis Termux

Sur ton **Redmi 14**, ouvre **Termux**.

### 4.1 Installer git et cloner le dépôt vide

```bash
pkg install -y git python

# Va dans ton dossier maison
cd ~

# Clone ton dépôt vide (remplace TON-NOM par ton pseudo GitHub)
git clone https://github.com/TON-NOM/orchestre-ia.git
cd orchestre-ia
```

> Quand git te demande ton identifiant : tape ton pseudo GitHub.
> Pour le mot de passe : **colle ton TOKEN** (pas ton mot de passe !)

### 4.2 Récupérer les fichiers du projet

Tu as deux options :

**Option A — Recréer les fichiers** (si tu as le code sous le coude)
Place chaque fichier du projet dans ce dossier `orchestre-ia/`.

**Option B — Télécharger le ZIP** (le plus simple)
1. Si tu as le projet en ZIP sur ton téléphone, place-le dans le dossier cloné
2. Active l'accès stockage : `termux-setup-storage`
3. Copie : `cp ~/storage/downloads/orchestre-ia-main.zip . && unzip orchestre-ia-main.zip`

### 4.3 Configurer git (une seule fois)

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton@email.com"
```

### 4.4 Pousser le code

```bash
# Vérifier ce qui va partir (VÉRIFIE QUE .env N'EST PAS DANS LA LISTE !)
git add -A
git status

# Créer le premier commit
git commit -m "🎼 Orchestre d'agents IA V2"

# Pousser sur GitHub
git branch -M main
git push -u origin main
```

> ⚠️ **VÉRIFICATION CRITIQUE** : dans `git status`, le fichier `.env`
> ne doit **PAS** apparaître. Si tu le vois, ARRÊTE et vérifie ton `.gitignore`.

> Si on te redemande un mot de passe : colle ton **TOKEN**, pas ton mdp GitHub.

✅ Va sur ton dépôt GitHub : tu dois voir tes fichiers !

---

## ÉTAPE 5 — Configurer les Secrets (clés API)

Les secrets stockent tes clés de façon chiffrée et invisible publiquement.

1. Sur ton dépôt GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Clique **New repository secret** pour chaque clé :

| Name (exact) | Secret (ta valeur) |
|--------------|--------------------|
| `GROQ_API_KEY` | `gsk_tanouvelleclé` (⬅️ la NOUVELLE, pas l'ancienne révoquée !) |
| `GEMINI_API_KEY` | *(optionnel)* ta clé Gemini |
| `OPENROUTER_API_KEY` | *(optionnel)* ta clé OpenRouter |

> 💡 Une seule clé (Groq) suffit pour démarrer.

---

## ÉTAPE 6 — Lancer ta première tâche cloud ! 🎉

### 6.1 Via le bouton GitHub

1. Onglet **Actions** de ton dépôt
2. Clique **🎼 Orchestre IA** (à gauche)
3. Clique **Run workflow** (à droite, bouton vert)
4. **sujet** : `Les énergies renouvelables en Afrique`
5. **type** : `auto`
6. Clique **Run workflow**

Attends 1-2 min, clique sur la run en cours → regarde les agents travailler dans les logs. Le rapport est aussi dans **Artifacts** (téléchargeable).

**Tu as un orchestre IA gratuit dans le cloud !** 🚀

---

## ÉTAPE 7 (option) — Bot Telegram 📱

Pilote l'orchestre en envoyant un message depuis ton téléphone.

### 7.1 Créer le bot

1. Sur Telegram, cherche **@BotFather**
2. Envoie `/newbot`
3. Nom : `Mon Orchestre IA`
4. Username : `mon_orchestre_ia_bot` (doit finir par `_bot`)
5. **Copie le token** : `1234567890:AaBbCcDdEeFf...`

### 7.2 Ton Chat ID

1. Cherche **@userinfobot** sur Telegram → `/start`
2. **Copie ton Id** : `123456789`

### 7.3 Ajouter les secrets Telegram sur GitHub

Dans **Settings → Secrets → Actions**, ajoute :
- `TELEGRAM_BOT_TOKEN` → le token du bot
- `TELEGRAM_CHAT_ID` → ton Id

> ✨ Maintenant chaque rapport généré sur GitHub t'est **envoyé sur Telegram** !

### 7.4 Lancer le bot sur Termux (pour déclencher depuis Telegram)

```bash
cd ~/orchestre-ia
cp .env.example .env
nano .env
```

Dans `.env`, remplis :
```
TELEGRAM_BOT_TOKEN=1234567890:AaBbCcDd...
TELEGRAM_CHAT_ID=123456789
GITHUB_TOKEN=ghp_tontokenétape3
GITHUB_REPO=TON-NOM/orchestre-ia
BOT_MODE=cloud
```

Puis :
```bash
pip install -r requirements.txt
python3 bot/telegram_bot.py
```

Laisse Termux ouvert. Envoie un message à ton bot → il déclenche GitHub Actions → le rapport arrive sur Telegram ! 📱

---

## ✅ Checklist finale

- [ ] Dépôt GitHub **public** créé
- [ ] Personal Access Token créé (droits `repo` + `workflow`)
- [ ] Code poussé (`.env` VÉRIFIÉ absent)
- [ ] Secret `GROQ_API_KEY` ajouté
- [ ] Première tâche lancée via **Run workflow**
- [ ] (option) Bot Telegram créé + secrets ajoutés
- [ ] (option) Bot lancé sur Termux → message envoyé → rapport reçu 🎉

---

## ❓ Dépannage

**`git push` demande un mot de passe et ça échoue**
→ Utilise ton **TOKEN** (pas ton mdp GitHub). Format : `ghp_...`

**`fatal: Authentication failed`**
→ Le token est expiré ou mauvais. Régénère-le (étape 3).

**Le workflow échoue : "Aucun fournisseur d'API"**
→ Vérifie les secrets (étape 5) : noms EXACTS `GROQ_API_KEY` etc.

**`.env` apparaît dans git status**
→ Vérifie que `.gitignore` contient bien une ligne `.env`. Si tu as déjà pushé `.env` par erreur, fais :
```bash
git rm --cached .env
git commit -m "Retire .env"
git push
```
Et **RÉVOQUE** immédiatement ta clé sur console.groq.com.

**Le bot Telegram ne répond pas**
→ Le bot doit tourner en continu (laisse Termux ouvert).
  Pour du 24/7 sans téléphone : héberge-le (Koyeb, Render — gratuits).
