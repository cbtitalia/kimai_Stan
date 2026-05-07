---
title: "Pointage_Stan — Kimai installation Docker"
tags: [pointage, kimai, docker, installation, proj4-pointage]
date: 2026-04-24
type: procédure
statut: actif
1=: homelab
2=: Kimai
3=: procédure locale
4=: procédure
---

- REF
  - 1= theme:: [[1=homelab]] [[1=docker]]
  - 2= marque:: [[2=Kimai]]
  - 3= systeme:: [[3=procédure locale]]
  - 4= type:: [[4=procédure]]

# Kimai — Installation Docker

> Procédure d'installation de Kimai via Docker Compose sur Synology NAS `192.168.1.15`.
> Kimai est une application open source de suivi du temps, auto-hébergée, sans abonnement.
> Projet : [[_index|Pointage_Stan]]

---

## Architecture déployée

| Conteneur | Image | Port interne | Port exposé | Rôle |
|---|---|---|---|---|
| `kimai_mysql` | mysql:8.3 | 3306 | — (interne) | Base de données |
| `kimai_app` | kimai/kimai2:apache | 8001 | **8055** | Interface web + API REST |

Accès local : `http://192.168.1.15:8055`

---

## Prérequis

- Container Manager installé sur le Synology (DSM → Centre de paquets)
- Accès SSH activé : Panneau de configuration → Terminal & SNMP → Service SSH → Activer
- Se connecter en SSH : `ssh cbtitalia@192.168.1.15`
- ~1 Go de RAM libre sur le NAS
- Port `8055` non utilisé par un autre service

> [!tip] Vérifier la RAM disponible
> ```bash
> free -h
> ```
> Colonne `available` doit afficher > 1G.

---

## Étape 1 — Préparer le dossier

> [!warning] Toujours utiliser `/volume1/` sur Synology
> Le dossier home (`/var/services/homes/cbtitalia/`) affiche un warning "may be deleted when the system is updated/restarted" — il peut disparaître lors d'une mise à jour DSM.
> `/volume1/` est le volume de stockage principal du NAS, persistant.

```bash
sudo mkdir -p /volume1/docker/kimai
sudo mkdir -p /volume1/docker/kimai/backups
cd /volume1/docker/kimai
```

Vérifier que le dossier est bien créé :

```bash
ls -la /volume1/docker/kimai
```

---

## Étape 2 — Créer le fichier `.env`

Le fichier `.env` contient tous les secrets (mots de passe, clés). Il n'est **jamais** partagé ni versionné.

```bash
nano /volume1/docker/kimai/.env
```

Contenu à coller :

```ini
# Kimai — variables d'environnement
# Ne jamais versionner ce fichier — chmod 600

# Base de données MySQL
DATABASE_PASSWORD=MotDePasseForTComplexe!
DATABASE_ROOT_PASSWORD=RootPasswordComplexe!

# Clé secrète Kimai (64 caractères aléatoires)
KIMAI_SECRET=coller_ici_la_chaine_generee

# SMTP Gmail pour les emails (notifications, exports)
SMTP_FROM=pfronfort90000@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=pfronfort90000@gmail.com
SMTP_PASSWORD=xxxx_xxxx_xxxx_xxxx

# API Kimai (à remplir après création des utilisateurs — Phase 2)
KIMAI_URL=http://localhost:8055/api
TOKEN_STAN=a_remplir_apres_phase_2
```

Sauvegarder : `Ctrl+O` → `Entrée` → `Ctrl+X`

Sécuriser le fichier (lecture propriétaire uniquement) :

```bash
chmod 600 /volume1/docker/kimai/.env
```

Vérifier :

```bash
ls -la /volume1/docker/kimai/.env
# Doit afficher : -rw------- 1 root ...
```

> [!tip] Générer `KIMAI_SECRET` (64 caractères hexadécimaux)
>
> **Depuis SSH sur le Synology :**
> ```bash
> cat /proc/sys/kernel/random/uuid | tr -d '-' | head -c 64
> ```
>
> **Depuis PowerShell Windows :**
> ```powershell
> -join ((1..64) | ForEach-Object { "0123456789abcdef"[(Get-Random -Max 16)] })
> ```
>
> Exemple de résultat : `a3f8c2d1e4b9f0a7c3d2e1f4b8c9d0e2a3f8c2d1e4b9f0a7c3d2e1f4b8c9d0e2`

