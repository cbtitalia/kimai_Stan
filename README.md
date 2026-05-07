# Kimai2 — Timesheet & Pointage

Docker setup et configuration pour Kimai2 (timesheet/pointage) sur Synology NAS.

## Contenu

- **docker-compose.yml** — Configuration Kimai2 + MariaDB
- **Dockerfile** — Image customisée si nécessaire
- **Scripts Python** :
  - `kimai_alerte_anomalies.py` — Détection anomalies pointage
  - `kimai_alerte_soir.py` — Alertes fin de journée
  - `toggle_pointage.py` — Basculer statut pointage
- **requirements.txt** — Dépendances Python
- **.env** — Configuration (secrets, ports, etc.)
- **backups/** — Sauvegardes base de données

## Documentation

Voir `/docs/` pour :
- `pointage-stan-kimai-docker.md` — Setup Docker complet
- `pointage-kimai-installation.md` — Procédure installation
- `pointage-stan-kimai-configuration.md` — Configuration détaillée

## Démarrage

```bash
cd /volume1/docker/kimai
docker-compose up -d
```

## Service

- Web UI : http://192.168.1.15:8001 (ou port configuré dans .env)
- Database : MariaDB interne (port 3306)

## Infrastructure

- **Plateforme** : Synology NAS (192.168.1.15)
- **Statut** : Production actif
- **Backup** : Voir backups/ et docs pour stratégie

---

Documentation centralisée depuis [Brain_Stan Vault](https://github.com/cbtitalia/Brain_Stan)
