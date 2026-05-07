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

PROJETS = {
    1: {"name": "Présence", "couleur": "#28a745"},
    2: {"name": "Absences", "couleur": "#dc3545"},
    8: {"name": "Homelab", "couleur": "#3b82f6"},
    9: {"name": "Coding Perso", "couleur": "#ef4444"},
    10: {"name": "Obsidian/Documentation", "couleur": "#f59e0b"},
    12: {"name": "Vélo", "couleur": "#10b981"}
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
border-radius:8px; padding:12px 16px; z-index:9999; min-width:200px; box-shadow:0 4px 8px rgba(0,0,0,0.2); font-family:Arial,sans-serif">
    <div style="font-size:11px; color:#666; margin-bottom:4px">POINTAGE EN COURS</div>
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
            document.getElementById('nom-activite').textContent = data.activity.name;
            document.getElementById('nom-activite').parentElement.style.borderLeftWidth = '4px';
            document.getElementById('nom-activite').parentElement.style.borderLeftStyle = 'solid';
            document.getElementById('nom-activite').parentElement.style.borderLeftColor = data.activity.color || '#333';
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
    """Affiche le menu de sélection des projets"""
    boutons = ""
    for project_id, project_info in PROJETS.items():
        couleur = project_info["couleur"]
        nom = project_info["name"]
        boutons += f'<a class="bouton" style="background-color:{couleur}" href="/select/stan?project={project_id}">{nom}</a>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;padding:20px;display:flex;align-items:center;justify-content:center;
min-height:100vh;background:#f0f0f0;font-family:Arial,sans-serif}}
.container{{background:white;border-radius:10px;padding:30px;box-shadow:0 4px 6px rgba(0,0,0,0.1);
max-width:500px;width:100%}}
h1{{text-align:center;color:#333;margin:0 0 30px 0;font-size:24px}}
.grille{{display:grid;grid-template-columns:1fr;gap:15px;margin-bottom:30px}}
.bouton{{color:white;padding:25px;text-align:center;
border-radius:8px;text-decoration:none;font-weight:bold;font-size:18px;
transition:background 0.3s;display:flex;align-items:center;justify-content:center;
min-height:70px}}
.bouton:hover{{opacity:0.9}}
</style>
</head>
<body>
{barre_flottante()}
<div class="container">
<h1>Choisir un projet</h1>
<div class="grille">
{boutons}
</div>
</div>
</body></html>"""

def page_selection_activities(activities, project_name):
    """Affiche le menu de sélection des activités avec boutons colorés"""
    boutons = ""
    for activity in activities:
        activity_id = activity["id"]
        activity_name = activity["name"]
        couleur = activity.get("color") or "#6c757d"
        boutons += f'<a class="bouton" style="background-color:{couleur}" onclick="window.open(\'/toggle/stan?activity={activity_id}\', \'popup\', \'width=500,height=600\'); return false">{activity_name}</a>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;padding:20px;display:flex;align-items:center;justify-content:center;
min-height:100vh;background:#f0f0f0;font-family:Arial,sans-serif}}
.container{{background:white;border-radius:10px;padding:30px;box-shadow:0 4px 6px rgba(0,0,0,0.1);
max-width:500px;width:100%}}
h1{{text-align:center;color:#333;margin:0 0 10px 0;font-size:24px}}
.sous-titre{{text-align:center;color:#666;margin:0 0 30px 0;font-size:14px}}
.grille{{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-bottom:30px}}
.bouton{{color:white;padding:20px;text-align:center;
border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;
transition:background 0.3s;display:flex;align-items:center;justify-content:center;
min-height:60px}}
.bouton:hover{{opacity:0.9}}
.bouton-fin{{background:#dc3545;grid-column:1/-1}}
</style>
</head>
<body>
{barre_flottante()}
<div class="container">
<h1>Activités</h1>
<p class="sous-titre">{project_name}</p>
<div class="grille">
{boutons}
<a href="/stop/stan" class="bouton bouton-fin">Fin du pointage</a>
</div>
</div>
</body></html>"""

def page_html(action, heure):
    """Affiche confirmation de démarrage/arrêt"""
    if action == "start":
        couleur = "#28a745"
        icone = "▶"
        texte = "Pointage début"
    else:
        couleur = "#dc3545"
        icone = "⏹"
        texte = "Pointage fin"
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;display:flex;align-items:center;justify-content:center;
height:100vh;background:{couleur};font-family:Arial,sans-serif;color:white}}
.box{{text-align:center;padding:40px}}
.icone{{font-size:80px}}
.texte{{font-size:28px;font-weight:bold;margin:20px 0}}
.heure{{font-size:22px;opacity:0.9}}
.barre{{height:6px;background:rgba(255,255,255,0.4);border-radius:3px;margin-top:30px;overflow:hidden}}
.barre-inner{{height:100%;background:white;border-radius:3px;animation:progress 2s linear forwards}}
@keyframes progress{{from{{width:100%}}to{{width:0%}}}}
</style>
<script>setTimeout(function(){{window.close();}},2000);</script>
</head>
<body><div class="box">
<div class="icone">{icone}</div>
<div class="texte">{texte}</div>
<div class="heure">{heure}</div>
<div class="barre"><div class="barre-inner"></div></div>
</div></body></html>"""

def page_doublon(heure):
    """Affiche alerte doublon"""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;display:flex;align-items:center;justify-content:center;
height:100vh;background:#fd7e14;font-family:Arial,sans-serif;color:white}}
.box{{text-align:center;padding:40px}}
.icone{{font-size:80px}}
.texte{{font-size:24px;font-weight:bold;margin:20px 0}}
.heure{{font-size:20px;opacity:0.9}}
.barre{{height:6px;background:rgba(255,255,255,0.4);border-radius:3px;margin-top:30px;overflow:hidden}}
.barre-inner{{height:100%;background:white;border-radius:3px;animation:progress 2s linear forwards}}
@keyframes progress{{from{{width:100%}}to{{width:0%}}}}
</style>
<script>setTimeout(function(){{window.close();}},2000);</script>
</head>
<body><div class="box">
<div class="icone">!</div>
<div class="texte">Doublon ignoré</div>
<div class="heure">{heure}</div>
<div class="barre"><div class="barre-inner"></div></div>
</div></body></html>"""

@app.get("/install", response_class=HTMLResponse)
async def install_page():
    """Page d'installation du userscript"""
    return """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Installation - Widget Kimai</title>
<style>
body {
  margin: 0;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
}
.container {
  background: white;
  border-radius: 12px;
  padding: 40px;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}
h1 {
  color: #333;
  margin-top: 0;
  text-align: center;
  font-size: 28px;
}
.step {
  margin: 25px 0;
  padding: 20px;
  background: #f5f5f5;
  border-left: 4px solid #667eea;
  border-radius: 4px;
}
.step-number {
  display: inline-block;
  background: #667eea;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  text-align: center;
  line-height: 30px;
  font-weight: bold;
  margin-right: 10px;
}
.button {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  margin: 10px 5px 10px 0;
  cursor: pointer;
  border: none;
  font-size: 14px;
  transition: background 0.3s;
}
.button:hover { background: #764ba2; }
.button.secondary { background: #666; }
.button.secondary:hover { background: #555; }
.button.success { background: #10b981; }
.button.success:hover { background: #059669; }
.status {
  text-align: center;
  padding: 15px;
  background: #e8f5e9;
  border: 1px solid #4caf50;
  border-radius: 4px;
  color: #2e7d32;
  margin: 20px 0;
}
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 20px 0;
}
.project-card {
  background: #f9f9f9;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid #667eea;
}
.project-card h4 {
  margin: 0 0 10px 0;
  color: #333;
}
.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 13px;
}
.activity-list li {
  padding: 5px 0;
  color: #555;
}
.activity-list li:before {
  content: "□ ";
  color: #999;
}
.tab-buttons {
  display: flex;
  gap: 10px;
  margin: 20px 0;
  border-bottom: 2px solid #ddd;
}
.tab-button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}
.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}
.tab-content { display: none; }
.tab-content.active { display: block; }
</style>
</head><body>
<div class="container">
  <h1>⏱️ Pointage Personnel NFC</h1>

  <div class="status">
    ✓ Toggle pointage sur téléphone + 6 projets personnalisés
  </div>

  <div class="step">
    <span class="step-number">1</span>
    <strong>Crée les activités dans Kimai</strong><br>
    <small style="color:#666">Admin → Activités → + Nouvelle</small><br><br>

    <div class="project-grid">
      <div class="project-card">
        <h4>🔵 Homelab</h4>
        <ul class="activity-list">
          <li>Docker</li>
          <li>NAS</li>
          <li>Networking</li>
        </ul>
      </div>
      <div class="project-card">
        <h4>🔴 Coding Perso</h4>
        <ul class="activity-list">
          <li>Dev</li>
          <li>Bug fix</li>
          <li>Learning</li>
        </ul>
      </div>
      <div class="project-card">
        <h4>🟠 Obsidian/Doc</h4>
        <ul class="activity-list">
          <li>Écriture</li>
          <li>Organisation</li>
          <li>Linking</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="step">
    <span class="step-number">2</span>
    <strong>Utilise le pointage</strong><br><br>
    <strong>Pointage NFC (téléphone):</strong><br>
    Scanne tag NFC → Sélectionne projet → Choisis activité → Chronomètre démarre ! ⏱️<br><br>
    <a href="http://192.168.1.15:8059/select/stan" class="button secondary">📱 Accéder au toggle</a>
  </div>

  <div style="text-align:center; color:#666; margin-top:40px; padding-top:20px; border-top:1px solid #ddd">
    <p><strong>Projets disponibles:</strong> Présence • Absences • Homelab • Coding Perso • Obsidian/Doc</p>
    <p style="font-size:12px">Pointage NFC | Chronomètre automatique | Couleurs par activité | Sync temps réel</p>
  </div>
</div>
</body></html>"""

@app.get("/kimai-pointage-widget.user.js")
async def serve_userscript():
    """Sert le userscript Tampermonkey"""
    script = """// ==UserScript==
// @name         Kimai - Widget Pointage en cours
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Affiche l'activité en cours avec chronomètre en haut à gauche de Kimai
// @author       Stan
// @match        http://192.168.1.15:8055/*
// @match        http://localhost:8055/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  const barre = document.createElement('div');
  barre.id = 'barre-pointage-kimai';
  barre.style.cssText = 'display:none;position:fixed;top:10px;left:10px;background:white;border:2px solid #333;border-radius:8px;padding:12px 16px;z-index:99999;min-width:220px;box-shadow:0 4px 8px rgba(0,0,0,0.2);font-family:Arial,sans-serif';

  barre.innerHTML = `
    <div style="font-size:11px;color:#666;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px">⏱️ Pointage</div>
    <div style="font-size:16px;font-weight:bold;color:#333;margin-bottom:8px;padding-left:4px;border-left:4px solid #999" id="nom-activite">-</div>
    <div style="display:flex;justify-content:space-between;align-items:center;gap:10px">
      <div style="font-size:28px;font-weight:bold;color:#dc3545;font-family:monospace" id="chrono">00:00</div>
      <a href="#" id="btn-stop" style="background:#dc3545;color:white;padding:8px 12px;border-radius:4px;text-decoration:none;font-size:12px;font-weight:bold;cursor:pointer">STOP</a>
    </div>
  `;

  document.body.appendChild(barre);

  async function updateBarre() {
    try {
      const resp = await fetch('http://192.168.1.15:8059/api/current');
      const data = await resp.json();
      if (data.activity) {
        barre.style.display = 'block';
        document.getElementById('nom-activite').textContent = data.activity.name;
        document.getElementById('nom-activite').style.borderLeftColor = data.activity.color || '#999';
        document.getElementById('chrono').textContent = data.elapsed;
      } else {
        barre.style.display = 'none';
      }
    } catch(e) {}
  }

  document.getElementById('btn-stop').addEventListener('click', async function(e) {
    e.preventDefault();
    try {
      await fetch('http://192.168.1.15:8059/stop/stan');
      updateBarre();
    } catch(e) {}
  });

  updateBarre();
  setInterval(updateBarre, 500);
})();
"""
    from fastapi.responses import Response
    return Response(content=script, media_type="application/x-javascript")

@app.get("/api/current")
async def get_current_activity():
    """Retourne l'activité en cours au format JSON"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS, params={"active": 1})
            actifs = r.json()

            if not actifs:
                return JSONResponse({"activity": None})

            pointage = actifs[0]
            activity_data = pointage.get("activity", {})
            activity_id = activity_data.get("id") if isinstance(activity_data, dict) else activity_data
            activity_name = activity_data.get("name", "Inconnu") if isinstance(activity_data, dict) else "Inconnu"
            activity_color = activity_data.get("color", "#666") if isinstance(activity_data, dict) else "#666"

            # Calculer le temps écoulé
            debut_str = pointage.get("begin", "")
            if debut_str:
                elapsed_min = minutes_depuis(debut_str)
                heures = int(elapsed_min // 60)
                minutes = int(elapsed_min % 60)
                elapsed_str = f"{heures:02d}:{minutes:02d}"
            else:
                elapsed_str = "00:00"

            return JSONResponse({
                "activity": {
                    "id": activity_id,
                    "name": activity_name,
                    "color": activity_color
                },
                "elapsed": elapsed_str,
                "started": debut_str
            })
    except Exception as e:
        return JSONResponse({"activity": None, "error": str(e)})

@app.get("/select/stan", response_class=HTMLResponse)
async def select_project_or_activity(project: int = None):
    """Affiche sélection de projet OU sélection d'activités"""
    if project is None:
        # Affiche la sélection de projets
        return HTMLResponse(content=page_selection_projets())

    # Affiche les activités du projet choisi
    try:
        if project not in PROJETS:
            return HTMLResponse(content="<h1>Projet invalide</h1>")

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{KIMAI_URL}/activities", headers=HEADERS,
                                params={"project": project, "size": 100})
            activities = r.json()

            if not activities:
                return HTMLResponse(content="<h1>Aucune activité pour ce projet</h1>")

            project_name = PROJETS[project]["name"]
            return HTMLResponse(content=page_selection_activities(activities, project_name))
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erreur: {str(e)}</h1>")