> [!info] Mot de passe Gmail SMTP (`SMTP_PASSWORD`)
> Gmail n'accepte pas le mot de passe du compte pour l'envoi SMTP — il faut un **mot de passe d'application** généré par Google.
>
> **Créer un mot de passe d'application :**
> 1. Aller sur **myaccount.google.com** avec le compte `pfronfort90000@gmail.com`
> 2. **Sécurité → Validation en deux étapes** → doit être activée (obligatoire)
> 3. En bas de la page → **Mots de passe des applications**
> 4. Nom : `Kimai Synology` → **Créer**
> 5. Google génère un code format `xxxx xxxx xxxx xxxx` → copier immédiatement (affiché une seule fois)
> 6. Coller ce code dans `SMTP_PASSWORD` — les espaces sont acceptés tels quels
>
> > Le mot de passe `qnvg hrct vpuw wzhq` utilisé dans les anciens scripts est déjà un mot de passe d'application valide pour ce compte — il peut être réutilisé directement.

---

## Étape 3 — Créer `docker-compose.yml`

```bash
nano /volume1/docker/kimai/docker-compose.yml
```

Contenu :

```yaml
services:

  mysql:
    image: mysql:8.3
    container_name: kimai_mysql
    environment:
      MYSQL_DATABASE: kimai
      MYSQL_USER: kimai
      MYSQL_PASSWORD: ${DATABASE_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DATABASE_ROOT_PASSWORD}
    volumes:
      - kimai_mysql:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  kimai:
    image: kimai/kimai2:apache
    container_name: kimai_app
    environment:
      ADMINMAIL: admin@pointage.local
      ADMINPASS: AdminPassAChanger!
      APP_SECRET: ${KIMAI_SECRET}
      DATABASE_URL: mysql://kimai:${DATABASE_PASSWORD}@mysql/kimai?charset=utf8mb4&serverVersion=8.3
      MAILER_DSN: smtp://${SMTP_USER}:${SMTP_PASSWORD}@${SMTP_HOST}:${SMTP_PORT}
      MAILER_FROM: ${SMTP_FROM}
    ports:
      - "8055:8001"
    depends_on:
      mysql:
        condition: service_healthy
    volumes:
      - kimai_data:/opt/kimai/var/data
      - kimai_public:/opt/kimai/public/avatars
    restart: unless-stopped

volumes:
  kimai_mysql:
  kimai_data:
  kimai_public:
```

Sauvegarder : `Ctrl+O` → `Entrée` → `Ctrl+X`

> [!info] Explication des paramètres clés
> - `depends_on: condition: service_healthy` — Kimai attend que MySQL soit prêt avant de démarrer
> - `restart: unless-stopped` — redémarrage automatique après reboot du NAS
> - `ports: "8055:8001"` — le port 8001 interne est exposé sur le port 8055 du Synology
> - Les volumes nommés (`kimai_mysql`, `kimai_data`) persistent même si les conteneurs sont supprimés

---

## Étape 4 — Lancer Kimai

```bash
cd /volume1/docker/kimai
sudo docker compose up -d
```

Docker télécharge les images (MySQL ~600 Mo + Kimai ~300 Mo) puis démarre les conteneurs.

Résultat attendu :
```
✔ Network kimai_default       Created
✔ Volume "kimai_kimai_mysql"  Created
✔ Volume "kimai_kimai_data"   Created
✔ Volume "kimai_kimai_public" Created
✔ Container kimai_mysql       Healthy
✔ Container kimai_app         Started
```

Suivre les logs de démarrage :

```bash
sudo docker compose logs -f kimai
```

Attendre la ligne confirmant que Kimai est prêt :
```
NOTICE: ready to handle connections
```

Quitter les logs : `Ctrl+C`

Vérifier que les deux conteneurs sont actifs :

```bash
sudo docker compose ps
```

Les deux doivent afficher `running` (kimai_app) et `healthy` (kimai_mysql).

> [!note] Premier démarrage
> La première fois, MySQL initialise la base de données et Kimai effectue les migrations — compter 1 à 2 minutes. Les démarrages suivants sont quasi-instantanés.

---

## Étape 5 — Première connexion

Ouvrir dans le navigateur depuis le réseau local :

```
http://192.168.1.15:8055
```

Se connecter avec les identifiants par défaut :
- **Email** : `admin@pointage.local`
- **Mot de passe** : `AdminPassAChanger!`

> [!danger] Changer le mot de passe admin immédiatement
> **Cliquer sur l'avatar en haut à droite → Profil → onglet Sécurité → Modifier le mot de passe**
> Choisir un mot de passe fort et le noter dans le `.env` ou un gestionnaire de mots de passe.

---

## Commandes du quotidien

```bash
# Statut des conteneurs
sudo docker compose ps

# Logs en temps réel (tous les conteneurs)
sudo docker compose logs -f

# Logs Kimai uniquement
sudo docker compose logs -f kimai

# Logs MySQL uniquement
sudo docker compose logs -f mysql

# Redémarrer Kimai (sans toucher MySQL)
sudo docker compose restart kimai

# Arrêter tous les conteneurs (données conservées)
sudo docker compose stop

# Redémarrer après un stop
sudo docker compose start

# Supprimer les conteneurs (volumes et données conservés)
sudo docker compose down
```

