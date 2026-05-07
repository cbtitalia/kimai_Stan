#!/usr/bin/env python3
"""
Génère des timesheets de test réalistes sur 5 jours
Durées: 20min à 2h
Horaires: 8h-12h et 14h-18h
Activités variées
"""

import requests
import json
from datetime import datetime, date, timedelta
import random
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

KIMAI_API = "http://192.168.1.15:8055/api"
TOKEN = "3335823591a9859b9fba28c7e"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Projets et activités réalistes
SCHEDULES = {
    # Jour 1 (5 jours avant)
    -5: [
        (14, "08:00", 90),    # Presence - Bureau 1h30
        (26, "09:30", 120),   # Coding - Python 2h
        (30, "14:00", 60),    # Obsidian - Wiki 1h
        (34, "15:15", 45),    # Velo - Sorties 45min
    ],
    # Jour 2 (4 jours avant)
    -4: [
        (15, "08:15", 105),   # Presence - Reunions 1h45
        (22, "09:45", 120),   # Homelab - Docker 2h
        (31, "14:30", 50),    # Obsidian - Syntheses 50min
    ],
    # Jour 3 (3 jours avant)
    -3: [
        (16, "08:00", 75),    # Presence - Support 1h15
        (27, "10:00", 140),   # Coding - FastAPI 2h20
        (35, "14:00", 60),    # Velo - Entretien 1h
        (32, "15:30", 55),    # Obsidian - Dataview 55min
    ],
    # Jour 4 (2 jours avant)
    -2: [
        (17, "08:30", 110),   # Presence - Formation 1h50
        (23, "10:00", 100),   # Homelab - NAS 1h40
        (28, "14:00", 80),    # Coding - Obsidian plugins 1h20
        (36, "15:30", 50),    # Velo - Entraînement 50min
    ],
    # Jour 5 (1 jour avant)
    -1: [
        (14, "08:00", 120),   # Presence - Bureau 2h
        (24, "10:30", 90),    # Homelab - VPN 1h30
        (33, "14:00", 65),    # Obsidian - Maintenance 1h05
        (37, "15:30", 40),    # Velo - Materiel 40min
        (29, "17:00", 25),    # Coding - Apprentissage 25min
    ],
}

def create_timesheet(project_id, activity_id, start_time, duration_minutes):
    """Crée un timesheet"""
    # Calculer les timestamps
    hour, minute = map(int, start_time.split(':'))

    today = date.today()
    day_offset = 0

    # Chercher le jour dans la clé
    for offset, activities in SCHEDULES.items():
        for act_id, time, dur in activities:
            if act_id == activity_id and start_time == time and dur == duration_minutes:
                day_offset = offset
                break

    target_date = today + timedelta(days=day_offset)

    begin = datetime.combine(target_date, datetime.min.time()).replace(hour=hour, minute=minute)
    end = begin + timedelta(minutes=duration_minutes)

    payload = {
        "project": project_id,
        "activity": activity_id,
        "begin": begin.isoformat(),
        "end": end.isoformat()
    }

    try:
        resp = requests.post(f"{KIMAI_API}/timesheets", headers=HEADERS, json=payload)
        if resp.status_code in [200, 201]:
            return True, f"✅ {activity_id} ({duration_minutes}min à {start_time})"
        else:
            return False, f"❌ {activity_id}: {resp.status_code} - {resp.text[:100]}"
    except Exception as e:
        return False, f"❌ {activity_id}: {str(e)}"

def main():
    print("🔄 Création timesheets de test (5 jours)...\n")

    success_count = 0
    fail_count = 0

    for day_offset, activities in sorted(SCHEDULES.items()):
        target_date = date.today() + timedelta(days=day_offset)
        print(f"📅 {target_date.strftime('%A %d/%m/%Y')}")
        print("-" * 50)

        daily_total = 0

        for activity_id, start_time, duration in activities:
            # Déterminer le projet (14-21 = Pro, 22-37 = Perso)
            project_id = 13 if activity_id <= 21 else 14

            success, msg = create_timesheet(project_id, activity_id, start_time, duration)
            if success:
                success_count += 1
                daily_total += duration
            else:
                fail_count += 1

            print(f"  {msg}")

        hours = daily_total // 60
        mins = daily_total % 60
        print(f"  📊 Total jour: {hours}h{mins:02d}\n")

    print("=" * 50)
    print(f"✅ Réussis: {success_count}")
    print(f"❌ Échoués: {fail_count}")
    print(f"📊 Total timesheets: {success_count + fail_count}")

if __name__ == "__main__":
    main()
