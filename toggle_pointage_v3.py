from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx, os, json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/scripts/.env")

KIMAI_URL = "http://kimai:8001/api"
TOKEN     = os.environ["TOKEN_STAN"]
HEADERS   = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
DELAI_MIN = 2  # minutes anti-doublon

# Configuration V3 : 1 Client Stan → 2 Projets (Pro + Perso) → 24 Activités
KIMAI_CLIENT = 1  # Stan
KIMAI_PROJECTS = {
    "pro": {"id": 13, "name": "Stan_Pro"},
    "perso": {"id": 14, "name": "Stan_Perso"}
}

CATEGORIES = {
    "pro": {
        "presence": {
            "name": "Presence",
            "couleur": "#28a745",
            "activites": {
                "Presence - Bureau": 14,
                "Presence - Reunions": 15,
                "Presence - Support": 16,
                "Presence - Formation": 17
            }
        },
        "absences": {
            "name": "Absences",
            "couleur": "#dc3545",
            "activites": {
                "Absences - Conges": 18,
                "Absences - Maladie": 19,
                "Absences - Teletravail": 20,
                "Absences - Dimanche": 21
            }
        }
    },
    "perso": {
        "homelab": {
            "name": "Homelab",
            "couleur": "#3b82f6",
            "activites": {
                "Homelab - Infra Docker": 22,
                "Homelab - Serveurs NAS": 23,
                "Homelab - Reseau VPN": 24,
                "Homelab - Automatisations": 25
            }
        },
        "coding": {
            "name": "Coding Perso",
            "couleur": "#ef4444",
            "activites": {
                "Coding Perso - Python": 26,
                "Coding Perso - FastAPI": 27,
                "Coding Perso - Obsidian plugins": 28,
                "Coding Perso - Apprentissage": 29
            }
        },
        "obsidian": {
            "name": "Obsidian/Doc",
            "couleur": "#f59e0b",
            "activites": {
                "Obsidian/Doc - Wiki notes": 30,
                "Obsidian/Doc - Syntheses archivage": 31,
                "Obsidian/Doc - Dataview dashboards": 32,
                "Obsidian/Doc - Maintenance structure": 33
            }
        },
        "velo": {
            "name": "Velo",
            "couleur": "#10b981",
            "activites": {
                "Velo - Sorties parcours": 34,
                "Velo - Entretien maintenance": 35,
                "Velo - Entrainement physique": 36,
                "Velo - Materiel achat": 37
            }
        }
    }
}

app = FastAPI()

