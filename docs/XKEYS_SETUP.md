# XKeys 24 Setup Guide

## Overview

XKeys 24 is a programmable keyboard with 24 touch-sensitive keys. This guide configures it to control Kimai timesheet via AutoHotkey script.

**Architecture**:
- XKeys 24 keyboard → F13-F20 function keys → AutoHotkey script → Kimai Toggle API

---

## Hardware Setup

### 1. Connect XKeys 24

1. Plug USB cable into Windows PC
2. Install drivers from XKeys (if needed): https://www.xkeys.com/xkeys/support/
3. Verify in Device Manager: `XKeys 24 USB Keyboard`

### 2. Configure XKeys Touches

XKeys comes with **MacroWorks** software (GUI configurator).

#### Option A: MacroWorks GUI

1. Open **MacroWorks** application
2. Select "XKeys 24" device
3. For each touch (1-8):
   - **Touch 1** → F13 (Stan Pro)
   - **Touch 2** → F14 (Stan Perso)
   - **Touch 3** → F15 (Divers)
   - **Touch 4** → F16 (CCI90, future)
   - **Touch 5** → F17 (ISO27001, future)
   - **Touch 6** → F18 (CapCyber, future)
   - **Touch 7-8** → F19, F20 (reserved)
4. Save configuration to device

#### Option B: Basic Programming

1. Hold down the touch you want to program for 3 seconds
2. Type the key combination (e.g., `F13`)
3. Release the touch
4. LED blinks to confirm programming

### 3. Test Keys

In any text editor, press each XKeys touch and verify F13-F20 are sent:

```
F13 → displays as F13
F14 → displays as F14
...
```

---

## AutoHotkey Script Installation

### 1. Install AutoHotkey

Download **AutoHotkey v2.0+**: https://www.autohotkey.com/

1. Run installer
2. Select "v2" (current version)
3. Install to default location

### 2. Deploy Script

1. Download `xkeys_pointage_stan.ahk` from this repo
2. Save to: `C:\Users\<YourUsername>\xkeys_pointage_stan.ahk`
3. Edit configuration (see below)

### 3. Configure Script

Edit the script and update:

```autohotkey
; Configuration
API_URL := "http://192.168.1.15:8059/toggle/stan"
TOKEN := "admin_token_2026"  ; From .env TOKEN_STAN
```

Ensure:
- `API_URL` points to your Kimai NAS (192.168.1.15:8059)
- `TOKEN` matches `TOKEN_STAN` in `.env`

### 4. Run Script

**Option A: Double-click**
```
Double-click: xkeys_pointage_stan.ahk
```

**Option B: Command line**
```bash
AutoHotkey.exe C:\Users\<YourUsername>\xkeys_pointage_stan.ahk
```

**Option C: Startup (Windows Task Scheduler)**

Create a scheduled task to run script on login:
1. Win+R → `taskschd.msc`
2. Create Basic Task
3. Name: "Pointage Stan AutoHotkey"
4. Trigger: "At startup"
5. Action: "Start a program" → `AutoHotkey.exe`
6. Arguments: `C:\Users\<YourUsername>\xkeys_pointage_stan.ahk`
7. Enable "Run whether user is logged in or not"

---

## Keyboard Mapping

| XKeys Touch | Function Key | Project | Action |
|-------------|-------------|---------|--------|
| 1 | F13 | Stan_Pro | Toggle timesheet |
| 2 | F14 | Stan_Perso | Toggle timesheet |
| 3 | F15 | Divers | Toggle timesheet |
| 4 | F16 | Reserved | Future project |
| 5 | F17 | Reserved | Future project |
| 6 | F18 | Reserved | Future project |
| 7 | F19 | Reserved | Future project |
| 8 | F20 | Reserved | Future project |
| ESC | Esc | Current | Stop active timesheet |

---

## Testing

### 1. Start Script

```bash
AutoHotkey.exe xkeys_pointage_stan.ahk
```

Expected output:
- ✅ Toast notification: "Pointage Stan Ready (XKeys 24)"
- Tray icon appears (bottom-right corner)

