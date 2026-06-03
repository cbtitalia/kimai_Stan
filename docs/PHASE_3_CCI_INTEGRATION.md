# Phase 3 — CCI Integration Plan (June 2026+)

## Context

**Start Date**: 2026-05-26 (CDD begins)  
**Phase 3 Start**: June 2026 (after onboarding complete)  
**Role**: Conseiller Numérique Cybersécurité @ CCI90  

Pointage_Stan needs to reflect **real CCI projects** discovered during onboarding (Phase 1).

---

## Current State (Pre-Phase 3)

### Kimai Projects (V3 Generic)
```
Stan_Pro (ID 13)
├── Presence (Bureau, Réunions, Support, Formation)
└── Absences (Congés, Maladie, Télétravail, Dimanche)

Stan_Perso (ID 14)
├── Homelab (Docker, NAS, VPN, Automatisations)
├── Coding (Python, FastAPI, Obsidian, Learning)
├── Obsidian/Doc (Wiki, Synthèses, Dataview, Maintenance)
└── Vélo (Sorties, Entretien, Entraînement, Matériel)
```

### XKeys Mapping
```
F13 → Stan_Pro (generic work)
F14 → Stan_Perso (personal)
F15 → Divers (catchall)
F16-F20 → Reserved
```

---

## Phase 3 Objectives

### 1. Discover Real CCI Projects

During onboarding (J1-14), identify actual workstreams:

| Discovery | Source | Timeframe |
|-----------|--------|-----------|
| **Cap Cyber 5** | Manager, Jean-Luc Habermacher | J1-2 |
| **Prospection targets** | Bases données CCI | J3-5 |
| **Ateliers** | Apéro du Commerce, territoriaux | J4-7 |
| **Diagnostics MyCyber360°** | Training materials | J8-10 |
| **Formation ISO 27001** | Course schedule | J10-12 |
| **Administrative tasks** | Manager, onboarding | J1-14 |

### 2. Map Projects to Kimai

Create **CCI-specific projects** based on discoveries:

```
Stan_CCI90 (ID 20)  ← NEW: Work at CCI
├── Prospection (Identification, Appels, Emails, Meetings)
├── Ateliers (Sensibilisation, Supports, Facilitation)
├── Diagnostics (Visite entreprise, Questionnaire, Rapport)
├── Cap Cyber (Coordination, Débriefing, Préparation v6)
└── Administration (Integration, Meetings, Documentation)

Stan_ISO27001 (ID 21)  ← NEW: Training & Certification
├── Cours (Modules 1-5, révisions)
├── Examens (Blanc, officiel)
└── Certification (Badge LinkedIn, documentation)

Stan_CapCyber (ID 22)  ← NEW: Event Management
├── Coordination (Planning, vendor liaison, logistics)
├── Participation (Attendance, feedback collection)
└── Débriefing (Analysis, lessons learned, planning v6)

Stan_Perso (ID 14)  ← EXISTING: Keep unchanged
└── (same as before)
```

### 3. Activities per Project

#### Stan_CCI90 Activities

| ID | Prospection | Ateliers | Diagnostics |
|----|------------|----------|-------------|
| 38 | Identification | Sensibilisation | Visite entreprise |
| 39 | Appels téléphoniques | Supports réutilisables | Questionnaire MyCyber |
| 40 | Emails/Messages | Facilitation | Rapport diagnostic |
| 41 | Meetings découverte | — | Follow-up/Plan d'action |

| ID | Cap Cyber | Admin |
|----|-----------|-------|
| 42 | Coordination | Intégration/Onboarding |
| 43 | Débriefing participants | Meetings manager |
| 44 | Planning Cap Cyber 6 | Documentation/Ressources |
| 45 | — | Communications internes |

#### Stan_ISO27001 Activities

| ID | Cours | Révisions | Examen |
|----|-------|-----------|--------|
| 46 | Module 1: Gouvernance | Domaine 1-3 | Blanc |
| 47 | Module 2: Risques | Domaine 4-6 | Officiel |
| 48 | Module 3: Contrôles | Domaine 7-8 | — |
| 49 | Module 4: Certification | Cas pratiques | — |
| 50 | Module 5: Audit | Révisions finales | — |

#### Stan_CapCyber Activities

| ID | Activity |
|----|----------|
| 51 | Coordination logistics |
| 52 | Vendor liaison |
| 53 | Participant feedback |
| 54 | Lessons learned |
| 55 | Cap Cyber 6 planning |

---

## Implementation Timeline

### Week 1 (Onboarding Phase)
- Attend Manager meeting → understand CCI structure
- Contact Cap Cyber coordinator → understand event workload
- Scan training materials → understand ISO 27001 commitment
- **Action**: Document findings in vault

