// ==UserScript==
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

  // Créer la barre flottante
  const barre = document.createElement('div');
  barre.id = 'barre-pointage-kimai';
  barre.style.cssText = `
    display: none;
    position: fixed;
    top: 10px;
    left: 10px;
    background: white;
    border: 2px solid #333;
    border-radius: 8px;
    padding: 12px 16px;
    z-index: 99999;
    min-width: 220px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-family: Arial, sans-serif;
  `;

  barre.innerHTML = `
    <div style="font-size: 11px; color: #666; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;">
      ⏱️ Pointage en cours
    </div>
    <div style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 8px; padding-left: 4px; border-left: 4px solid #999;" id="nom-activite">
      Aucun pointage
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
      <div style="font-size: 28px; font-weight: bold; color: #dc3545; font-family: 'Courier New', monospace;" id="chrono">
        00:00
      </div>
      <a href="#" id="btn-stop-kimai" style="background: #dc3545; color: white; padding: 8px 12px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: bold; cursor: pointer;">
        STOP
      </a>
    </div>
  `;

  document.body.appendChild(barre);

  // Fonction pour mettre à jour la barre
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
    } catch (e) {
      console.error('Erreur lors de la mise à jour du pointage:', e);
    }
  }

  // Bouton STOP
  document.getElementById('btn-stop-kimai').addEventListener('click', async function(e) {
    e.preventDefault();
    try {
      await fetch('http://192.168.1.15:8059/stop/stan');
      updateBarre();
    } catch (e) {
      console.error('Erreur lors de l\'arrêt du pointage:', e);
    }
  });

  // Mise à jour initiale et rafraîchissement toutes les 500ms
  updateBarre();
  setInterval(updateBarre, 500);
})();
