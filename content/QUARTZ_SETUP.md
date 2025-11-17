# Quartz + Cloudflare Setup Guide

## ✅ Configuration actuellement complétée

- ✅ GitHub user: `TrotiRemi`
- ✅ Repo: `Big-Data-Analytics-Project-And-Lab-With-Spark`
- ✅ Email domain: `esiee.fr,edu.esiee.fr`
- ✅ Cloudflare project (placeholder): `bda-website`
- ✅ `.gitignore` créé pour exclure les données volumineux
- ✅ Git repo initialisé

## ⚠️ À faire avant `make site/setup`

### 1. Créer un compte Cloudflare Pages (si pas déjà fait)

1. Allez sur https://dash.cloudflare.com/
2. Créez un compte ou connectez-vous
3. Allez à **Pages** → Créez un nouveau projet
4. Connectez votre repo GitHub `Big-Data-Analytics-Project-And-Lab-With-Spark`
5. Attendez que le projet soit créé (ça crée une URL du type `bda-website.pages.dev`)

### 2. Obtenir votre Cloudflare Account ID

1. Allez à https://dash.cloudflare.com/
2. En bas à droite, vous verrez **Account ID** (c'est un UUID comme `a1b2c3d4...`)
3. Copiez-le

### 3. Créer un API Token Cloudflare

1. Allez à https://dash.cloudflare.com/profile/api-tokens
2. Cliquez **Create Token**
3. Utilisez le template **Edit Cloudflare Workers** ou créez un custom token avec ces permissions:
   - **Pages**: Edit
   - **DNS**: Edit
   - **Zero Trust Access**: Edit
4. **Scope**: Sélectionnez votre account
5. Copiez le token généré

### 4. Configurer le token

Avant de lancer `make site/setup`, exécutez:

```bash
export CLOUDFLARE_ACCOUNT_ID="votre_account_id_ici"
export CLOUDFLARE_API_TOKEN="votre_token_api_ici"
```

Ou modifiez directement le fichier `setup_quartz_cloudflare.sh`:
- Remplacez `CHANGE_ME_CF_ACCOUNT_ID` par votre Account ID
- Remplacez `REPLACE_WITH_API_TOKEN` par votre API Token

## 🚀 Lancer le setup

Une fois que vous avez vos credentials Cloudflare:

```bash
make site/setup
```

Cela va:
1. Télécharger Quartz
2. Convertir vos notebooks `.ipynb` en HTML
3. Créer des wrappers Markdown
4. Copier les fichiers de documentation
5. Builder le site statique
6. Pousser sur GitHub (branche `main`)
7. Déployer sur Cloudflare Pages
8. Configurer l'Access pour restreindre aux emails `esiee.fr` et `edu.esiee.fr`

## 📝 Pour mettre à jour après

Après avoir édité vos notebooks ou docs:

```bash
make site/update
```

## 🔍 Pour vérifier avant de commit

```bash
make site/check
```

## ✨ Résultat

Votre site sera accessible à:
- `https://bda-website.pages.dev` (ou votre domaine personnalisé)
- Restreint aux emails ESIEE via Cloudflare Access
- Avec tous vos notebooks et labs comme ressources interactives

---

**Questions?** Les logs de chaque étape s'affichent avec timestamps `[HH:MM:SS]`
