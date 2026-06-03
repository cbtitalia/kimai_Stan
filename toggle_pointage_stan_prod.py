from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import os, json, httpx

app = FastAPI(title="Pointage Stan NFC", version="3.0")
KIMAI_URL = os.getenv("KIMAI_URL", "http://kimai:8001/api")
TOKEN_ADMIN = os.getenv("TOKEN_STAN", "")
KIMAI_HEADERS = {"Authorization": f"Bearer {TOKEN_ADMIN}", "Content-Type": "application/json"}

PRESENCE_PROJECT = 1
PRESENCE_ACTIVITY = 1
USER_ID = 1

@app.get("/health")
async def health():
    return {"status": "ok"}

async def nfc_logic():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{KIMAI_URL}/timesheets?active=1&user={USER_ID}", headers=KIMAI_HEADERS)
            if r.status_code != 200:
                print(f"[ERROR] GET /timesheets failed: {r.status_code} {r.text}")
                return {"action": "Erreur", "data": "API"}
            
            actifs = r.json()
            
            if actifs:
                ts = actifs[0]
                ts_id = ts["id"]
                begin = ts.get("begin", "")
                
                r = await client.patch(f"{KIMAI_URL}/timesheets/{ts_id}/stop", headers=KIMAI_HEADERS)
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
                    return {"action": "Fin", "data": duration_str}
            else:
                payload = {"project": PRESENCE_PROJECT, "activity": PRESENCE_ACTIVITY, "user": USER_ID, "begin": datetime.now().isoformat()}
                r = await client.post(f"{KIMAI_URL}/timesheets", json=payload, headers=KIMAI_HEADERS)
                print(f"[DEBUG] POST /timesheets: {r.status_code}")
                if r.status_code == 200:
                    now = datetime.now()
                    time_str = now.strftime("%H:%M")
                    return {"action": "Debut", "data": time_str}
                else:
                    print(f"[ERROR] POST /timesheets failed: {r.status_code} {r.text}")
                    return {"action": "Erreur", "data": f"POST:{r.status_code}"}
    except Exception as e:
        print(f"[ERROR] {e}")
    
    return {"action": "Erreur", "data": "inconnu"}

@app.get("/nfc/stan", response_class=HTMLResponse)
async def nfc_stan_get():
    result = await nfc_logic()
    action = result["action"]
    data = result["data"]
    
    if action == "Debut":
        return f'<html><head><meta charset="utf-8"></head><body style="background:#4CAF50;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="text-align:center;color:white"><div style="font-size:56px;font-weight:bold">Debut pointage</div><div style="font-size:120px;font-weight:bold;margin-top:40px">{data}</div></div></body></html>'
    elif action == "Fin":
        return f'<html><head><meta charset="utf-8"></head><body style="background:#F44336;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="text-align:center;color:white"><div style="font-size:56px;font-weight:bold">Fin pointage</div><div style="font-size:80px;font-weight:bold;margin-top:40px">Duree: {data}</div></div></body></html>'
    else:
        return f'<html><body style="background:#FF0000;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="color:white;font-size:48px">Erreur: {data}</div></body></html>'

@app.post("/nfc/stan", response_class=HTMLResponse)
async def nfc_stan_post():
    result = await nfc_logic()
    action = result["action"]
    data = result["data"]
    
    if action == "Debut":
        return f'<html><head><meta charset="utf-8"></head><body style="background:#4CAF50;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="text-align:center;color:white"><div style="font-size:56px;font-weight:bold">Debut pointage</div><div style="font-size:120px;font-weight:bold;margin-top:40px">{data}</div></div></body></html>'
    elif action == "Fin":
        return f'<html><head><meta charset="utf-8"></head><body style="background:#F44336;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="text-align:center;color:white"><div style="font-size:56px;font-weight:bold">Fin pointage</div><div style="font-size:80px;font-weight:bold;margin-top:40px">Duree: {data}</div></div></body></html>'
    else:
        return f'<html><body style="background:#FF0000;margin:0;height:100vh;display:flex;align-items:center;justify-content:center"><div style="color:white;font-size:48px">Erreur: {data}</div></body></html>'
