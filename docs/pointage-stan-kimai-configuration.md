---
title: "Pointage_Ronfort — Configuration Kimai — Workflow"
tags: [pointage, kimai, configuration, workflow, ronfort, proj4-pointage]
date: 2026-04-25
type: procédure
statut: actif
1=: pointage
2=: Kimai
3=: procédure locale
4=: procédure
---

- REF
  - 1= theme:: [[1=pointage]]
  - 2= marque:: [[2=Kimai]]
  - 3= systeme:: [[3=procédure locale]]
  - 4= type:: [[4=procédure]]

# Kimai2 — Workflow de configuration Ronfort (3 employés)

> Guide de configuration de kimai2 pour PF Ronfort : Eric, Florian, Pascal.
> Instance : `http://192.168.1.15:8060` — Toggle : port `8065`
> Prérequis : kimai2 installé → [[pointage-stan-kimai-docker]]

---

## Vue d'ensemble

```
![[pointage-ronfort-configuration-workflow.excalidraw]]

```
1. Première connexion & mot de passe admin
        ↓
2. Paramètres système (langue, fuseau horaire)
        ↓
3. Créer les 3 utilisateurs (Eric, Florian, Pascal)
        ↓
4. Créer les projets (Présence, Absences)
        ↓
5. Créer les activités (Pointage journalier, Congé légal, Astreinte)
        ↓
6. Récupérer les 3 tokens API
        ↓
7. Mettre à jour toggle_pointage.py
        ↓
8. Tester les 3 badges NFC
```

---

## Étape 1 — Première connexion

**URL :** `http://192.168.1.15:8060`

- Email : `admin@pointage.local`
- Mot de passe : `AdminPassAChanger!`

> [!danger] Changer le mot de passe admin immédiatement
> Avatar → **Profil → Sécurité → Modifier le mot de passe**

---

## Étape 2 — Paramètres système

**Administration → Paramètres → Système**

| Paramètre | Valeur |
|---|---|
| Langue | Français |
| Fuseau horaire | Europe/Paris |
| Nom de l'application | Pointage Ronfort |

---

## Étape 3 — Créer les 3 utilisateurs

**Administration → Utilisateurs → + Nouvel utilisateur** (×3)

| Nom | Email | Rôle | Mot de passe |
|---|---|---|---|
| Eric | eric@ronfort.local | ROLE_USER | (choisir) |
| Florian | florian@ronfort.local | ROLE_USER | (choisir) |
| Pascal | pascal@ronfort.local | ROLE_USER | (choisir) |

---

## Étape 4 — Créer les projets

**Administration → Projets → + Nouveau projet**

| Projet | Client | ID obtenu |
|---|---|---|
| `Présence` | PF Ronfort | `2` |
| `Absences` | PF Ronfort | `1` |

> [!warning] Vérifier les IDs réels via API
> ```bash
> curl -s http://192.168.1.15:8060/api/projects -H "Authorization: Bearer TOKEN_ADMIN"
> ```

---

## Étape 5 — Créer les activités

**Administration → Activités → + Nouvelle activité**

| Activité | Projet | ID obtenu |
|---|---|---|
| `Pointage journalier` | Présence | `1` |
| `Congé légal` | Absences | `2` |
| `Astreinte` | Absences | `3` |

> [!warning] Vérifier les IDs réels via API
> ```bash
> curl -s http://192.168.1.15:8060/api/activities -H "Authorization: Bearer TOKEN_ADMIN"
> ```

---

## Étape 6 — Récupérer les 3 tokens API

Pour **chaque employé**, se connecter avec **son propre compte** :

1. Se connecter avec le compte Eric → Avatar → **Profil → API** → copier le token
2. Répéter pour Florian et Pascal

| Employé | Token API | User ID |
|---|---|---|
| Eric | `dd0bf45f66ec2870035e79f26` | 2 |
| Florian | `09185ffac0761b9b9dfa3dea2` | 3 |
| Pascal | `7757ffad7bbe7433332148733` | 4 |
| Admin | `c4528b4a9967d0b197d3fdbea` | 1 |

---

## Étape 7 — Mettre à jour `toggle_pointage.py`

Fichier : `/volume1/docker/kimai2/toggle_pointage.py`

Variables clés à vérifier :

```python
KIMAI_URL = "http://kimai:8001/api"
PROJECT   = 2      # ID projet Présence
ACTIVITY  = 1      # ID activité Pointage journalier

EMPLOYES = {
    "eric":    "dd0bf45f66ec2870035e79f26",
    "florian": "09185ffac0761b9b9dfa3dea2",
    "pascal":  "7757ffad7bbe7433332148733",
}
```

Après modification, rebuild :
```bash
cd /volume1/docker/kimai2 && sudo docker compose up -d --build --force-recreate toggle
```

---

## Étape 8 — Tester les 3 badges

```bash
# Test Eric
curl -s http://192.168.1.15:8065/toggle/eric | grep texte

# Test Florian
curl -s http://192.168.1.15:8065/toggle/florian | grep texte

# Test Pascal
curl -s http://192.168.1.15:8065/toggle/pascal | grep texte
```

Résultats attendus :
- `Pointage debut Eric` (vert) → `Pointage fin Eric` (rouge)
- Idem pour Florian et Pascal

Vérifier dans Kimai : **Administration → Tous les temps**

---

## Commandes de diagnostic

```bash
# Statut containers kimai2
cd /volume1/docker/kimai2 && sudo docker compose ps

# Vérifier tous les pointages (admin)
curl -s "http://192.168.1.15:8060/api/timesheets?user=all" \
  -H "Authorization: Bearer c4528b4a9967d0b197d3fdbea"

# Logs toggle kimai2
sudo docker compose logs -f toggle
```

---

## URLs toggle Ronfort

| Employé | URL NFC externe |
|---|---|
| Eric | `http://93.0.162.95:8065/toggle/eric` |
| Florian | `http://93.0.162.95:8065/toggle/florian` |
| Pascal | `http://93.0.162.95:8065/toggle/pascal` |

---

## Références

- [[A faire - Pointage_Ronfort]] — suivi des tâches
- [[pointage-stan-kimai-docker]] — Installation Docker
- [[pointage-stan-toggle-script]] — Script toggle NFC
- [[pointage-stan-alerte-anomalies]] — Scripts alertes
