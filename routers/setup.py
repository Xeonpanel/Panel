import flask, os, time, sys, hashlib

from __main__ import app

@app.post("/setup/register-admin")
def setup_register_admin():
    pass

@app.get("/setup/finish")
def setup_reboot_server():
    time.sleep(1)
    exit(0)

@app.get("/setup/setup-final")
def setup_final():
    return flask.render_template(
        "/setup/setupfinal.html",
        title="Installing",
        page="setup.installing"
    )

@app.get("/setup/getting-started")
def setup_getting_started():
    return flask.render_template(
        "/setup/welcome.html",
        title="Getting Started",
        page="setup.gettingstarted"
    )

@app.get("/setup/setup-account")
def setup_account():
    return flask.render_template(
        "/setup/setupaccount.html",
        title="Setup Account",
        page="setup.setupaccount"
    )
