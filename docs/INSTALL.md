# 📖 Guide d'installation détaillé — Termux + GitHub

> Installation pas à pas de l'Orchestre d'Agents IA sur un téléphone Android (ex: Redmi 14) via Termux.

---

## Étape 0 — Installer Termux

⚠️ **Important :** N'installe PAS Termux depuis le Play Store (version obsolète et buguée).

1. Ouvre ton navigateur sur le téléphone
2. Va sur **https://f-droid.org/packages/com.termux/**
3. Télécharge et installe l'APK
4. Ouvre **Termux**

Tu as maintenant un vrai terminal Linux sur ton téléphone ! 🎉

---

## Étape 1 — Mettre à jour Termux

Dans Termux, tape ces commandes (une par une, appuie sur Entrée à chaque fois) :

```bash
pkg update -y
pkg upgrade -y
```

> Si on te demande `[Y/n]`, répond `y` puis Entrée.

---

## Étape 2 — Installer les outils de base

```bash
pkg install -y git curl jq
```

| Outil | À quoi ça sert |
|-------|----------------|
| `git` | Cloner le projet depuis GitHub |
| `curl` | Appeler l'API Groq (envoyer/recevoir des données) |
| `jq` | Lire et créer du JSON (le format de l'API) |

Vérifie que tout est bien installé :

```bash
git --version    # doit afficher git version X.XX
curl --version   # doit afficher curl X.XX
jq --version     # doit afficher jq-X.X
```

---

## Étape 3 — Configurer Git (pour GitHub)

Si tu n'as jamais utilisé git sur ce téléphone :

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton.email@example.com"
```

---

## Étape 4 — Cloner le projet

### Option A : Cloner ton propre dépôt GitHub

Si tu as déjà créé un dépôt sur GitHub et y as poussé le projet :

```bash
git clone https://github.com/TON-NOM-D-UTILISATEUR/orchestre-ia.git
cd orchestre-ia
```

### Option B : Télécharger depuis GitHub en ZIP

Si quelqu'un d'autre a partagé le projet :

1. Sur GitHub, clique le bouton vert **Code** → **Download ZIP**
2. Dans Termux :
```bash
# Le fichier est sûrement dans ~/storage/downloads/
# (voir l'étape sur l'accès au stockage ci-dessous)
unzip orchestre-ia-main.zip
cd orchestre-ia-main
```

### Option C : Créer le projet à la main

Tu peux aussi recréer tous les fichiers un par un avec `nano nom_du_fichier.sh`.

---

## Étape 5 — Accès au stockage (optionnel)

Si tu veux accéder aux fichiers depuis d'autres applis (partager le rapport) :

```bash
termux-setup-storage
```

Une popup te demandera l'autorisation → **Autoriser**.

Tu pourras alors copier tes rapports vers le dossier Downloads :
```bash
cp output/rapport_*.md ~/storage/downloads/
```

---

## Étape 6 — Lancer l'installation

Dans le dossier du projet :

```bash
bash install.sh
```

Ce script va :
- ✅ Mettre à jour Termux
- ✅ Installer curl, jq, git
- ✅ Rendre les scripts exécutables
- ✅ Créer le fichier `.env` (à partir du modèle)

---

## Étape 7 — Ajouter ta clé API Groq

### Obtenir la clé (gratuite)

1. Va sur **https://console.groq.com** (depuis le navigateur du téléphone)
2. Crée un compte / connecte-toi
3. Menu de gauche → **API Keys**
4. Clique **Create API Key**
5. Donne-lui un nom (ex: `orchestre-ia`)
6. **Copie la clé** (elle commence par `gsk_`)
   > ⚠️ Tu ne pourras plus la voir après ! Copie-la bien.

### La mettre dans le projet

Dans Termux :

```bash
nano .env
```

L'éditeur `nano` s'ouvre. Remplace la ligne :

```
GROQ_API_KEY=gsk_colle_ta_cle_ici
```

par ta vraie clé :

```
GROQ_API_KEY=gsk_1234567890abcdefghijklmnopqrstuvwxyz
```

**Pour sauvegarder dans nano :**
- Appuie sur `Ctrl + O` (la lettre O) puis `Entrée` → sauvegarde
- Appuie sur `Ctrl + X` → quitte nano

> 💡 Sur clavier téléphone : `Ctrl` = maintenir la touche volume ou utiliser Hacker Keyboard.

---

## Étape 8 — Lancer ta première recherche ! 🎉

```bash
./orchestrateur.sh "L'impact de l'intelligence artificielle sur la santé"
```

Tu vas voir les 3 agents travailler l'un après l'autre, puis le rapport final s'afficher.

Le rapport est aussi sauvegardé dans `output/`.

---

## 🔄 Mettre à jour le projet depuis GitHub

Si tu as cloné depuis GitHub et que le dépôt a été mis à jour :

```bash
git pull
```

---

## ☁️ Pousser ton projet sur GitHub (depuis Termux)

Si tu veux héberger ton propre projet sur GitHub :

```bash
# 1. Initialiser git (si pas déjà fait)
git init

# 2. Ajouter tous les fichiers
git add .

# 3. Vérifier que .env n'est PAS dans la liste (sécurité !)
git status

# 4. Créer un commit
git commit -m "Mon orchestre d'agents IA"

# 5. Ajouter ton dépôt distant
git remote add origin https://github.com/TON-NOM/orchestre-ia.git

# 6. Envoyer sur GitHub
git branch -M main
git push -u origin main
```

> ⚠️ **Vérifie bien** que `.env` n'apparaît pas dans `git status` !
> Le fichier `.gitignore` est censé l'exclure automatiquement.

---

## ✅ Checklist finale

- [ ] Termux installé (depuis F-Droid)
- [ ] `pkg update && pkg upgrade` fait
- [ ] `curl`, `jq`, `git` installés
- [ ] Projet cloné ou créé
- [ ] `bash install.sh` lancé
- [ ] Clé API Groq dans `.env`
- [ ] `./orchestrateur.sh "test"` fonctionne

**Tout est coché ? Bravo, tu as ton orchestre IA sur ton téléphone !** 🎼🤖
