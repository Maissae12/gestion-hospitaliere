# MediGest – Application de Gestion Hospitalière

Application CRUD complète développée avec **Django + Django REST Framework** (backend) et **Vue.js 3** (frontend SPA).

---

## Technologies utilisées

| Couche | Technologie |
|--------|-------------|
| Backend | Django 6, Django REST Framework |
| Frontend SPA | Vue.js 3 (Composition API, CDN) |
| Communication | Axios (requêtes HTTP / JSON) |
| CSS | Bootstrap 5.3 |
| Base de données | MySQL |
| Auth | Session Django + protection CSRF |

---

## Installation

### 1. Cloner / extraire le projet

```bash
cd gestionhopitale
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install django djangorestframework django-cors-headers mysqlclient
```

### 4. Configurer la base de données MySQL

```sql
CREATE DATABASE gestionhopitale CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'djangouser'@'localhost' IDENTIFIED BY 'MAISSAE12345';
GRANT ALL PRIVILEGES ON gestionhopitale.* TO 'djangouser'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

---
## Installation avec Docker (recommandé)

Ce projet est dockerisé. Le conteneur contient Python 3.12, Django et toutes les dépendances nécessaires, il n'est pas nécessaire d'installer Python ou les packages directement sur la machine.

Note : la base de données MySQL doit être installée et lancée séparément sur la machine (ou sur un serveur accessible). Le conteneur Docker s'y connecte via les identifiants du fichier `.env`.

### Prérequis
- Docker Desktop (avec Docker Compose)
- Un serveur MySQL actif (local ou distant)

### Configuration

Créer un fichier `.env` à la racine du projet avec les variables nécessaires, par exemple :
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=gestionhopitale
DB_USER=djangouser
DB_PASSWORD=MAISSAE12345
DB_HOST=host.docker.internal
DB_PORT=3306

Comme MySQL tourne sur l'hôte (la machine) et non dans un conteneur, utiliser `host.docker.internal` comme `DB_HOST` (au lieu de `localhost`) pour que le conteneur puisse joindre la base de données.

### Lancer le projet

```bash
docker compose up --build
```

Ou en arrière-plan :

```bash
docker compose up -d
```

L'application sera accessible sur : `http://localhost:8000/`

### Commandes utiles

```bash
docker compose logs -f              # Voir les logs en direct
docker compose stop                 # Arrêter le conteneur (sans le supprimer)
docker compose start                # Redémarrer
docker compose down                 # Arrêter et supprimer le conteneur
docker compose exec web python manage.py migrate           # Appliquer les migrations
docker compose exec web python manage.py createsuperuser   # Créer un superutilisateur
docker compose exec web bash        # Accéder au shell du conteneur
```


### Points clés de la configuration

- Le volume `.:/app` monte le code source dans le conteneur, ce qui permet au serveur de développement Django de détecter les changements en direct (StatReloader), sans reconstruire l'image à chaque modification.
- Reconstruire l'image est nécessaire uniquement après modification du `Dockerfile` ou de `requirements.txt` :

```bash
docker compose up --build
```
## Accès à l'application

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Page de connexion |
| `http://127.0.0.1:8000/home_dashboard/` | Dashboard principal |
| `http://127.0.0.1:8000/hopital/` | Interface Django classique |
| `http://127.0.0.1:8000/vue/` | **Interface Vue.js SPA** |
| `http://127.0.0.1:8000/api/` | **API REST (navigable)** |
| `http://127.0.0.1:8000/admin/` | Administration Django |

---

## Endpoints API REST

Tous les endpoints suivent le standard REST (GET / POST / PUT / PATCH / DELETE).  
L'authentification par session est requise.

### Étudiants
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/etudiants/` | Liste tous les étudiants |
| POST | `/api/etudiants/` | Créer un étudiant |
| GET | `/api/etudiants/{id}/` | Détail d'un étudiant |
| PUT | `/api/etudiants/{id}/` | Modifier un étudiant |
| PATCH | `/api/etudiants/{id}/` | Modification partielle |
| DELETE | `/api/etudiants/{id}/` | Supprimer un étudiant |

**Filtres disponibles** : `?q=nom`, `?ville=Casablanca`, `?filiere=GI`, `?niveau=GI1`, `?sexe=M`

### Médecins
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/medecins/` | Liste tous les médecins |
| POST | `/api/medecins/` | Créer un médecin |
| GET | `/api/medecins/{id}/` | Détail d'un médecin |
| PUT | `/api/medecins/{id}/` | Modifier un médecin |
| DELETE | `/api/medecins/{id}/` | Supprimer un médecin |

**Filtres** : `?q=nom`, `?specialite=Cardio`

