---
title: "Pointage Stan & Ronfort — Installation complète Kimai Docker"
tags: [pointage, kimai, docker, nfc, ronfort, synthese]
date: 2026-04-25
type: synthese
1=: pointage
2=: Kimai
3=: doc projet
4=: compte-rendu
---

- REF
  - 1= theme:: [[1=pointage]]
  - 2= marque:: [[2=Kimai]]
  - 3= systeme:: [[3=doc projet]]
  - 4= type:: [[4=compte-rendu]]

# Pointage Stan & Ronfort — Installation complète Kimai Docker

> Session du 2026-04-24 au 2026-04-25. Installation de bout en bout de deux instances Kimai sur Synology `192.168.1.15`.

---

## Architecture déployée

```
Badge NFC → IP publique fixe → Synology 192.168.1.15
    ├── kimai1 (Stan)   : port 8055 (Kimai) + 8059 (toggle)
    └── kimai2 (Ronfort): port 8060 (Kimai) + 8065 (toggle)
```

Pas de Cloudflare, pas de domaine, pas de Drive Sync — IP fixe SFR + redirection de port.

---

## kimai1 — Stan (opérationnel)

| Composant | Détail |
|---|---|
| Dossier | `/volume1/docker/kimai` |
| Accès local | `http://192.168.1.15:8055` |
| Toggle | `http://93.0.162.95:8059/toggle/stan` |
| Utilisateur | Stan (1 personne) |
| IDs | Présence=1, Pointage journalier=1 |

**Scripts automatiques :**
- `kimai_alerte_anomalies.py` → cron 8h lun-ven (Planificateur Synology)
- `kimai_alerte_soir.py` → cron 18h tous les jours (récap 7 jours + alerte impair)
- Sauvegarde MySQL → cron 2h quotidien

**Alerte soir :** email quotidien avec détail du jour (heure début/fin, durée, total) + tableau 7 jours glissants. Bandeau vert (OK) / orange (impair) / rouge (pointage actif à 18h).

---

## kimai2 — Ronfort (opérationnel)

| Composant | Détail |
|---|---|
| Dossier | `/volume1/docker/kimai2` |
| Accès local | `http://192.168.1.15:8060` |
| Accès externe | `http://93.0.162.95:8060` |
| Toggle Eric | `http://93.0.162.95:8065/toggle/eric` |
| Toggle Florian | `http://93.0.162.95:8065/toggle/florian` |
| Toggle Pascal | `http://93.0.162.95:8065/toggle/pascal` |
| Utilisateurs | Eric, Florian, Pascal |
| IDs | Présence=2, Pointage journalier=1 |

---

## Décisions techniques retenues

| Décision | Choix | Raison |
|---|---|---|
| Accès externe | IP fixe + port forwarding | Gratuit, simple, pas de domaine requis |
| NFC → toggle | URL HTTP dans tag NDEF | Badge scanné → navigateur → page HTML 2s |
| Page toggle | HTML vert/rouge auto-fermante | Feedback visuel immédiat sans app |
| Jours fériés | Hardcodés dans les scripts | Kimai 2.55.0 sans module holidays |
| Export mensuel | Kimai natif | Pas de script nécessaire |
| Alertes | Email Gmail SMTP | Système existant réutilisé |

---

## Points techniques notés

- `/volume1/docker/` obligatoire sur Synology (pas `~/`) — le home peut être effacé à la mise à jour DSM
- `sudo docker compose` requis (pas de permission sans sudo)
- Mot de passe MySQL : éviter `@` et `%` → cassent la DATABASE_URL dans Kimai
- `TZ=Europe/Paris` à ajouter dans docker-compose.yml pour corriger le décalage +2h
- Fichiers scripts montés via volume `/volume1/docker/kimai:/scripts` dans le conteneur toggle
- `load_dotenv("/scripts/.env")` dans les scripts Python (chemin interne Docker)
- `cat << 'ENDSCRIPT' > fichier` pour écrire les scripts depuis SSH (pas `python3 << EOF`)

---

## À faire — Ronfort (suite)

Suivi : [[A faire - Pointage_Ronfort]]

- [ ] Programmer les 3 cartes NFC (NFC Tools)
- [ ] `kimai_alerte_anomalies.py` pour kimai2
- [ ] `kimai_alerte_soir.py` pour kimai2
- [ ] Sauvegarde MySQL kimai2 (Planificateur Synology)
- [ ] Tests en parallèle 2 semaines

---

## Références

- [[A faire - Pointage_Stan]] — Suivi projet Stan
- [[A faire - Pointage_Ronfort]] — Suivi projet Ronfort
- [[pointage-stan-kimai-docker]] — Procédure Docker
- [[pointage-stan-toggle-script]] — Script toggle NFC
- [[pointage-stan-alerte-anomalies]] — Scripts alertes
