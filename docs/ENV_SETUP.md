# Setup Guide — .env Configuration

## Before Starting

This guide explains how to configure `.env` for Kimai deployment on Synology NAS.

⚠️ **SECURITY**: `.env` contains secrets and is **NEVER** committed to git. Always keep it local.

---

## Step 1: Copy Template

```bash
cd /volume1/docker/kimai
cp .env.example .env
chmod 600 .env
```

---

## Step 2: Generate Secure Secrets

### Database Passwords
Create strong random passwords (32 chars):

**Linux/Mac:**
```bash
openssl rand -hex 32
```

**Windows PowerShell:**
```powershell
[Convert]::ToHexString((1..32 | % { Get-Random -Max 256 }))
```

Example output: `a7f3e9c2b1d4f6e8a9c0b1d2e3f4a5b6`

### Kimai Secret
Same process — generate 64-char random string:
```bash
openssl rand -hex 32
```

### API Token
Generate a secure token for Toggle API (Bearer authentication):
```bash
openssl rand -hex 32
```

---

## Step 3: Fill .env Values

Edit `/volume1/docker/kimai/.env` and set:

```ini
# Database (use generated passwords from Step 2)
DATABASE_PASSWORD=<generated-32-char-hex>
DATABASE_ROOT_PASSWORD=<generated-32-char-hex>

# Kimai Secret
KIMAI_SECRET=<generated-32-char-hex>

# SMTP (for email notifications, exports)
SMTP_FROM=your-email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your_app_password_here  # For Gmail: Use App Password (not regular password)

# API Token (for Toggle service)
TOKEN_STAN=<generated-32-char-hex>

# Kimai URL (do not change for local Docker setup)
KIMAI_URL=http://kimai:8001/api
```

### Gmail App Password Setup

If using Gmail SMTP:
1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer" (or other device)
4. Google generates a 16-char app password (spaces included)
5. Copy this password to `SMTP_PASSWORD` in `.env`

---

## Step 4: Verify Configuration

Test the `.env` file is valid:

```bash
cd /volume1/docker/kimai
docker-compose config
```

If no errors → proceed to Step 5.

---

## Step 5: Start Services

```bash
docker-compose up -d
sleep 30
docker-compose ps
```

Expected output:
```
NAME                    STATUS
kimai_mysql             Up (healthy)
kimai_app               Up
kimai_toggle            Up
```

---

## Step 6: Access & Verify

### Kimai Web UI
- URL: http://192.168.1.15:8055
- Default user: `admin@pointage.local`
- Default password: `AdminPassAChanger!` (change immediately!)

### Toggle API Health
```bash
curl -s http://192.168.1.15:8059/health
```

Expected: `{"status":"ok"}`

---

## Troubleshooting

### Database Connection Error
**Symptom**: `ERROR: Connection refused at mysql:3306`

**Fix**:
1. Check MySQL is healthy: `docker-compose ps`
2. Wait 30-60s for MySQL startup
3. Restart: `docker-compose restart kimai`

### SMTP Auth Failed
**Symptom**: Email notifications not sending

**Fix**:
1. Verify Gmail App Password (not regular password)
2. Enable "Less secure app access" if using personal Gmail
3. Test manually:
   ```bash
   curl -s smtp://your-email@gmail.com:app_password@smtp.gmail.com:587 -v
   ```

### API Token Issues
**Symptom**: Toggle API returns 401 Unauthorized

**Fix**:
1. Verify TOKEN_STAN in `.env`
2. Restart toggle service: `docker-compose restart toggle`
3. Check token format: 32-char hex string

---

## Backup Your .env

After successful configuration, back up your `.env`:

```bash
cp /volume1/docker/kimai/.env /volume1/docker/kimai/backups/.env.backup
chmod 600 /volume1/docker/kimai/backups/.env.backup
```

**NEVER commit this backup to git.**

---

## Security Checklist

- [ ] `.env` file has permissions `600` (readable by owner only)
- [ ] No `.env` committed to git (check `.gitignore`)
- [ ] Database passwords are 32+ char random strings
- [ ] SMTP password is Gmail App Password (not regular password)
- [ ] API token is 32+ char random string
- [ ] All values filled (no placeholders remaining)

---

## Next Steps

Once `.env` is configured and services are running:
1. Create Kimai users and projects (see `pointage-stan-kimai-configuration.md`)
2. Configure Toggle API activities (see `toggle_pointage_v3.py`)
3. Set up backups and monitoring (see main README)

---

*Last updated: 2026-06-03*