### Week 2 (Prospection Phase)
- Analyze CCI target database
- Draft prospection plan (15-20 targets)
- **Action**: Create list of potential activities from prospection flow

### Week 3-4 (Ateliers Phase)
- Design first atelier
- Identify reusable support creation workflow
- **Action**: Map activities for "Ateliers" project

### Week 4+ (Create Kimai Projects)
- Create projects 20-22 in Kimai UI
- Add activities 38-55
- Test in Kimai admin interface
- **Action**: Document project IDs in `toggle_pointage_cci.py`

### June (Deploy V3 API)
- Deploy `toggle_pointage_v3.py` with new projects
- Deploy `toggle_pointage_cci.py` with CCI activities
- Test API endpoints: `/toggle/stan?project=20`, etc.
- **Action**: Update XKeys script with new project IDs

### June-August (Iterate)
- Use Pointage_Stan to track real CCI work
- Identify missing activities → add them
- Identify unused activities → remove them
- Adjust project/activity structure based on actual usage

---

## Execution Checklist

### Discovery (Week 1-2)
- [ ] Manager meeting: understand CCI structure + projects
- [ ] Cap Cyber coordinator: understand workload + timeline
- [ ] Training center: understand ISO 27001 schedule
- [ ] Database review: understand prospection targets + sectors
- [ ] Document findings in wiki

### Project Creation (Week 4)
- [ ] Create project "Stan_CCI90" in Kimai (ID 20)
- [ ] Create project "Stan_ISO27001" in Kimai (ID 21)
- [ ] Create project "Stan_CapCyber" in Kimai (ID 22)
- [ ] Create activities 38-55 in respective projects
- [ ] Test Kimai UI: verify projects visible + selectable

### API Deployment (Late May / Early June)
- [ ] Update `toggle_pointage_cci.py` with new IDs
- [ ] Deploy to Kimai container: `/volume1/docker/kimai/toggle_pointage_cci.py`
- [ ] Update `docker-compose.yml` to use new API
- [ ] Test endpoints: `/toggle/stan?project=20`, `/toggle/stan?project=21`, etc.
- [ ] Verify API responses include all activities

### XKeys Integration (June)
- [ ] Reprogram XKeys touches 4-6:
  - Touch 4 (F16) → Stan_CCI90
  - Touch 5 (F17) → Stan_ISO27001
  - Touch 6 (F18) → Stan_CapCyber
- [ ] Update `xkeys_pointage_stan.ahk`:
  ```autohotkey
  F16::HandleProjectToggle(20)  ; Stan_CCI90
  F17::HandleProjectToggle(21)  ; Stan_ISO27001
  F18::HandleProjectToggle(22)  ; Stan_CapCyber
  ```
- [ ] Test each touch: verify correct project starts
- [ ] Deploy updated script to production PC

### Go-Live (June 2026)
- [ ] Brief team on new Pointage_Stan projects
- [ ] Monitor usage: check timesheets created correctly
- [ ] Collect feedback: identify missing activities
- [ ] Adjust as needed: add/remove activities based on real usage

---

## Post-Phase 3 Evolution

As you discover more about CCI work:

### Quarterly Reviews
- Analyze Kimai data: which activities get tracked most?
- Identify unused activities: remove clutter
- Identify missing activities: add new ones
- Update XKeys mapping if projects change priority

### Examples of Evolution
- Ateliers becomes very active → split into sub-categories
- Prospection drops → merge into broader category
- CCI requests new project → create new Kimai project + XKeys touch

---

## Related Documentation

- **Vault**: Brain_Stan → Pro/CCI/Plan-100-jours-CCI90 (detailed workstreams)
- **Onboarding**: Brain_Stan → Pro/CCI/Checklist-Jour-1
- **Cap Cyber**: Brain_Stan → Pro/CCI/Cap-Cyber-5-Debriefing
- **Repo**: This kimai_Stan repo → toggle_pointage_cci.py (Phase 3 code)

---

## Success Metrics

By end of Phase 3 (September 2026):

| Metric | Target | Verified By |
|--------|--------|------------|
| CCI projects tracked | 3+ projects daily | Kimai dashboard |
| Timesheet accuracy | 95%+ (vs manual tracking) | Audit 2-week period |
| Activity utilization | 80%+ of activities used | Kimai reports |
| User adoption | 100% of team (if applicable) | Usage logs |
| Documentation | Phase 3 complete + updated | This file + wiki |

---

*Last updated: 2026-06-03*  
*Status: Planning (Phase 3 starts June 2026)*
