#!/usr/bin/env python3
import httpx, os, smtplib
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("/scripts/.env")

KIMAI   = os.environ["KIMAI_URL"]
TOKEN   = os.environ["TOKEN_STAN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

JOURS_FR = ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"]

JOURS_FERIES = {
    "2026-01-01", "2026-04-06", "2026-05-01", "2026-05-08",
    "2026-05-14", "2026-05-25", "2026-07-14", "2026-08-15",
    "2026-11-01", "2026-11-11", "2026-12-25",
    "2027-01-01", "2027-04-05", "2027-05-01", "2027-05-08",
    "2027-05-13", "2027-05-24", "2027-07-14", "2027-08-15",
    "2027-11-01", "2027-11-11", "2027-12-25",
}

def get_pointages_jour(jour):
    r = httpx.get(f"{KIMAI}/timesheets", headers=HEADERS,
                  params={"begin": f"{jour}T00:00:00", "end": f"{jour}T23:59:59", "size": 50}, timeout=15)
    return [e for e in r.json() if isinstance(e, dict) and e.get("activity") == 1]

def tableau_jour(pointages):
    if not pointages:
        return "<p>Aucun pointage aujourd'hui.</p>"
    lignes = ""
    total = 0
    for e in pointages:
        debut = e.get("begin", "")[11:16]
        fin = e.get("end", "")[11:16] if e.get("end") else "en cours"
        duree = e.get("duration", 0) or 0
        total += duree
        duree_str = f"{duree//3600}h{(duree%3600)//60:02d}" if duree else ""
        style = "background:#fff3cd;" if not e.get("end") else ""
        lignes += f'<tr style="{style}"><td style="padding:5px;border:1px solid #ddd">{debut}</td><td style="padding:5px;border:1px solid #ddd">{fin}</td><td style="padding:5px;border:1px solid #ddd;text-align:center">{duree_str}</td></tr>'
    total_str = f"{total//3600}h{(total%3600)//60:02d}"
    lignes += f'<tr style="background:#4472C4;color:white;font-weight:bold"><td colspan="2" style="padding:5px">Total journee</td><td style="padding:5px;text-align:center">{total_str}</td></tr>'
    return f'<table style="border-collapse:collapse;width:100%"><thead><tr style="background:#333;color:white"><th style="padding:5px">Debut</th><th style="padding:5px">Fin</th><th style="padding:5px">Duree</th></tr></thead><tbody>{lignes}</tbody></table>'

def tableau_7jours(aujourd_hui):
    lignes = ""
    for i in range(6, -1, -1):
        jour = aujourd_hui - timedelta(days=i)
        jour_str = f"{JOURS_FR[jour.weekday()]} {jour.strftime('%d/%m')}"
        ferie = str(jour) in JOURS_FERIES
        weekend = jour.weekday() >= 5
        if ferie:
            lignes += f'<tr style="background:#f0f0f0;color:#aaa"><td style="padding:5px;border:1px solid #ddd"><b>{jour_str}</b></td><td colspan="3" style="padding:5px;border:1px solid #ddd;text-align:center">Ferie</td></tr>'
            continue
        pts = get_pointages_jour(jour)
        nb = len(pts)
        total = sum(e.get("duration", 0) or 0 for e in pts)
        total_str = f"{total//3600}h{(total%3600)//60:02d}" if total else "—"
        heures = " / ".join([e.get("begin","")[11:16] + "-" + (e.get("end","")[11:16] if e.get("end") else "...") for e in pts])
        if nb == 0 and not weekend:
            bg = "background:#FFD6D6;"
        elif nb % 2 != 0:
            bg = "background:#FFE8CC;"
        elif i == 0:
            bg = "background:#E8F5E9;"
        elif weekend and nb == 0:
            bg = "background:#f0f0f0;"
        else:
            bg = ""
        lignes += f'<tr style="{bg}"><td style="padding:5px;border:1px solid #ddd"><b>{jour_str}</b></td><td style="padding:5px;border:1px solid #ddd;font-size:12px">{heures if heures else ("—" if not weekend else "")}</td><td style="padding:5px;border:1px solid #ddd;text-align:center">{nb}p</td><td style="padding:5px;border:1px solid #ddd;text-align:center;font-weight:bold">{total_str}</td></tr>'
    return f'<table style="border-collapse:collapse;width:100%"><thead><tr style="background:#333;color:white"><th style="padding:5px">Jour</th><th style="padding:5px">Pointages</th><th style="padding:5px">Nb</th><th style="padding:5px">Total</th></tr></thead><tbody>{lignes}</tbody></table>'

def envoyer(sujet, html):
    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = sujet
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = "cbtitalia@gmail.com"
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as s:
        s.starttls()
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        s.send_message(msg)

def main():
    aujourd_hui = date.today()
    weekend = aujourd_hui.weekday() >= 5
    ferie = str(aujourd_hui) in JOURS_FERIES

    r = httpx.get(f"{KIMAI}/timesheets", headers=HEADERS, params={"active": 1}, timeout=15)
    actifs = r.json()
    pts_jour = get_pointages_jour(aujourd_hui)
    nb = len(pts_jour)

    # Weekend ou férié : envoyer uniquement s'il y a des pointages
    if (weekend or ferie) and nb == 0:
        print(f"{'Weekend' if weekend else 'Ferie'} sans pointage — pas d'email.")
        return

    a_actif = len(actifs) > 0
    tab_jour = tableau_jour(pts_jour)
    tab_7j = tableau_7jours(aujourd_hui)
    date_str = aujourd_hui.strftime("%d/%m/%Y")
    heure = datetime.now().strftime("%d/%m/%Y %H:%M")

    if a_actif:
        debut = actifs[0].get("begin", "")[11:16]
        sujet = f"Pointage en cours — {date_str}"
        alerte = f"<p style='background:#dc3545;color:white;padding:10px;border-radius:4px'>Pointage encore actif depuis <b>{debut}</b> — passe le badge.</p>"
        statut = "En cours"
    elif nb % 2 != 0:
        sujet = f"Pointage impair ({nb}) — {date_str}"
        alerte = f"<p style='background:#fd7e14;color:white;padding:10px;border-radius:4px'>{nb} pointage(s) — nombre impair.</p>"
        statut = "Impair"
    else:
        sujet = f"Pointage OK ({nb}) — {date_str}"
        alerte = f"<p style='background:#28a745;color:white;padding:10px;border-radius:4px'>{nb} pointage(s) — journee correcte.</p>"
        statut = "OK"

    html = f"""<html><body style='font-family:Arial,sans-serif;max-width:650px;margin:auto'>
    <h2>Pointage Stan — {date_str} — {statut}</h2>
    {alerte}
    <h3>Detail du jour :</h3>{tab_jour}
    <h3 style='margin-top:20px'>7 derniers jours :</h3>{tab_7j}
    <p style='color:#999;font-size:12px;margin-top:16px'>Envoye le {heure}</p>
    </body></html>"""

    print(f"Statut : {statut} ({nb} entrees) — email envoye.")
    envoyer(sujet, html)

if __name__ == "__main__":
    main()
