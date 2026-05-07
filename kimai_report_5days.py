#!/usr/bin/env python3
"""
Rapport timesheets sur 5 jours avec couleurs
"""

import requests
import json
from datetime import datetime, date, timedelta
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

KIMAI_API = "http://192.168.1.15:8055/api"
TOKEN = "3335823591a9859b9fba28c7e"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

ACTIVITIES_MAP = {
    14: ("Presence", "Bureau", "#1fa446"),
    15: ("Presence", "Reunions", "#22c55e"),
    16: ("Presence", "Support", "#16a34a"),
    17: ("Presence", "Formation", "#15803d"),
    18: ("Absences", "Conges", "#dc2626"),
    19: ("Absences", "Maladie", "#b91c1c"),
    20: ("Absences", "Teletravail", "#e11d48"),
    21: ("Absences", "Dimanche", "#c41e3a"),
    22: ("Homelab", "Docker", "#0369a1"),
    23: ("Homelab", "NAS", "#0284c7"),
    24: ("Homelab", "VPN", "#06b6d4"),
    25: ("Homelab", "Automatisations", "#00d9ff"),
    26: ("Coding", "Python", "#dc2626"),
    27: ("Coding", "FastAPI", "#f97316"),
    28: ("Coding", "Obsidian plugins", "#ea580c"),
    29: ("Coding", "Apprentissage", "#c2410c"),
    30: ("Obsidian", "Wiki notes", "#d97706"),
    31: ("Obsidian", "Syntheses", "#f59e0b"),
    32: ("Obsidian", "Dataview", "#fbbf24"),
    33: ("Obsidian", "Maintenance", "#fcd34d"),
    34: ("Velo", "Sorties", "#059669"),
    35: ("Velo", "Entretien", "#10b981"),
    36: ("Velo", "Entraînement", "#34d399"),
    37: ("Velo", "Materiel", "#6ee7b7"),
}

def get_timesheets_range(start_date, end_date):
    """Récupère timesheets sur une plage"""
    resp = requests.get(f"{KIMAI_API}/timesheets?limit=500", headers=HEADERS)
    if resp.status_code != 200:
        return []

    sheets = resp.json()
    filtered = []

    for ts in sheets:
        begin = ts.get("begin", "")
        if begin:
            ts_date = begin.split('T')[0]
            if start_date <= ts_date <= end_date:
                filtered.append(ts)

    return filtered

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(hours)}h{int(minutes):02d}" if hours > 0 else f"{int(minutes)}min"

def main():
    today = date.today()
    start = today + timedelta(days=-5)
    end = today + timedelta(days=1)

    print(f"📊 Rapport timesheets: {start} à {end}\n")

    sheets = get_timesheets_range(start.isoformat(), end.isoformat())
    print(f"📋 Total: {len(sheets)} timesheets\n")

    # Grouper par jour
    by_day = {}
    by_activity = {}

    for ts in sheets:
        begin = ts.get("begin", "")
        if not begin:
            continue

        day = begin.split('T')[0]
        act_id = ts.get("activity", {})
        act_id = act_id.get("id") if isinstance(act_id, dict) else act_id

        duration = ts.get("duration", 0)

        if day not in by_day:
            by_day[day] = []

        if act_id not in ACTIVITIES_MAP:
            continue

        cat, name, color = ACTIVITIES_MAP[act_id]
        by_day[day].append((act_id, name, cat, duration, color))

        if cat not in by_activity:
            by_activity[cat] = 0
        by_activity[cat] += duration

    # Afficher par jour
    total_all = 0
    for day in sorted(by_day.keys()):
        day_obj = datetime.strptime(day, "%Y-%m-%d").date()
        day_name = day_obj.strftime("%a %d/%m")

        print(f"📅 {day_name}")
        print("-" * 60)

        day_total = 0
        for act_id, name, cat, duration, color in sorted(by_day[day], key=lambda x: x[2]):
            day_total += duration
            dur_str = format_duration(duration)
            # Afficher avec couleur ANSI (fallback sur symbole coloré)
            print(f"  ● {cat:15} → {name:20} : {dur_str:>8}")

        print(f"  {'─' * 56}")
        print(f"  📊 Jour: {format_duration(day_total)}\n")
        total_all += day_total

    # Résumé par catégorie
    print("=" * 60)
    print("📈 RÉSUMÉ PAR CATÉGORIE")
    print("=" * 60)

    for cat in ["Presence", "Absences", "Homelab", "Coding", "Obsidian", "Velo"]:
        if cat in by_activity:
            dur = format_duration(by_activity[cat])
            pct = (by_activity[cat] / total_all * 100) if total_all > 0 else 0
            print(f"{cat:15} : {dur:>8} ({pct:5.1f}%)")

    print("=" * 60)
    print(f"{'TOTAL':15} : {format_duration(total_all):>8} (100.0%)")
    print("=" * 60)

if __name__ == "__main__":
    main()
