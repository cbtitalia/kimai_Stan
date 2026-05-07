// ==UserScript==
// @name         Kimai - Couleurs Activités (24 teintes)
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Affiche les 24 couleurs pastel des activités dans Kimai
// @author       Claude
// @match        http://192.168.1.15:8055/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Map: activity_id → couleur hex
    const ACTIVITY_COLORS = {
        // Presence (vert)
        14: "#C8E6C9",
        15: "#A5D6A7",
        16: "#81C784",
        17: "#66BB6A",
        // Absences (rouge/rose)
        18: "#EF9A9A",
        19: "#E57373",
        20: "#F48FB1",
        21: "#EC407A",
        // Homelab (bleu)
        22: "#B3E5FC",
        23: "#81D4FA",
        24: "#4FC3F7",
        25: "#29B6F6",
        // Coding (orange)
        26: "#FFCC80",
        27: "#FFB74D",
        28: "#FFA726",
        29: "#FF7043",
        // Obsidian (jaune)
        30: "#FFF9C4",
        31: "#FFF59D",
        32: "#FFF176",
        33: "#FFEE58",
        // Velo (turquoise)
        34: "#B2DFDB",
        35: "#80CBC4",
        36: "#4DB6AC",
        37: "#26A69A"
    };

    function getActivityColor(activityId) {
        return ACTIVITY_COLORS[activityId] || "#CCCCCC";
    }

    function colorizeTimesheets() {
        // Cibler les lignes de timesheet
        const rows = document.querySelectorAll('tr[data-id]');
        rows.forEach(row => {
            const activityCell = row.querySelector('td:nth-child(3)');
            if (!activityCell) return;

            const actLink = activityCell.querySelector('a[href*="/activity/"]');
            if (!actLink) return;

            const match = actLink.href.match(/\/activity\/(\d+)/);
            if (!match) return;

            const activityId = parseInt(match[1]);
            const color = getActivityColor(activityId);

            // Colorer le fond de la ligne
            row.style.borderLeft = `4px solid ${color}`;
            row.style.backgroundColor = color + "22"; // Fond transparent

            // Colorer la cellule activité
            activityCell.style.color = color;
            activityCell.style.fontWeight = "bold";
        });
    }

    function colorizeActivitySelectors() {
        // Colorer les options de sélection d'activité
        const selects = document.querySelectorAll('select[name*="activity"]');
        selects.forEach(select => {
            const options = select.querySelectorAll('option');
            options.forEach(option => {
                const match = option.value.match(/(\d+)/);
                if (match) {
                    const activityId = parseInt(match[1]);
                    const color = getActivityColor(activityId);
                    option.style.background = `linear-gradient(${color}, ${color})`;
                    option.style.color = "#000";
                }
            });
        });
    }

    function colorizeActivityBadges() {
        // Colorer les "badges" activités
        const badges = document.querySelectorAll('[class*="activity"], [class*="label"]');
        badges.forEach(badge => {
            const text = badge.textContent;
            // Chercher l'ID dans le href s'il existe
            const link = badge.closest('a');
            if (link) {
                const match = link.href.match(/\/activity\/(\d+)/);
                if (match) {
                    const activityId = parseInt(match[1]);
                    const color = getActivityColor(activityId);
                    badge.style.backgroundColor = color;
                    badge.style.color = "#333";
                    badge.style.fontWeight = "bold";
                }
            }
        });
    }

    function colorizeGraphs() {
        // Chercher les graphiques et les colorer par activité
        // (Kernal dépend de la structure du DOM de Kimai)
        const chartBars = document.querySelectorAll('[role="img"][aria-label*="activity"], .chart-bar, svg rect');
        chartBars.forEach(bar => {
            const label = bar.getAttribute('aria-label') || bar.textContent || '';
            // Essayer de trouver l'ID d'activité dans le label
            const match = label.match(/activity[^0-9]*(\d+)/i) || label.match(/(\d+)/);
            if (match) {
                const activityId = parseInt(match[1]);
                if (ACTIVITY_COLORS[activityId]) {
                    const color = getActivityColor(activityId);
                    bar.style.fill = color;
                    bar.setAttribute('style', `fill: ${color} !important;`);
                }
            }
        });
    }

    // Appliquer les couleurs au chargement
    colorizeTimesheets();
    colorizeActivitySelectors();
    colorizeActivityBadges();
    colorizeGraphs();

    // Observer pour les changements dynamiques
    const observer = new MutationObserver(() => {
        colorizeTimesheets();
        colorizeActivitySelectors();
        colorizeActivityBadges();
        colorizeGraphs();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: false
    });

    console.log("✅ Kimai Couleurs Activités activé - 24 teintes pastel");

})();
