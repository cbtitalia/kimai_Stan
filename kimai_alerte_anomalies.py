#!/usr/bin/env python3
import httpx, os, smtplib
from datetime import date, timedelta, datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("/scripts/.env")

KIMAI   = os.environ["KIMAI_URL"]
TOKEN   = os.environ["TOKEN_STAN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

EMPLOYES = [{"nom": "Stan", "id": 1}]

JOURS_FERIES = {
    "2026-01-01", "2026-04-06", "2026-05-01", "2026-05-08",
    "2026-05-14", "2026-05-25", "2026-07-14", "2026-08-15",
    "2026-11-01", "2026-11-11", "2026-12-25",
    "2027-01-01", "2027-04-05", "2027-05-01", "2027-05-08",
    "2027-05-13", "2027-05-24", "2027-07-14", "2027-08-15",
    "2027-11-01", "2027-11-11", "2027-12-25",
}

def get_pointages(user_id, jour):
    try:
        r = httpx.get(f"{KIMAI}/timesheets", headers=HEADERS,
                      params={"user": user_id, "begin": f"{jour}T00:00:00",
                              "end": f"{jour}T23:59:59", "size": 50}, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erreur API : {e}")
        return []

def analyser(employe, jour):
    entrees = get_pointages(employe["id"], jour)
    pointages = [e for e in entrees if "congé" not in e.get("activity", {}).get("name", "").lower()
                 and "astreinte" not in e.get("activity", {}).get("name", "").lower()]
    if not pointages:
        absences = [e for e in entrees if e not in pointages]
        if absences:
            return {"nom": employe["nom"], "statut": "absent_justifie", "detail": absences[0].get("activity", {}).get("name", "")}
        return {"nom": employe["nom"], "statut": "absent", "detail": "Aucun pointage"}
    if len(pointages) == 1 and pointages[0].get("duration", 0) > 21600:
        d = pointages[0]
        return {"nom": employe["nom"], "statut": "sans_midi",
                "detail": f"{d.get('begin','')[:16].replace('T',' ')} → {d.get('end','')[:16].replace('T',' ')}"}
    total = sum(e.get("duration", 0) for e in pointages)
    return {"nom": employe["nom"], "statut": "ok",
            "detail": f"{len(pointages)} entrée(s) — {total//3600}h{(total%3600)//60:02d}"}

def envoyer(html, anomalies, jour):
    sujet = f"⚠️ Pointage anomalie {jour.strftime('%d/%m/%Y')}" if anomalies \
            else f"✅ Pointage OK {jour.strftime('%d/%m/%Y')}"
    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = sujet
    msg["From"]    = os.environ["SMTP_FROM"]
    msg["To"]      = "cbtitalia@gmail.com"
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as s:
        s.starttls()
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        s.send_message(msg)

def generer_html(resultats, jour):
    lignes = ""
    for r in resultats:
        icone = {"absent": "❌", "sans_midi": "⚠️", "absent_justifie": "📅", "ok": "✅"}.get(r["statut"], "❓")
        couleur = {"absent": "#dc3545", "sans_midi": "#fd7e14", "absent_justifie": "#6c757d", "ok": "#28a745"}.get(r["statut"], "#333")
        lignes += f'<tr><td style="padding:8px;font-size:20px">{icone}</td><td style="padding:8px;font-weight:bold;color:{couleur}">{r["nom"]}</td><td style="padding:8px">{r["detail"]}</td></tr>'
    titre = "⚠️ Anomalie détectée" if any(r["statut"] in ("absent","sans_midi") for r in resultats) else "✅ Tout est OK"
    return f"""<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
    <h2>Pointage_Stan — {titre} — {jour.strftime('%d/%m/%Y')}</h2>
    <table style="width:100%;border-collapse:collapse;background:#f9f9f9">
    <thead><tr style="background:#4472C4;color:white"><th style="padding:8px">Statut</th><th style="padding:8px">Employé</th><th style="padding:8px">Détail</th></tr></thead>
    <tbody>{lignes}</tbody></table>
    <p style="color:#999;font-size:12px">Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </body></html>"""

def main():
    hier = date.today() - timedelta(days=1)
    if hier.weekday() >= 5:
        print(f"{hier} est un weekend — pas de vérification.")
        return
    if str(hier) in JOURS_FERIES:
        print(f"{hier} est un jour férié — pas de vérification.")
        return
    print(f"Vérification des pointages du {hier}...")
    resultats = [analyser(e, hier) for e in EMPLOYES]
    for r in resultats:
        print(f"  {r['nom']:10} → {r['statut']:15} {r['detail']}")
    anomalies = any(r["statut"] in ("absent", "sans_midi") for r in resultats)
    if anomalies:
        envoyer(generer_html(resultats, hier), anomalies, hier)
        print("Email d'alerte envoyé.")
    else:
        print("Aucune anomalie.")

if __name__ == "__main__":
    main()