### Dossiers médicaux
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/dossiers/` | Liste tous les dossiers |
| POST | `/api/dossiers/` | Créer un dossier |
| PUT | `/api/dossiers/{id}/` | Modifier un dossier |
| DELETE | `/api/dossiers/{id}/` | Supprimer un dossier |

**Filtres** : `?q=etudiant`, `?groupe_sanguin=A+`

### Rendez-vous
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/rendezvous/` | Liste tous les RDV |
| POST | `/api/rendezvous/` | Créer un RDV |
| PUT | `/api/rendezvous/{id}/` | Modifier un RDV |
| DELETE | `/api/rendezvous/{id}/` | Supprimer un RDV |

**Filtres** : `?q=nom`, `?statut=prévu`, `?date_rdv=2025-01-15`

### Consultations
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/consultations/` | Liste toutes les consultations |
| POST | `/api/consultations/` | Créer une consultation |
| PUT | `/api/consultations/{id}/` | Modifier une consultation |
| DELETE | `/api/consultations/{id}/` | Supprimer une consultation |

### Médicaments
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/medicaments/` | Liste tous les médicaments |
| POST | `/api/medicaments/` | Créer un médicament |
| PUT | `/api/medicaments/{id}/` | Modifier un médicament |
| DELETE | `/api/medicaments/{id}/` | Supprimer (si non utilisé) |

### Prescriptions
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/prescriptions/` | Liste toutes les prescriptions |
| POST | `/api/prescriptions/` | Créer une prescription |
| PUT | `/api/prescriptions/{id}/` | Modifier |
| DELETE | `/api/prescriptions/{id}/` | Supprimer |

### Vaccinations
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/vaccinations/` | Liste toutes les vaccinations |
| POST | `/api/vaccinations/` | Créer une vaccination |
| PUT | `/api/vaccinations/{id}/` | Modifier |
| DELETE | `/api/vaccinations/{id}/` | Supprimer |

---

## Exemples de requêtes API

### Créer un étudiant (POST)
```bash
curl -X POST http://127.0.0.1:8000/api/etudiants/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{
    "nom": "Alaoui",
    "prenom": "Youssef",
    "CIN": "BK123456",
    "CNE": "R134567890",
    "date_naissance": "2002-05-10",
    "filiere": "GI",
    "niveau": "GI2",
    "sexe": "M",
    "telephone": "0612345678",
    "ville": "Casablanca"
  }'
```

### Modifier un médecin (PUT)
```bash
curl -X PUT http://127.0.0.1:8000/api/medecins/1/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"nom":"Benali","prenom":"Hassan","specialite":"Cardiologie","telephone":"0661234567","rdv_jr":10,"salaire":15000}'
```

### Supprimer un étudiant (DELETE)
```bash
curl -X DELETE http://127.0.0.1:8000/api/etudiants/3/ \
  -H "X-CSRFToken: <token>"
```

---

## Structure du projet

```
gestionhopitale/
├── gestionhopitale/
│   ├── settings.py        # Config 
│   ├── urls.py            # Routes principales + /api/ + /vue/
│   └── wsgi.py
├── hopital/
│   ├── models.py          # Modèles de données
│   ├── serializers.py     #  Sérialiseurs DRF
│   ├── api_views.py       # ViewSets REST API
│   ├── api_urls.py        #  Routes API (router DRF)
│   ├── views.py           # Vues Django classiques + vue_spa
│   ├── urls.py            # Routes vues classiques
│   ├── forms.py           # Formulaires Django
│   ├── validators.py      # Validateurs personnalisés
│   └── templates/
│       └── hopital/
│           ├── vue_spa.html  # 
│           ├── baseagent.html
│           ├── basemedecin.html
│           └── ...
├── static/
├── manage.py
└── README.md              
```

---

## Fonctionnalités implémentées (cahier des charges)

### API REST (Django REST Framework)
- [x] Architecture REST complète (ViewSets + Router)
- [x] Serializers pour chaque modèle avec validation
- [x] Toutes les opérations CRUD via HTTP (GET/POST/PUT/PATCH/DELETE)
- [x] Gestion des erreurs HTTP (400, 404, 500)
- [x] Filtres et recherche via paramètres GET
- [x] Pagination (20 éléments par page)
- [x] API Browsable (interface web DRF navigable)

###  Vue.js SPA (`/vue/`)
- [x] Composition API (Vue 3)
- [x] Dashboard avec statistiques en temps réel
- [x] Interface CRUD dynamique pour chaque entité
- [x] Tableau de données avec recherche
- [x] Modal d'ajout/modification avec pré-remplissage
- [x] Confirmation avant suppression
- [x] Notifications toast (succès / erreur)
- [x] États de chargement (spinner)
- [x] Pagination
- [x] Validation côté client (champs obligatoires)
- [x] Affichage des erreurs serveur dans le formulaire
- [x] Menu latéral (sidebar) responsive
- [x] Navigation SPA sans rechargement de page

### Sécurité
- [x] Protection CSRF sur toutes les requêtes
- [x] Authentification requise pour l'API
- [x] Validation côté serveur (serializers)
- [x] CORS configuré pour Vue.js en développement

### Existant conservé
- [x] Interface Django classique inchangée
- [x] Base de données MySQL identique
- [x] Tous les modèles, vues, templates, formulaires originaux
