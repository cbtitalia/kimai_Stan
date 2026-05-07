from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/scripts/.env")

KIMAI_URL = "http://kimai:8001/api"
TOKEN     = os.environ["TOKEN_STAN"]
HEADERS   = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
PROJECT   = 1
ACTIVITY  = 1
DELAI_MIN = 2  # minutes anti-doublon

app = FastAPI()

def minutes_depuis(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        now = datetime.now(dt.tzinfo)
        return (now - dt).total_seconds() / 60
    except Exception:
        return 999

def page_html(action, heure):
    if action == "start":
        couleur = "#28a745"
        icone = "▶"
        texte = "Pointage debut"
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
<div class="texte">Doublon ignore</div>
<div class="heure">{heure}</div>
<div class="barre"><div class="barre-inner"></div></div>
</div></body></html>"""

@app.get("/toggle/{prenom}", response_class=HTMLResponse)
async def toggle(prenom: str):
    if prenom.lower() != "stan":
        raise HTTPException(status_code=403, detail="Non autorise")
    heure = datetime.now().strftime("%H:%M")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS, params={"active": 1})
        actifs = r.json()
        if actifs:
            debut_str = actifs[0].get("begin", "")
            if debut_str and minutes_depuis(debut_str) < DELAI_MIN:
                return HTMLResponse(content=page_doublon(heure))
            tid = actifs[0]["id"]
            await client.patch(f"{KIMAI_URL}/timesheets/{tid}/stop", headers=HEADERS)
            return HTMLResponse(content=page_html("stop", heure))
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            r2 = await client.get(f"{KIMAI_URL}/timesheets", headers=HEADERS,
                                   params={"begin": f"{today}T00:00:00",
                                           "end": f"{today}T23:59:59", "size": 1})
            recents = r2.json()
            if recents and recents[0].get("end"):
                if minutes_depuis(recents[0]["end"]) < DELAI_MIN:
                    return HTMLResponse(content=page_doublon(heure))
            await client.post(f"{KIMAI_URL}/timesheets", headers=HEADERS,
                              json={"project": PROJECT, "activity": ACTIVITY})
            return HTMLResponse(content=page_html("start", heure))
