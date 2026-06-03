"""
toggle_pointage_cci.py — Phase 3 CCI Integration API Template

FastAPI toggle service for Kimai with CCI-specific projects and activities.
This is a TEMPLATE — customize with actual project IDs discovered during onboarding.

Projects:
- Stan_CCI90 (ID 20) — Work at CCI
- Stan_ISO27001 (ID 21) — Training & Certification
- Stan_CapCyber (ID 22) — Event Management
- Stan_Perso (ID 14) — Personal (unchanged)

Status: Ready for Phase 3 (June 2026+)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx, os, json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/scripts/.env")

KIMAI_URL = "http://kimai:8001/api"
TOKEN = os.environ.get("TOKEN_STAN", "")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
DELAI_MIN = 2  # Anti-doublon delay (minutes)

# Configuration Phase 3: CCI Projects
KIMAI_CLIENT = 1  # Stan

KIMAI_PROJECTS = {
    "cci90": {"id": 20, "name": "Stan_CCI90"},
    "iso27001": {"id": 21, "name": "Stan_ISO27001"},
    "cap_cyber": {"id": 22, "name": "Stan_CapCyber"},
    "perso": {"id": 14, "name": "Stan_Perso"}
}

CATEGORIES = {
    "cci90": {
        "prospection": {
            "name": "Prospection",
            "color": "#3b82f6",
            "activities": {
                "Prospection - Identification": 38,
                "Prospection - Appels": 39,
                "Prospection - Emails": 40,
                "Prospection - Meetings": 41
            }
        },
        "ateliers": {
            "name": "Ateliers",
            "color": "#8b5cf6",
            "activities": {
                "Ateliers - Sensibilisation": 42,
                "Ateliers - Supports": 43,
                "Ateliers - Facilitation": 44
            }
        },
        "diagnostics": {
            "name": "Diagnostics",
            "color": "#ec4899",
            "activities": {
                "Diagnostics - Visite": 45,
                "Diagnostics - Questionnaire": 46,
                "Diagnostics - Rapport": 47
            }
        },
        "cap_cyber": {
            "name": "Cap Cyber",
            "color": "#f59e0b",
            "activities": {
                "Cap Cyber - Coordination": 48,
                "Cap Cyber - Debriefing": 49,
                "Cap Cyber - Planning v6": 50
            }
        },
        "admin": {
            "name": "Administration",
            "color": "#6b7280",
            "activities": {
                "Admin - Integration": 51,
                "Admin - Meetings": 52,
                "Admin - Documentation": 53
            }
        }
    },
    "iso27001": {
        "cours": {
            "name": "Cours",
            "color": "#06b6d4",
            "activities": {
                "Cours - Module 1": 54,
                "Cours - Module 2": 55,
                "Cours - Module 3": 56,
                "Cours - Module 4": 57,
                "Cours - Module 5": 58
            }
        },
        "revisions": {
            "name": "Révisions",
            "color": "#8b5cf6",
            "activities": {
                "Revisions - Domaine 1-3": 59,
                "Revisions - Domaine 4-6": 60,
                "Revisions - Domaine 7-8": 61,
                "Revisions - Cas pratiques": 62
            }
        },
        "examen": {
            "name": "Examen",
            "color": "#ef4444",
            "activities": {
                "Examen - Blanc": 63,
                "Examen - Officiel": 64
            }
        }
    },
    "cap_cyber": {
        "logistique": {
            "name": "Logistique",
            "color": "#10b981",
            "activities": {
                "Logistique - Planning": 65,
                "Logistique - Vendors": 66,
                "Logistique - Feedback": 67
            }
        },
        "post_event": {
            "name": "Post-Event",
            "color": "#6b7280",
            "activities": {
                "Post-Event - Lessons Learned": 68,
                "Post-Event - Planning v6": 69
            }
        }
    },
    "perso": {
        # Same as Phase 2 (unchanged)
        "homelab": {
            "name": "Homelab",
            "color": "#3b82f6",
            "activities": {
                "Homelab - Infra Docker": 70,
                "Homelab - Serveurs NAS": 71,
                "Homelab - Reseau VPN": 72,
                "Homelab - Automatisations": 73
            }
        },
        "coding": {
            "name": "Coding",
            "color": "#10b981",
            "activities": {
                "Coding - Python": 74,
                "Coding - FastAPI": 75,
                "Coding - Obsidian plugins": 76,
                "Coding - Learning": 77
            }
        },
        "obsidian": {
            "name": "Obsidian/Doc",
            "color": "#f59e0b",
            "activities": {
                "Obsidian - Wiki": 78,
                "Obsidian - Syntheses": 79,
                "Obsidian - Dataview": 80,
                "Obsidian - Maintenance": 81
            }
        },
        "velo": {
            "name": "Vélo",
            "color": "#ec4899",
            "activities": {
                "Velo - Sorties": 82,
                "Velo - Entretien": 83,
                "Velo - Entrainement": 84,
                "Velo - Materiel": 85
            }
        }
    }
}

app = FastAPI(title="Pointage Stan Phase 3 (CCI)", version="3.1")

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "version": "3.1", "phase": "CCI Integration"}

# Main toggle endpoint
@app.get("/toggle/stan", response_class=HTMLResponse)
async def toggle_stan_get(project: int = None):
    """
    Toggle timesheet for specified project.

    Query params:
    - project: Kimai project ID (20=CCI90, 21=ISO27001, 22=CapCyber, 14=Perso)

    Returns: HTML UI with status message + auto-close
    """
    if not project:
        return error_html("Erreur", "Project ID required (project=20|21|22|14)")

    try:
        result = await toggle_logic(project)
        return format_response(result)
    except Exception as e:
        return error_html("Erreur API", str(e))

@app.post("/toggle/stan")
async def toggle_stan_post(project: int = None):
    """POST variant of toggle endpoint"""
    return await toggle_stan_get(project)

# Activity selection endpoint (Phase 3 feature)
@app.get("/activities/stan", response_class=JSONResponse)
async def get_activities(project: int):
    """
    Get available activities for a project.

    Returns:
    {
      "project_id": 20,
      "project_name": "Stan_CCI90",
      "categories": [
        {
          "name": "Prospection",
          "activities": [
            {"id": 38, "name": "Identification"},
            ...
          ]
        }
      ]
    }
    """
    project_key = get_project_key(project)
    if not project_key:
        return {"error": "Unknown project"}

    project_config = KIMAI_PROJECTS[project_key]
    categories_data = []

    if project_key in CATEGORIES:
        for cat_key, cat_data in CATEGORIES[project_key].items():
            activities = [
                {"id": act_id, "name": act_name}
                for act_name, act_id in cat_data["activities"].items()
            ]
            categories_data.append({
                "name": cat_data["name"],
                "color": cat_data["color"],
                "activities": activities
            })

    return {
        "project_id": project,
        "project_name": project_config["name"],
        "categories": categories_data
    }

# Async toggle logic
async def toggle_logic(project_id: int):
    """
    Main toggle logic: start or stop timesheet for project.

    Returns: {"status": "started|stopped", "duration_min": X}
    """
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # Check active timesheets
            r = await client.get(
                f"{KIMAI_URL}/timesheets?active=1&user=1",
                headers=HEADERS
            )

            if r.status_code != 200:
                return {"status": "error", "message": f"API error: {r.status_code}"}

            active_timesheets = r.json()

            if active_timesheets:
                # Stop active timesheet
                ts = active_timesheets[0]
                ts_id = ts["id"]
                begin = ts.get("begin", "")

                r = await client.patch(
                    f"{KIMAI_URL}/timesheets/{ts_id}/stop",
                    headers=HEADERS
                )

                if r.status_code == 200:
                    try:
                        begin_dt = datetime.fromisoformat(begin.replace("Z", "+00:00"))
                        end_dt = datetime.now(begin_dt.tzinfo) if begin_dt.tzinfo else datetime.now()
                        duration = int((end_dt - begin_dt).total_seconds() // 60)
                        hours = duration // 60
                        minutes = duration % 60
                        duration_str = f"{hours}h {minutes}m"
                    except:
                        duration_str = "?"

                    return {
                        "status": "stopped",
                        "project": project_id,
                        "duration_min": duration,
                        "duration_str": duration_str
                    }
            else:
                # Start new timesheet
                payload = {
                    "project": project_id,
                    "activity": get_default_activity(project_id),
                    "user": 1,
                    "begin": datetime.now().isoformat()
                }

                r = await client.post(
                    f"{KIMAI_URL}/timesheets",
                    json=payload,
                    headers=HEADERS
                )

                if r.status_code == 200:
                    now = datetime.now()
                    time_str = now.strftime("%H:%M")
                    return {
                        "status": "started",
                        "project": project_id,
                        "time": time_str
                    }
                else:
                    return {"status": "error", "message": f"POST failed: {r.status_code}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Helper functions
def get_project_key(project_id: int):
    """Map Kimai project ID to config key"""
    for key, proj in KIMAI_PROJECTS.items():
        if proj["id"] == project_id:
            return key
    return None

def get_default_activity(project_id: int):
    """Get first activity for project (for auto-selection)"""
    project_key = get_project_key(project_id)
    if project_key and project_key in CATEGORIES:
        first_category = list(CATEGORIES[project_key].values())[0]
        first_activity_id = list(first_category["activities"].values())[0]
        return first_activity_id
    return 1  # Fallback

def get_project_color(project_id: int):
    """Get primary color for project"""
    colors = {
        20: "#3b82f6",  # Blue (CCI90)
        21: "#06b6d4",  # Cyan (ISO27001)
        22: "#f59e0b",  # Amber (CapCyber)
        14: "#ec4899"   # Pink (Perso)
    }
    return colors.get(project_id, "#6b7280")

def format_response(result):
    """Format API response as HTML"""
    status = result.get("status", "error")
    project_id = result.get("project", "?")

    if status == "started":
        time = result.get("time", "?")
        return f'''
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background:{get_project_color(project_id)};margin:0;height:100vh;display:flex;align-items:center;justify-content:center;color:white">
<div style="text-align:center"><div style="font-size:48px;font-weight:bold">▶ Pointage démarré</div><div style="font-size:96px;font-weight:bold;margin-top:40px">{time}</div></div>
</body>
</html>
        '''
    elif status == "stopped":
        duration = result.get("duration_str", "?")
        return f'''
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background:#6b7280;margin:0;height:100vh;display:flex;align-items:center;justify-content:center;color:white">
<div style="text-align:center"><div style="font-size:48px;font-weight:bold">⏸ Pointage arrêté</div><div style="font-size:80px;font-weight:bold;margin-top:40px">Durée: {duration}</div></div>
</body>
</html>
        '''
    else:
        return error_html("Erreur API", result.get("message", "Unknown error"))

def error_html(title, message):
    """Format error as HTML"""
    return f'''
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background:#ef4444;margin:0;height:100vh;display:flex;align-items:center;justify-content:center;color:white">
<div style="text-align:center"><div style="font-size:48px;font-weight:bold">❌ {title}</div><div style="font-size:32px;margin-top:40px">{message}</div></div>
</body>
</html>
    '''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8059)