> [!warning] Ne jamais faire `docker compose down -v` en production
> L'option `-v` supprime aussi les volumes → perte totale des données Kimai et MySQL.

---

## Mise à jour Kimai

```bash
cd /volume1/docker/kimai

# Télécharger les nouvelles images
sudo docker compose pull

# Relancer avec les nouvelles versions
sudo docker compose up -d

# Vérifier la version active
sudo docker exec kimai_app bin/console kimai:version
```

> Kimai effectue automatiquement les migrations de base de données au démarrage.

---

## Sauvegarde

### Créer le dossier de sauvegardes

```bash
mkdir -p /volume1/docker/kimai/backups
```

### Sauvegarder la base de données

```bash
sudo docker exec kimai_mysql \
  mysqldump -u kimai -pMotDePasseForTComplexe! kimai \
  > /volume1/docker/kimai/backups/kimai_$(date +%Y%m%d).sql
```

### Sauvegarder les fichiers (avatars, pièces jointes)

```bash
sudo docker run --rm \
  -v kimai_kimai_data:/data \
  -v /volume1/docker/kimai/backups:/backup \
  alpine tar czf /backup/kimai_data_$(date +%Y%m%d).tar.gz /data
```

### Automatiser via le Planificateur Synology

Panneau de configuration → **Planificateur de tâches → Créer → Tâche planifiée → Script utilisateur**

| Paramètre | Valeur |
|---|---|
| Nom | Kimai — Sauvegarde MySQL quotidienne |
| Utilisateur | root |
| Planification | Quotidienne à 02h00 |
| Commande | `docker exec kimai_mysql mysqldump -u kimai -pMotDePasseForTComplexe! kimai > /volume1/docker/kimai/backups/kimai_$(date +\%Y\%m\%d).sql` |

---

## Mot de passe MySQL

Le mot de passe actuel de la base Kimai est `KimaiStan2026x` (changé le 2026-04-24).

> [!warning] Éviter les caractères spéciaux `@`, `%`, `!` dans le mot de passe MySQL
> Ces caractères cassent le parsing de la `DATABASE_URL` dans Kimai (le `@` est interprété comme séparateur host/credentials).
> Si le mot de passe doit être changé, utiliser uniquement lettres, chiffres, `-`, `_`, `x`.

Pour changer le mot de passe :
```bash
# 1. Changer dans MySQL
docker exec -it kimai_mysql mysql -u root -pMOT_DE_PASSE_ROOT -e 'ALTER USER '"'"'kimai'"'"'@'"'"'%'"'"' IDENTIFIED BY '"'"'NOUVEAU_MDP'"'"'; FLUSH PRIVILEGES;'

# 2. Mettre à jour le .env
python3 -c "
content = open('/volume1/docker/kimai/.env').read()
content = '\n'.join(['DATABASE_PASSWORD=NOUVEAU_MDP' if l.startswith('DATABASE_PASSWORD=') else l for l in content.splitlines()])
open('/volume1/docker/kimai/.env','w').write(content)
"

# 3. Recréer les conteneurs
cd /volume1/docker/kimai && sudo docker compose up -d --force-recreate
```

---

## Dépannage

| Problème | Cause probable | Solution |
|---|---|---|
| `permission denied` sur docker.sock | Utilisateur non dans le groupe docker | Utiliser `sudo docker compose` |
| Kimai ne démarre pas | MySQL pas encore prêt | Attendre, vérifier `docker compose logs mysql` |
| Page blanche sur :8055 | Kimai encore en initialisation | Attendre 1-2 min, rafraîchir |
| `ERR_EMPTY_RESPONSE` sur :8055 | Kimai encore en démarrage après restart | Attendre 1-2 min |
| `getaddrinfo failed` dans les logs | `@` ou `%` dans le mot de passe MySQL | Changer le mot de passe (sans caractères spéciaux) |
| Erreur 500 | Mauvaise `DATABASE_URL` dans `.env` | Vérifier les mots de passe dans `.env` |
| Conteneur redémarre en boucle | `KIMAI_SECRET` trop court | Regénérer une clé de 64 caractères |
| `may be deleted` au login SSH | Dossier dans `/var/services/homes/` | Toujours utiliser `/volume1/docker/kimai/` |

---

## Références

- [[pointage-stan-installation]] — Architecture complète Kimai + NFC
- [[pointage-stan-nfc-android]] — Configuration cartes NFC
- [[_index|Index Pointage_Stan]]
- Kimai Docker Hub : https://hub.docker.com/r/kimai/kimai2
- Kimai documentation : https://www.kimai.org/documentation/docker.html
