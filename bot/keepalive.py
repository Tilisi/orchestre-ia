"""
🖥️ KEEP-ALIVE : empêche le bot cloud de s'endormir
===================================================
Render (gratuit) endort les services après 15 min sans
trafic entrant. Ce petit serveur web répond "OK" aux
pings d'UptimeRobot, ce qui maintient le bot éveillé 24/7.

Il tourne dans un thread séparé, en parallèle du bot.
"""

import threading
from flask import Flask

app = Flask(__name__)


@app.route("/")
def sante():
    """Endpoint de santé : répond OK aux pings."""
    return "OK - Orchestre IA bot en ligne", 200


@app.route("/health")
def health():
    """Alias pour les health checks."""
    return {"status": "ok", "bot": "orchestre-ia"}, 200


def demarrer_keepalive(port=10000):
    """Lance le serveur keep-alive dans un thread daemon."""
    serveur = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False),
        daemon=True,
    )
    serveur.start()
    return serveur