### 2. Test API Connectivity

```bash
# Test from PowerShell
curl -H "Authorization: Bearer admin_token_2026" `
  "http://192.168.1.15:8059/toggle/stan?project=13"
```

Expected response:
```json
{"status": "started|stopped", "project": 13, "duration_min": 0}
```

### 3. Test XKeys Touch

1. Press **Touch 1** (Stan Pro)
2. Expected: Green toast notification "▶ Pointage démarré - Projet: Stan Pro"
3. Press **Touch 1** again
4. Expected: Gray toast notification "⏸ Pointage arrêté - Durée: X min"

### 4. Test Multiple Projects

1. Press **Touch 1** (Stan Pro) → starts Pro timesheet
2. Press **Touch 2** (Stan Perso) → stops Pro, starts Perso
3. Verify in Kimai UI: two separate timesheets created

---

## Troubleshooting

### Script won't start
**Error**: "AutoHotkey: File not found"

**Fix**:
1. Verify AutoHotkey is installed: `AutoHotkey.exe --version`
2. Verify script path is correct
3. Ensure no special characters in file path

### XKeys touches don't send F13-F20
**Error**: Touches trigger other actions

**Fix**:
1. Re-program touches in MacroWorks (see Hardware Setup § 2)
2. Verify no other software (like gaming software) is intercepting F13-F20
3. Test in Notepad: touches should type `F13`, `F14`, etc.

### API Connection refused
**Error**: Toast shows "❌ API Error: Connection refused"

**Fix**:
1. Verify Kimai is running: `http://192.168.1.15:8055` in browser
2. Verify Toggle API is running: `http://192.168.1.15:8059/health`
3. Verify firewall allows 8055, 8059 ports
4. Verify IP address in script matches your NAS IP

### Toast notifications don't show
**Error**: AutoHotkey runs but no visual feedback

**Fix**:
1. Current implementation uses ToolTip (native Windows)
2. For better UX, install Toast library:
   - Download: `Lib/Toast.ahk` from https://github.com/AHK-just-me/Toast
   - Place in same directory as script
   - Uncomment Toast lines in script

### Token authentication fails
**Error**: Toast shows "❌ API Error: 401 Unauthorized"

**Fix**:
1. Verify `TOKEN` in script matches `TOKEN_STAN` in `.env`
2. Restart Toggle API: `docker-compose restart toggle`
3. Check API logs: `docker-compose logs toggle`

---

## Production Deployment

### Phase 1: Testing (sandbox)
- [ ] XKeys hardware configured (F13-F20)
- [ ] AutoHotkey script running locally
- [ ] Script connects to sandbox API (port 8056)
- [ ] Touches create timesheets in Kimai sandbox
- [ ] Multiple projects toggle correctly

### Phase 2: Production
- [ ] Backup current Kimai data
- [ ] Deploy V3 API to production (toggle_pointage_v3.py)
- [ ] Update script TOKEN to production value
- [ ] Update API_URL to production NAS
- [ ] Test touches with production Kimai
- [ ] Monitor logs: `docker-compose logs -f toggle`

### Phase 3: Post-CDD (June 2026)
- [ ] Discover actual CCI projects
- [ ] Update PROJECT_MAP with new project IDs
- [ ] Reprogram XKeys touches (F16-F20) with CCI projects
- [ ] Update script and test new projects

---

## References

- **XKeys Support**: https://www.xkeys.com/xkeys/support/
- **AutoHotkey Docs**: https://www.autohotkey.com/docs/v2/
- **Kimai API**: http://192.168.1.15:8055/api/doc
- **Toggle API Source**: `toggle_pointage_v3.py` in this repo

---

## Security Notes

- ⚠️ **TOKEN**: Keep `TOKEN_STAN` secret (credentials)
- ⚠️ **Script Path**: Don't commit scripts with tokens to git
- ⚠️ **API URL**: Ensure you're calling correct NAS (192.168.1.15, not external)

Store sensitive data in `.env` only, never in script.

---

*Last updated: 2026-06-03*
