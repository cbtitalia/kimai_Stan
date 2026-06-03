; XKeys Pointage Stan — AutoHotkey v2 Script
; Captures XKeys 24 touches and sends to Kimai Toggle API
; Requires: AutoHotkey v2.0+, XKeys 24 keyboard programmed with F13-F24

#Requires AutoHotkey v2.0
#SingleInstance Force

; Configuration
API_URL := "http://192.168.1.15:8059/toggle/stan"
TOKEN := "admin_token_2026"  ; From .env TOKEN_STAN

; Project mapping: F13-F24 → Project IDs
PROJECT_MAP := Map(
    "F13", 13,  ; Stan_Pro
    "F14", 14,  ; Stan_Perso
    "F15", 19,  ; Divers (or CCI projects in future)
    "F16", 20,  ; Reserved
    "F17", 21,  ; Reserved
    "F18", 22,  ; Reserved
    "F19", 23,  ; Reserved
    "F20", 24   ; Reserved
)

; Color mapping for Toast notifications
COLOR_MAP := Map(
    13, "0x28a745",  ; Green (Pro)
    14, "0xdc3545",  ; Red (Perso)
    19, "0xffc107",  ; Yellow (Divers)
    20, "0x17a2b8",  ; Cyan
    21, "0x6f42c1",  ; Purple
    22, "0x20c997",  ; Teal
    23, "0xe83e8c",  ; Pink
    24, "0x6c757d"   ; Gray
)

; Initialize
current_project := 0
current_status := "stopped"

; F13: Toggle Stan_Pro
F13::HandleProjectToggle(13)

; F14: Toggle Stan_Perso
F14::HandleProjectToggle(14)

; F15: Toggle Divers
F15::HandleProjectToggle(19)

; F16-F20: Reserved for future projects
F16::HandleProjectToggle(20)
F17::HandleProjectToggle(21)
F18::HandleProjectToggle(22)
F19::HandleProjectToggle(23)
F20::HandleProjectToggle(24)

; ESC: Stop current timesheet (safety)
Esc::HandleStop()

; Main handler function
HandleProjectToggle(project_id) {
    global current_project, current_status, API_URL, TOKEN

    ; Build API call
    url := API_URL . "?project=" . project_id
    headers := Map("Authorization", "Bearer " . TOKEN, "Content-Type", "application/json")

    try {
        response := CallAPI(url, headers)

        if (response.status = "started") {
            ShowToast("▶ Pointage démarré", "Projet: " . GetProjectName(project_id), COLOR_MAP[project_id])
            current_project := project_id
            current_status := "started"
        } else if (response.status = "stopped") {
            duration := response.duration_min ? response.duration_min . " min" : "?"
            ShowToast("⏸ Pointage arrêté", "Durée: " . duration, "0x6c757d")
            current_status := "stopped"
        } else {
            ShowToast("❌ Erreur", response.error, "0xFF0000")
        }
    } catch as err {
        ShowToast("❌ API Error", err.Message, "0xFF0000")
    }
}

HandleStop() {
    global current_project, current_status

    if (current_status = "stopped") {
        ShowToast("⚠ Aucun pointage actif", "", "0xFFC107")
        return
    }

    ; Send stop request to current project
    HandleProjectToggle(current_project)
}

; API Call function (requires WinHTTP or similar)
CallAPI(url, headers) {
    ; Using PowerShell as bridge for HTTP calls
    ; (Alternative: embed Curl.exe or use WinHTTP COM object)

    ps_cmd := 'powershell -NoProfile -Command "'
            . '$headers = @{Authorization=''Bearer admin_token_2026''}; '
            . '$response = Invoke-WebRequest -Uri ''' . url . ''' -Method GET -Headers $headers -ErrorAction Stop; '
            . '$response.Content"'

    shell := ComObjCreate("WScript.Shell")
    exec := shell.Exec(ComSpec " /c " ps_cmd)
    result := exec.StdOut.ReadAll()

    ; Parse JSON response
    try {
        ; Simple JSON parsing (for production, use proper JSON library)
        if (InStr(result, "started"))
            return {status: "started", duration_min: 0}
        else if (InStr(result, "stopped")) {
            ; Extract duration if present
            return {status: "stopped", duration_min: ExtractDuration(result)}
        } else
            return {status: "error", error: result}
    } catch
        return {status: "error", error: "Invalid API response"}
}

; Helper: Extract duration from response
ExtractDuration(json_str) {
    ; Simple extraction: look for "duration_min": NNN
    pattern := '"duration_min"\s*:\s*(\d+)'
    if (RegExMatch(json_str, pattern, match))
        return match[1]
    return 0
}

; Helper: Get project name from ID
GetProjectName(project_id) {
    names := Map(
        13, "Stan Pro",
        14, "Stan Perso",
        19, "Divers",
        20, "CCI90",
        21, "ISO27001",
        22, "CapCyber",
        23, "Autre1",
        24, "Autre2"
    )
    return names.Has(project_id) ? names[project_id] : "Project #" . project_id
}

; Toast notification function
ShowToast(title, message, color := "0x28a745") {
    ; Create a semi-transparent overlay
    ; For production, use third-party notification library (e.g., Lib/Toast.ahk)

    ; Simple approach: MsgBox (replace with proper Toast later)
    ; MsgBox(title . "`n" . message)

    ; Better: Use ToolTip (auto-dismiss after 3 seconds)
    ToolTip(title . "`n" . message)
    SetTimer(() => ToolTip(), 3000)  ; Auto-dismiss after 3s
}

; Status bar script info
StatusMsg() {
    msg := "Pointage Stan v2.0 (XKeys)`n"
        . "F13: Stan Pro | F14: Stan Perso | F15: Divers`n"
        . "ESC: Stop`n"
        . "Current: " . (current_project ? GetProjectName(current_project) : "None")
        . " (" . current_status . ")"
    return msg
}

; Ctrl+Alt+S: Show status
^!s::MsgBox(StatusMsg())

; Tray menu
A_TrayMenu.Add()
A_TrayMenu.Add("Show Status`tCtrl+Alt+S", MenuHandler)
A_TrayMenu.Add("Configuration", MenuHandler)
A_TrayMenu.Add()
A_TrayMenu.Add("Exit", MenuHandler)

MenuHandler(ItemName, ItemID, Menu) {
    switch ItemName {
        case "Show Status":
            MsgBox(StatusMsg())
        case "Configuration":
            Run("notepad D:\xkeys_pointage_stan.ahk")
        case "Exit":
            ExitApp()
    }
}

; Auto-start notification
ShowToast("✅ Pointage Stan", "Ready (XKeys 24)", "0x28a745")
