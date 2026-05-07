#!/usr/bin/env python3
"""
Met à jour les couleurs des 24 activités Kimai via l'API
"""

import requests
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

KIMAI_API = "http://192.168.1.15:8055/api"
TOKEN = "3335823591a9859b9fba28c7e"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Map: activity_id → couleur hex (format Kimai)
ACTIVITY_COLORS = {
    # Presence (vert pastel)
    14: "C8E6C9",
    15: "A5D6A7",
    16: "81C784",
    17: "66BB6A",
    # Absences (rose/rouge pastel)
    18: "EF9A9A",
    19: "E57373",
    20: "F48FB1",
    21: "EC407A",
    # Homelab (bleu pastel)
    22: "B3E5FC",
    23: "81D4FA",
    24: "4FC3F7",
    25: "29B6F6",
    # Coding (orange pastel)
    26: "FFCC80",
    27: "FFB74D",
    28: "FFA726",
    29: "FF7043",
    # Obsidian (jaune pastel)
    30: "FFF9C4",
    31: "FFF59D",
    32: "FFF176",
    33: "FFEE58",
    # Velo (turquoise pastel)
    34: "B2DFDB",
    35: "80CBC4",
    36: "4DB6AC",
    37: "26A69A"
}

def get_activity(activity_id):
    """Récupère les données d'une activité"""
    try:
        resp = requests.get(
            f"{KIMAI_API}/activities/{activity_id}",
            headers=HEADERS
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

def update_activity_color(activity_id, color_hex):
    """Met à jour la couleur d'une activité"""
    try:
        # Récupérer l'activité existante
        activity = get_activity(activity_id)
        if not activity:
            return False, f"❌ ID {activity_id}: Activité non trouvée"

        # Mettre à jour avec la couleur
        project = activity.get("project")
        if isinstance(project, dict):
            project_id = project.get("id")
        else:
            project_id = project

        payload = {
            "name": activity.get("name", ""),
            "project": project_id,
            "color": color_hex,
            "visible": activity.get("visible", True)
        }

        resp = requests.patch(
            f"{KIMAI_API}/activities/{activity_id}",
            headers=HEADERS,
            json=payload
        )

        if resp.status_code in [200, 201]:
            return True, f"✅ ID {activity_id}: {color_hex}"
        else:
            return False, f"❌ ID {activity_id}: {resp.status_code}"

    except Exception as e:
        return False, f"❌ ID {activity_id}: {str(e)}"

def main():
    print("🎨 Mise à jour des couleurs des 24 activités...\n")

    success = 0
    fail = 0

    for activity_id, color in sorted(ACTIVITY_COLORS.items()):
        ok, msg = update_activity_color(activity_id, color)
        print(msg)

        if ok:
            success += 1
        else:
            fail += 1

    print("\n" + "=" * 60)
    print(f"✅ Réussis: {success}")
    print(f"❌ Échoués: {fail}")
    print(f"📊 Total: {success + fail}")
    print("=" * 60)
    print("\n💡 Recharge Kimai pour voir les couleurs!")

if __name__ == "__main__":
    main()
