# Pointage_Stan — Project Status (2026-06-03)

## Current State

### Production (NAS 192.168.1.15:8055)
- **Status**: ✅ Running (MySQL + Kimai + Toggle API)
- **Architecture**: Minimal (1 project, 1 activity, simple toggle)
- **API**: `toggle_pointage_stan_prod.py` — basic start/stop only
- **Database**: MySQL 8.3 in Docker
- **Location**: `/volume1/docker/kimai/`

### Sandbox (Port 8056)
- **Status**: 🚀 Launching (created 2026-06-03 21:11)
- **Purpose**: Test V3 architecture before production deployment
- **Config**: `docker-compose.sandbox.yml` (isolated DB, volumes, credentials)
- **Expected Startup**: 1-2 minutes for Kimai boot
- **Access**: http://192.168.1.15:8056 (admin@sandbox.local / SandboxAdmin2026!)

---

## Architecture V3 (Ready for Sandbox Testing)

### Projects
- **Stan_Pro** (ID 13) — Professional work
  - Presence (Bureau, Réunions, Support, Formation)
  - Absences (Congés, Maladie, Télétravail, Dimanche)
  
- **Stan_Perso** (ID 14) — Personal projects
  - Homelab (Docker, NAS, VPN, Automatisations)
  - Coding (Python, FastAPI, Obsidian plugins, Learning)
  - Obsidian/Doc (Wiki, Synthèses, Dataview, Maintenance)
  - Vélo (Sorties, Entretien, Entraînement, Matériel)

### Activities
- 24+ activities defined in `toggle_pointage_v3.py`
- IDs: 14-37 (Pro: 14-21, Perso: 22-37)

---

## Files in This Repo

| File | Purpose | Status |
|------|---------|--------|
| `docker-compose.yml` | Production setup | ✅ Live |
| `docker-compose.sandbox.yml` | Testing setup | 🆕 Created 2026-06-03 |
| `toggle_pointage_v3.py` | V3 API (multi-project) | 📋 Ready for test |
| `toggle_pointage_stan_prod.py` | Current prod API | ✅ Documented 2026-06-03 |
| `toggle_pointage.py` | Legacy API | 📦 Reference only |
| `docs/` | Installation & config guides | ✅ Complete |

---

## Deployment Plan

### Phase 1: Sandbox Testing (NOW)
- [ ] Wait for sandbox startup (~2 min)
- [ ] Access http://192.168.1.15:8056
- [ ] Create 2 test projects (Stan_Pro, Stan_Perso)
- [ ] Add sample activities (5-10 per project)
- [ ] Deploy `toggle_pointage_v3.py` to sandbox toggle service
- [ ] Test API endpoints (`/toggle/stan?project=X`)
- [ ] Verify activity selection UI

### Phase 2: Production Preparation
- [ ] Create backup of current production data
- [ ] Copy V3 projects/activities config from sandbox
- [ ] Deploy `toggle_pointage_v3.py` to production
- [ ] Update docker-compose.yml if needed
- [ ] Restart production services

### Phase 3: Post-CDD Integration (June 2026)
- [ ] Discover actual CCI projects
- [ ] Create CCI-specific project (Stan_CCI90)
- [ ] Add CCI activities (Prospection, Ateliers, Diagnostics, Formation)
- [ ] Update `toggle_pointage_v3.py` with new project IDs
- [ ] Update XKeys mapping (F13/F14/F15/F16+)

---

## Key Links

- **GitHub**: https://github.com/cbtitalia/kimai_Stan
- **Vault Docs**: Brain_Stan wiki → Informatique/Pointage_Stan/
- **NAS SSH**: `ssh cbtitalia@192.168.1.15`
- **Production**: http://192.168.1.15:8055 (admin@pointage.local)
- **Sandbox**: http://192.168.1.15:8056 (admin@sandbox.local)

---

## Recent Changes

**2026-06-03**:
- ✅ Created `kimai_sandbox` instance (port 8056)
- ✅ Added `docker-compose.sandbox.yml` to repo
- ✅ Documented `toggle_pointage_stan_prod.py` (current prod)
- ✅ Verified `toggle_pointage_v3.py` exists (V3 architecture ready)

**2026-05-26** (CDD Start):
- Conseiller Cyber role begins at CCI90
- Pointage_Stan architecture still at minimal V1

---

## Next Step

1. **Monitor sandbox startup** (watch logs or HTTP access)
2. **Test V3 API** once sandbox is ready
3. **Document CCI projects** for Phase 3
4. **Plan production cutover** (date TBD)

---

*Generated: 2026-06-03 21:30 UTC*
*Location: github.com/cbtitalia/kimai_Stan*
