#!/usr/bin/env python3
"""
Synchronise les timesheets Kimai avec le dashboard Obsidian
Usage: python3 kimai_sync_dashboard.py
"""

import requests
import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

KIMAI_API = "http://192.168.1.15:8055/api"
TOKEN = "3335823591a9859b9fba28c7e"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Map: activity_id → (category, activity_name, color_hex, emoji)
ACTIVITIES_MAP = {
    14: ("Presence", "Presence - Bureau", "#C8E6C9", "🟢"),
    15: ("Presence", "Presence - Reunions", "#A5D6A7", "🟢"),
    16: ("Presence", "Presence - Support", "#81C784", "🟢"),
    17: ("Presence", "Presence - Formation", "#66BB6A", "🟢"),
    18: ("Absences", "Absences - Conges", "#EF9A9A", "🔴"),
    19: ("Absences", "Absences - Maladie", "#E57373", "🔴"),
    20: ("Absences", "Absences - Teletravail", "#F48FB1", "🔴"),
    21: ("Absences", "Absences - Dimanche", "#EC407A", "🔴"),
    22: ("Homelab", "Homelab - Infra Docker", "#B3E5FC", "🔵"),
    23: ("Homelab", "Homelab - Serveurs NAS", "#81D4FA", "🔵"),
    24: ("Homelab", "Homelab - Reseau VPN", "#4FC3F7", "🔵"),
    25: ("Homelab", "Homelab - Automatisations", "#29B6F6", "🔵"),
    26: ("Coding", "Coding Perso - Python", "#FFCC80", "🔶"),
    27: ("Coding", "Coding Perso - FastAPI", "#FFB74D", "🔶"),
    28: ("Coding", "Coding Perso - Obsidian plugins", "#FFA726", "🔶"),
    29: ("Coding", "Coding Perso - Apprentissage", "#FF7043", "🔶"),
    30: ("Obsidian", "Obsidian/Doc - Wiki notes", "#FFF9C4", "🟡"),
    31: ("Obsidian", "Obsidian/Doc - Syntheses archivage", "#FFF59D", "🟡"),
    32: ("Obsidian", "Obsidian/Doc - Dataview dashboards", "#FFF176", "🟡"),
    33: ("Obsidian", "Obsidian/Doc - Maintenance structure", "#FFEE58", "🟡"),
    34: ("Velo", "Velo - Sorties parcours", "#B2DFDB", "🚴"),
    35: ("Velo", "Velo - Entretien maintenance", "#80CBC4", "🚴"),
    36: ("Velo", "Velo - Entrainement physique", "#4DB6AC", "🚴"),
    37: ("Velo", "Velo - Materiel achat", "#26A69A", "🚴"),
}

CATEGORY_ORDER = ["Presence", "Absences", "Homelab", "Coding", "Obsidian", "Velo"]

def get_timesheets_today():
    """Récupère les timesheets des 7 derniers jours"""
    today = date.today()
    start_date = today - timedelta(days=7)
    start_iso = start_date.isoformat()
    end_iso = today.isoformat()

    # Récupérer tous les timesheets et filtrer par date
    resp = requests.get(f"{KIMAI_API}/timesheets?limit=500", headers=HEADERS)

    if resp.status_code != 200:
        print(f"❌ Erreur API Kimai: {resp.status_code}")
        return []

    timesheets = resp.json()

    # Filtrer par date (7 derniers jours)
    sheets = []
    for ts in timesheets:
        begin = ts.get("begin", "")
        if begin:
            ts_date = begin.split('T')[0]
            if start_iso <= ts_date <= end_iso:
                sheets.append(ts)

    return sheets

def aggregate_by_activity(timesheets):
    """Agrège les timesheets par activité"""
    agg = {}

    for ts in timesheets:
        activity = ts.get("activity")
        activity_id = activity.get("id") if isinstance(activity, dict) else activity

        if activity_id not in ACTIVITIES_MAP:
            continue

        duration = ts.get("duration", 0)
        category, activity_name, color, emoji = ACTIVITIES_MAP[activity_id]

        key = (category, activity_id, activity_name, color, emoji)
        agg[key] = agg.get(key, 0) + duration

    return agg

