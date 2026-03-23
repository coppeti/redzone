# RedZone — CLAUDE.md

## Présentation du projet

Site communautaire pour un club de motards (RedZone). L'interface principale est un carousel de cartes membres avec animation 3D flip. Le projet est en Django 5.2 avec Alpine.js côté frontend.

## Stack technique

- **Backend** : Django 5.2.5, Python 3.12, SQLite (dev) / PostgreSQL (prod via psycopg2)
- **Frontend** : Alpine.js v3, CSS3 custom (pas de framework CSS)
- **Typos** : Nosifer (titres), Poppins ExtraLight/Light/Medium (body)
- **Env vars** : python-decouple (.env)
- **Serveur prod** : Gunicorn

## Structure des apps

```
config/     → settings, urls racine
accounts/   → CustomUser, auth email, espace membres
main/       → home (carousel), gallery
```

## Modèle principal : CustomUser

Authentification par **email** (pas username). Champs spécifiques au club :

| Champ | Type | Notes |
|-------|------|-------|
| email | EmailField unique | identifiant de connexion |
| rank | IntegerField default=99 | ordre d'affichage dans le carousel |
| firstname | CharField(30) | |
| nickname | CharField(100) | affiché sur la carte (police Nosifer) |
| aka1–aka4 | CharField(100) | alias, affichés au dos de la carte |
| description | TextField | bio courte |
| picture | ImageField | uploadé dans `media/members/` |

> `MemberCard` dans `main/models.py` est un modèle legacy inutilisé.

## URLs

| URL | Vue | Accès |
|-----|-----|-------|
| `/` | `main.views.home` | public |
| `/gallery/` | `main.views.gallery` | public |
| `/redzone/` | `LoginView` custom | public (form email) |
| `/membres/` | `accounts.views.member_space` | `@login_required` |
| `/admin/` | Django admin | staff |

- `LOGIN_URL = "/redzone/"`
- `LOGIN_REDIRECT_URL = "/membres/"`

## Frontend

### Carousel (`static/js/carousel.js`)
Composant Alpine.js avec :
- Ratio carte 681:1000
- Clonage des cartes pour boucle infinie
- Drag souris + swipe tactile
- Flip 3D au clic (recto : photo, verso : nickname/aka/description)
- Boutons prev/next cachés sur écrans tactiles

### CSS (`static/css/styles.css`)
- Thème dark : fond `#000000`, accents `#ff0000`
- Breakpoints : desktop 1024px+, tablet 768–1024px, mobile ≤768px
- Header fixe : 196px desktop / 80px tablet / 60px mobile
- Footer fixe : 30px

## Commandes utiles

Le projet utilise **uv** pour la gestion des dépendances (pyproject.toml + uv.lock).

```bash
# Installer les dépendances / recréer le venv
uv sync

# Lancer le serveur de dev
uv run manage.py runserver

# Créer un superuser
uv run manage.py createsuperuser

# Appliquer les migrations
uv run manage.py migrate

# Créer une migration
uv run manage.py makemigrations

# Collecter les statics (prod)
uv run manage.py collectstatic

# Export DB
uv run manage.py dumpdata > dbdata.json

# Ajouter une dépendance
uv add <package>
```

## Configuration env (.env)

```
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
# DATABASE_URL= (optionnel, sinon SQLite)
```

## Conventions du projet

- Les membres sont ordonnés par `rank` (ASC) dans le carousel
- Les images membres sont dans `media/members/`
- La langue du site est **français** (`fr-CH`)
- Timezone : CET
- Pas de framework CSS — tout est custom dans `styles.css`
- Alpine.js est chargé en CDN (pas de bundler)

## Ce qui reste à développer

- Page gallery (placeholder vide pour l'instant)
- Espace membres (placeholder — fonctionnalités à définir)
- Profil membre éditable ?
- Formulaire d'inscription ?
