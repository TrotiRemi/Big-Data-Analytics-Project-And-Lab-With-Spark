---
title: Home
publish: true
---
# Big Data Analytics - ESIEE 2025-2026

Bienvenue sur le site du cours **Big Data Analytics** de l'école **ESIEE**.

## 📚 Organisation du cours

Ce dépôt contient tous les **laboratoires**, **assignments** et le **projet final** du cours.

### 🔬 Laboratoires (Laboratory_BDA)

- **Lab 0** : Introduction à Spark et RDD
- **Lab 1** : Transformation RDD et Pair RDD
- **Lab 2** : DataFrames et SQL
- **Lab 3** : Streaming et MLlib
- **Lab 4** : Checkpoint et optimisation

### 🎯 Projet Final (Projet_BDA)

Analyse blockchain et prédiction de prix Bitcoin avec Spark.

- **Consignes** : [01_BDA_Final_Project_Brief.md](Projet_BDA/consignes/01_BDA_Final_Project_Brief.md)
- **Reproducibility** : [02_Reproducibility_Checklist.md](Projet_BDA/consignes/02_Reproducibility_Checklist.md)
- **Template Report** : [03_BDA_Project_Report_Template.md](Projet_BDA/consignes/03_BDA_Project_Report_Template.md)
- **Dataset Guide** : [04_Dataset_Acquisition_Guide.md](Projet_BDA/consignes/04_Dataset_Acquisition_Guide.md)

---

## 🌐 Accès au site

Ce dépôt est déployé sur **Cloudflare Pages** avec l'outil **Quartz**.

- **URL** : https://bda-website.pages.dev (ou votre domaine personnalisé)
- **Accès** : Restreint aux emails ESIEE (`esiee.fr`, `edu.esiee.fr`)
- **Contenu** : Tous les notebooks, assignments et docs

---

## 🚀 Setup et déploiement

### Première fois

```bash
# Configurez vos credentials Cloudflare
export CLOUDFLARE_ACCOUNT_ID="..."
export CLOUDFLARE_API_TOKEN="..."

# Bootstrap le site (sur WSL ou Git Bash)
make site/setup
```

### Après édition

```bash
make site/update
```

### Vérifier avant de commit

```bash
make site/check
```

Pour plus de détails, voir [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) ou [QUARTZ_SETUP.md](QUARTZ_SETUP.md).

---

## 📋 Deadline

**07/12/2025 23:59 Paris time**

Soumission via le site du cours.

---

## ⚠️ Notes importantes

- Ne commitez **jamais** les credentials Cloudflare en clair
- Les dossiers `/data` ne sont **pas** déployés sur le site (trop volumineux)
- Utilisez `make site/check` avant de pousser sur GitHub
- En cas d'erreur 404, vérifiez votre Account ID et Access est activé

---

## 👨‍🏫 Instructeur

**Badr TAJINI** - Big Data Analytics - ESIEE 2025-2026