def format_duration(seconds):
    """Convertit secondes en HH:MM"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(hours)}h{int(minutes):02d}" if hours > 0 else f"{int(minutes)}min"

def generate_html_dashboard(data):
    """Génère le HTML du dashboard avec couleurs"""
    html = '<div style="font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto">\n'
    html += f'<p><small>🔄 Mise à jour: {data["timestamp"].split("T")[1][:5]}</small></p>\n'

    # Résumé par catégorie
    html += '<h3>📊 Résumé du jour</h3>\n'
    html += '<table style="width:100%; border-collapse: collapse;">\n'
    html += '<tr style="border-bottom: 2px solid #ddd;"><th style="text-align:left; padding:8px;">Catégorie</th><th style="text-align:right; padding:8px;">Heures</th></tr>\n'

    total = data["total_seconds"]
    for cat in ["Presence", "Absences", "Homelab", "Coding", "Obsidian", "Velo"]:
        if cat not in data["by_category"]:
            continue
        cat_data = data["by_category"][cat]
        pct = (cat_data["total_seconds"] / total * 100) if total > 0 else 0
        html += f'<tr style="border-bottom: 1px solid #eee;"><td style="padding:8px;">{cat}</td><td style="text-align:right; padding:8px;"><strong>{cat_data["total_formatted"]}</strong> ({pct:.0f}%)</td></tr>\n'

    html += f'<tr style="border-top: 2px solid #333; font-weight:bold;"><td style="padding:8px;">TOTAL</td><td style="text-align:right; padding:8px;">{data["total_formatted"]}</td></tr>\n'
    html += '</table>\n'

    # Détails par activité
    html += '<h3>📈 Détail par activité</h3>\n'

    for cat in ["Presence", "Absences", "Homelab", "Coding", "Obsidian", "Velo"]:
        if cat not in data["by_category"]:
            continue

        cat_data = data["by_category"][cat]
        html += f'<h4>{cat}</h4>\n<ul style="list-style: none; padding-left: 0;">\n'

        for act in cat_data["activities"]:
            color = act.get("color", "#333")
            html += f'<li style="padding: 4px 0; margin-left: 20px; position: relative;"><span style="position: absolute; left: -20px; color: {color}; font-size: 1.2em;">●</span><strong>{act["name"]}</strong> : <code style="background:#f0f0f0; padding:2px 6px; border-radius:3px;">{act["duration"]}</code></li>\n'

        html += '</ul>\n'

    html += '</div>\n'
    return html

def generate_markdown(agg):
    """Génère le markdown pour le dashboard"""

    if not agg:
        return "Aucun timesheet aujourd'hui", "0h00", {}

    total_secs = sum(agg.values())

    # Grouper par catégorie
    by_cat = {}
    for (cat, act_id, act_name, color, emoji), secs in agg.items():
        if cat not in by_cat:
            by_cat[cat] = {"emoji": emoji, "activities": []}
        by_cat[cat]["activities"].append((act_name.split(" - ")[1], secs, color, act_id))

    # Générer markdown
    md = f"**Mise à jour** : {datetime.now().strftime('%H:%M:%S')}\n\n"

    for category in CATEGORY_ORDER:
        if category not in by_cat:
            continue

        cat_data = by_cat[category]
        emoji = cat_data["emoji"]

        md += f"## {emoji} {category}\n\n"

        for act_name, secs, color, act_id in cat_data["activities"]:
            duration = format_duration(secs)
            md += f"- **{act_name}** : `{duration}`\n"

        md += "\n"

    # Résumé par catégorie
    md += "---\n\n## 📊 Résumé\n\n"
    md += "| Catégorie | Heures |\n"
    md += "|-----------|--------|\n"

    for category in CATEGORY_ORDER:
        if category not in by_cat:
            continue

        cat_secs = sum(secs for _, secs, _, _ in by_cat[category]["activities"])
        cat_duration = format_duration(cat_secs)
        emoji = by_cat[category]["emoji"]

        md += f"| {emoji} {category} | **{cat_duration}** |\n"

    md += f"\n**TOTAL** : **{format_duration(total_secs)}**\n"

    return md, format_duration(total_secs), by_cat

def main():
    print("🔄 Synchronisation des timesheets Kimai...")

    timesheets = get_timesheets_today()
    print(f"📋 {len(timesheets)} timesheet(s) trouvé(s) aujourd'hui")

    if not timesheets:
        print("❌ Aucun timesheet enregistré")
        return

    agg = aggregate_by_activity(timesheets)
    md, total, by_cat = generate_markdown(agg)

    print(f"\n{md}")
    print(f"\n✅ Total du jour : {total}")
    print(f"✅ Nombre d'activités : {len(agg)}")

    # Générer données complètes pour JSON
    data = {
        "timestamp": datetime.now().isoformat(),
        "total_seconds": sum(agg.values()),
        "total_formatted": total,
        "activities": {
            f"{cat}-{act_id}": {
                "name": act_name,
                "duration_seconds": secs,
                "duration_formatted": format_duration(secs),
                "category": cat,
                "color": color
            }
            for (cat, act_id, act_name, color, _), secs in agg.items()
        },
        "by_category": {
            cat: {
                "total_seconds": sum(s for _, s, _, _ in acts["activities"]),
                "total_formatted": format_duration(sum(s for _, s, _, _ in acts["activities"])),
                "activities": [{"name": n, "duration": format_duration(s), "color": c, "id": a_id} for n, s, c, a_id in acts["activities"]]
            }
            for cat, acts in by_cat.items()
        }
    }

    # Générer le HTML
    html_content = generate_html_dashboard(data)

    # Sauvegarder JSON
    output_file = Path(__file__).parent / "kimai_dashboard.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    # Essayer chemins Obsidian (local + NAS)
    wiki_paths = [
        Path(__file__).parent.parent / "wiki" / "Informatique" / "Pointage_Stan" / "kimai_dashboard.json",
        Path("/volume2/JLS46/015_Obsidian/Brain_Stan/wiki/Informatique/Pointage_Stan/kimai_dashboard.json")
    ]

    saved_path = output_file
    dashboard_path = None
    for wiki_output in wiki_paths:
        try:
            if wiki_output.parent.exists():
                # Sauvegarder JSON
                with open(wiki_output, "w") as f:
                    json.dump(data, f, indent=2)
                saved_path = wiki_output

                # Sauvegarder HTML dans le markdown du dashboard
                dashboard_md = wiki_output.parent / "dashboard-kimai.md"
                if dashboard_md.exists():
                    with open(dashboard_md, "r", encoding="utf-8") as f:
                        md_content = f.read()

                    # Remplacer la section affichage
                    import re
                    pattern = r'(<div id="detail-section">).*?(</div>)'
                    replacement = f'<div id="detail-section">\n{html_content}\n</div>'
                    updated = re.sub(pattern, replacement, md_content, flags=re.DOTALL)

                    with open(dashboard_md, "w", encoding="utf-8") as f:
                        f.write(updated)

                    dashboard_path = dashboard_md

                break
        except Exception as e:
            continue

    print(f"\n💾 JSON: {saved_path}")
    if dashboard_path:
        print(f"💾 Dashboard: {dashboard_path}")

if __name__ == "__main__":
    main()
