# Social Wellness Digest

## Vision
Combattre le burnout numérique via un écosystème d'utilité radicale.
Ce projet implémente "Application 1" : Le Digest de Bien-être Social.

## Architecture
- **Inestion**: Python (`DataIngestionService.py`)
- **Imtelligence**: TypeScript + LLM (`SemanticFilter.ts`)
- **Présentation**: Go (`DigestArchitect.go`)

## Setup GitHub (Comment pousser ce repo)

1.  **Sur GitHub** :
    - Connectez-vous à votre compte GitHub.
    - Cliquez sur le bouton "+" en haut à droite -> "New repository".
    - Nommez-le (ex: `social-wellness-digest`).
    - Ne cochez PAS "Initialize with README", "Add .gitignore", etc. (on a déjà le code localement).
    - Cliquez sur "Create repository".

2.  **Sur votre machine (ici)** :
    - Copiez l'URL du repo (ex: `https://github.com/VOTRE_USER/social-wellness-digest.git`).
    - Exécutez les commandes suivantes dans le terminal de ce dossier :

```bash
# Ajouter l'origine distante
git remote add origin https://github.com/VOTRE_USER/social-wellness-digest.git

# Renommer la branche principale en 'main' (standard actuel)
git branch -M main

# Ajouter tous les fichiers
git add .

# Faire le premier commit
git commit -m "Initial commit: Architecture setup based on Strategic Report"

# Pousser vers GitHub
git push -u origin main
```

### Option 2 : Via GitHub Desktop

1.  Ouvrez **GitHub Desktop**.
2.  Allez dans `File` -> `Add Local Repository`.
3.  Sélectionnez le dossier `i:\Sites\social_wellness_digest`.
4.  GitHub Desktop vous proposera de "Publish repository". Cliquez sur ce bouton.
5.  Assurez-vous que le nom est correct, choisissez si vous voulez que le code soit privé ou public.
6.  Cliquez sur "Publish Repository".