def minutes_depuis(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        now = datetime.now(dt.tzinfo)
        return (now - dt).total_seconds() / 60
    except Exception:
        return 999

def barre_flottante():
    """Barre flottante en haut à gauche avec l'activité en cours"""
    return """
<div id="barre-pointage" style="display:none; position:fixed; top:10px; left:10px; background:white; border:2px solid #333;
border-radius:8px; padding:12px 16px; z-index:9999; min-width:250px; box-shadow:0 4px 8px rgba(0,0,0,0.2); font-family:Arial,sans-serif">
    <div style="font-size:11px; color:#666; margin-bottom:4px">POINTAGE EN COURS</div>
    <div style="font-size:14px; font-weight:bold; color:#666; margin-bottom:4px" id="projet-cat">-</div>
    <div style="font-size:18px; font-weight:bold; color:#333; margin-bottom:8px" id="nom-activite">-</div>
    <div style="display:flex; justify-content:space-between; align-items:center">
        <div style="font-size:24px; font-weight:bold; color:#dc3545" id="chrono">00:00</div>
        <a href="#" onclick="fetch('/stop/stan').then(() => location.reload()); return false"
           style="background:#dc3545; color:white; padding:6px 12px; border-radius:4px; text-decoration:none; font-size:12px; font-weight:bold">
            STOP
        </a>
    </div>
</div>

<script>
async function updateBarre() {
    try {
        const resp = await fetch('/api/current');
        const data = await resp.json();
        if (data.activity) {
            document.getElementById('barre-pointage').style.display = 'block';
            document.getElementById('projet-cat').textContent = data.project + ' > ' + data.category;
            document.getElementById('nom-activite').textContent = data.activity;
            document.getElementById('nom-activite').parentElement.style.borderLeftWidth = '4px';
            document.getElementById('nom-activite').parentElement.style.borderLeftStyle = 'solid';
            document.getElementById('nom-activite').parentElement.style.borderLeftColor = data.color || '#333';
            document.getElementById('chrono').textContent = data.elapsed;
        } else {
            document.getElementById('barre-pointage').style.display = 'none';
        }
    } catch(e) {}
}

updateBarre();
setInterval(updateBarre, 500);
</script>
"""

def page_selection_projets():
    """Écran 0 : Sélection projet (PRO / PERSO)"""
    return """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Kimai - Pointage Stan</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.container { background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; text-align: center; max-width: 500px; width: 90%; }
.title { font-size: 28px; font-weight: bold; margin-bottom: 10px; color: #1f2937; }
.subtitle { font-size: 14px; color: #6b7280; margin-bottom: 40px; }
.boutons { display: grid; gap: 20px; }
.bouton { padding: 20px 30px; font-size: 18px; font-weight: bold; border-radius: 12px; cursor: pointer; text-decoration: none; color: white; border: none; transition: transform 0.2s; }
.bouton:hover { transform: scale(1.05); }
.bouton-pro { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.bouton-perso { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
</style></head>
<body>
<div class="container">
    <div class="title">⏱️ POINTAGE STAN</div>
    <div class="subtitle">Sélectionnez un projet</div>
    <div class="boutons">
        <a href="/select/stan?project=pro" class="bouton bouton-pro">👔 PRO (Carrière)</a>
        <a href="/select/stan?project=perso" class="bouton bouton-perso">🎨 PERSO (Loisirs)</a>
    </div>
</div>
""" + barre_flottante() + """
</body></html>"""

def page_selection_categories(project):
    """Écran 1 : Sélection catégorie par projet"""
    cats = CATEGORIES.get(project, {})
    if not cats:
        return "<h1>Erreur : projet invalide</h1>"

    boutons = f'<a href="/select/stan" style="background: #6b7280; margin-bottom: 20px;">◀ Retour</a>'

    for cat_key, cat_info in cats.items():
        couleur = cat_info["couleur"]
        nom = cat_info["name"]
        boutons += f'<a class="bouton" style="background-color:{couleur}" href="/select/stan?project={project}&category={cat_key}">{nom}</a>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Kimai - Catégories</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
.container {{ background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; text-align: center; max-width: 600px; width: 90%; }}
.title {{ font-size: 24px; font-weight: bold; margin-bottom: 30px; color: #1f2937; }}
.boutons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
.bouton {{ padding: 20px 15px; font-size: 16px; font-weight: bold; border-radius: 12px; cursor: pointer; text-decoration: none; color: white; border: none; transition: transform 0.2s; }}
.bouton:hover {{ transform: scale(1.05); }}
</style></head>
<body>
<div class="container">
    <div class="title">Choisir une catégorie</div>
    <div class="boutons">
        {boutons}
    </div>
</div>
""" + barre_flottante() + """
</body></html>"""

def page_selection_activites(project, category):
    """Écran 2 : Sélection activité"""
    cats = CATEGORIES.get(project, {}).get(category, {})
    if not cats:
        return "<h1>Erreur : catégorie invalide</h1>"

    boutons = f'<a href="/select/stan?project={project}" style="background: #6b7280; margin-bottom: 20px;">◀ Retour</a>'
    couleur = cats.get("couleur", "#333")
    cat_name = cats.get("name", "")

    for act_name, act_id in cats.get("activites", {}).items():
        boutons += f'<a class="bouton" style="background-color:{couleur}" href="/toggle/stan?project={project}&category={category}&activity={act_name}">{act_name}</a>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Kimai - Activités</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
.container {{ background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; text-align: center; max-width: 600px; width: 90%; }}
.title {{ font-size: 24px; font-weight: bold; margin-bottom: 30px; color: #1f2937; }}
.boutons {{ display: grid; grid-template-columns: 1fr; gap: 12px; }}
.bouton {{ padding: 16px 15px; font-size: 15px; font-weight: bold; border-radius: 10px; cursor: pointer; text-decoration: none; color: white; border: none; transition: transform 0.2s; }}
.bouton:hover {{ transform: scale(1.02); }}
</style></head>
<body>
<div class="container">
    <div class="title">◀ {cat_name}</div>
    <div class="boutons">
        {boutons}
    </div>
</div>
""" + barre_flottante() + """
</body></html>"""

@app.get("/select/stan", response_class=HTMLResponse)
async def select_stan(project: str = None, category: str = None):
    """Routes de sélection (3 écrans)"""
    if not project:
        # Écran 0 : Sélection projet
        return page_selection_projets()
    elif not category:
        # Écran 1 : Sélection catégorie
        return page_selection_categories(project)
    else:
        # Écran 2 : Sélection activité
        return page_selection_activites(project, category)

@app.get("/toggle/stan")
async def toggle_pointage(project: str, category: str, activity: str):
    """Crée ou bascule un timesheet"""
    try:
        # Récupérer activité ID
        activite_id = CATEGORIES[project][category]["activites"][activity]
        projet_id = KIMAI_PROJECTS[project]["id"]

        async with httpx.AsyncClient() as client:
            # Récupérer timesheet actif
            resp_active = await client.get(
                f"{KIMAI_URL}/timesheets/active",
                headers=HEADERS
            )

            active = resp_active.json() if resp_active.status_code == 200 else []

            # Arrêter ancien timesheet s'il existe et est ancien
            if active:
                for ts in active:
                    started = ts.get("started", "")
                    if minutes_depuis(started) > DELAI_MIN:
                        await client.patch(
                            f"{KIMAI_URL}/timesheets/{ts['id']}",
                            headers=HEADERS,
                            json={"end": datetime.now().isoformat()}
                        )

            # Créer nouveau timesheet
            response = await client.post(
                f"{KIMAI_URL}/timesheets",
                headers=HEADERS,
                json={
                    "project": projet_id,
                    "activity": activite_id,
                    "begin": datetime.now().isoformat()
                }
            )

            if response.status_code in [200, 201]:
                return JSONResponse({"status": "ok", "message": f"Timesheet créé : {activity}"})
            else:
                raise HTTPException(status_code=400, detail=f"Erreur Kimai : {response.text}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stop/stan")
async def stop_pointage():
    """Arrête le timesheet actif"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{KIMAI_URL}/timesheets/active",
                headers=HEADERS
            )

            active = resp.json() if resp.status_code == 200 else []

            if active:
                for ts in active:
                    await client.patch(
                        f"{KIMAI_URL}/timesheets/{ts['id']}",
                        headers=HEADERS,
                        json={"end": datetime.now().isoformat()}
                    )

            return JSONResponse({"status": "ok"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/current")
async def api_current():
    """Retourne l'activité en cours"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{KIMAI_URL}/timesheets/active",
                headers=HEADERS
            )

            if resp.status_code != 200:
                return {"activity": None}

            active = resp.json()
            if not active:
                return {"activity": None}

            ts = active[0]
            activity_id = ts.get("activity", {}).get("id")
            activity_name = ts.get("activity", {}).get("name", "")
            project_id = ts.get("project", {}).get("id")

            # Trouver project et category
            project_key = None
            category_key = None
            couleur = "#333"

            for proj_key, proj_info in KIMAI_PROJECTS.items():
                if proj_info["id"] == project_id:
                    project_key = proj_key
                    for cat_key, cat_info in CATEGORIES[proj_key].items():
                        if activity_id in cat_info["activites"].values():
                            category_key = cat_key
                            couleur = cat_info["couleur"]
                            break
                    break

            elapsed_sec = ts.get("duration", 0)
            hours = elapsed_sec // 3600
            minutes = (elapsed_sec % 3600) // 60
            elapsed = f"{int(hours):02d}:{int(minutes):02d}"

            return {
                "activity": activity_name,
                "project": KIMAI_PROJECTS.get(project_key, {}).get("name", ""),
                "category": CATEGORIES.get(project_key, {}).get(category_key, {}).get("name", ""),
                "elapsed": elapsed,
                "color": couleur
            }
    except Exception:
        return {"activity": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8059)