@app.get("/toggle/stan", response_class=HTMLResponse)
async def toggle(activity: int, project: int = 1):
    """Toggle pointage avec switch automatique si nouvelle activité"""
    heure = datetime.now().strftime("%H:%M")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Cherche un pointage actif
            r = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS, params={"active": 1})
            actifs = r.json()

            if actifs:
                pointage_actif = actifs[0]
                tid = pointage_actif["id"]
                activity_data = pointage_actif.get("activity", {})
                activity_actuelle = activity_data.get("id") if isinstance(activity_data, dict) else activity_data
                debut_str = pointage_actif.get("begin", "")

                # Anti-doublon : si même activity et scannée < 2 min
                if activity == activity_actuelle and debut_str and minutes_depuis(debut_str) < DELAI_MIN:
                    return HTMLResponse(content=page_doublon(heure))

                # Si NOUVELLE activité → switch (arrête l'ancienne, démarre la nouvelle)
                if activity != activity_actuelle:
                    await client.patch(f"{KIMAI_URL}/timesheets/{tid}/stop", headers=HEADERS)
                    await client.post(f"{KIMAI_URL}/timesheets", headers=HEADERS,
                                     json={"project": project, "activity": activity})
                    return HTMLResponse(content=page_html("start", heure))
                else:
                    # Même activité → simple toggle (arrête)
                    await client.patch(f"{KIMAI_URL}/timesheets/{tid}/stop", headers=HEADERS)
                    return HTMLResponse(content=page_html("stop", heure))
            else:
                # Pas de pointage actif → en créer un pour l'activity choisie
                today = datetime.now().strftime("%Y-%m-%d")
                r2 = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS,
                                     params={"begin": f"{today}T00:00:00",
                                            "end": f"{today}T23:59:59", "size": 1})
                recents = r2.json()
                if recents and recents[0].get("end"):
                    if minutes_depuis(recents[0]["end"]) < DELAI_MIN:
                        return HTMLResponse(content=page_doublon(heure))

                await client.post(f"{KIMAI_URL}/timesheets", headers=HEADERS,
                                 json={"project": project, "activity": activity})
                return HTMLResponse(content=page_html("start", heure))
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erreur: {str(e)}</h1>")

@app.get("/stop/stan", response_class=HTMLResponse)
async def stop_pointage():
    """Arrête le pointage courant (bouton Fin)"""
    heure = datetime.now().strftime("%H:%M")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Récupère le pointage actif
            r = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS, params={"active": 1})
            actifs = r.json()

            if actifs:
                tid = actifs[0]["id"]
                await client.patch(f"{KIMAI_URL}/timesheets/{tid}/stop", headers=HEADERS)
                return HTMLResponse(content=page_html("stop", heure))
            else:
                return HTMLResponse(content="<h1>Aucun pointage actif</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erreur: {str(e)}</h1>")
