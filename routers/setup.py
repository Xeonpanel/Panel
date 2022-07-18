import flask, os, time, sys, sqlite3, hashlib

from __main__ import app

@app.route("/setup/register-admin", methods=["POST"])
def setup_register_admin():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.executescript(open("schema.sql").read())
    conn.commit()
    cursor.execute("INSERT INTO settings (panel_name) VALUES ('Xeonpanel')")
    cursor.execute(
        "INSERT INTO users (name, email, password, token, user_type) VALUES (?, ?, ?, ?, ?)",
        (
            flask.request.form.get("username"),
            flask.request.form.get("email"),
            hashlib.sha256(
                flask.request.form.get("password").encode("utf-8")
            ).hexdigest(),
            os.urandom(50).hex(),
            "administrator"
        )
    )
    conn.commit()
    cursor.execute(
        "INSERT INTO images (name, startup, image) VALUES ('Python bot', 'python -m pip install -U [[PIP_PACKAGES]]; python /home/container/[[PYTHON_FILE]]', 'python:latest')"
    )
    conn.commit()
    cursor.execute(
        "INSERT INTO image_variables (name, variable, image_id) VALUES ('Python file', 'PYTHON_FILE', '1')"
    )
    conn.commit()
    cursor.execute(
        "INSERT INTO image_variables (name, variable, image_id) VALUES ('Python packages', 'PIP_PACKAGES', '1')"
    )
    conn.commit()
    #
    cursor.execute(
        "INSERT INTO images (name, startup, image) VALUES ('Nodejs bot', 'npm install [[NODE_PACKAGES]]; node /home/container/[[NODE_FILE]]', 'node:latest')"
    )
    conn.commit()
    cursor.execute(
        "INSERT INTO image_variables (name, variable, image_id) VALUES ('Node file', 'NODE_FILE', '2')"
    )
    conn.commit()
    cursor.execute(
        "INSERT INTO image_variables (name, variable, image_id) VALUES ('Node packages', 'NODE_PACKAGES', '2')"
    )
    conn.commit()
    return flask.redirect("/setup/setup-final")

@app.route("/setup/reboot", methods=["GET"])
def setup_reboot_server():
    time.sleep(1)
    os.execv(sys.executable, ["python"] + sys.argv)

@app.route("/setup/setup-final", methods=["GET"])
def setup_final():
    return flask.render_template(
        "/setup/setupfinal.html",
        title="Installing"
    )

@app.route("/setup/getting-started", methods=["GET"])
def setup_getting_started():
    return flask.render_template(
        "/setup/welcome.html",
        title="Getting Started"
    )

@app.route("/setup/setup-account", methods=["GET"])
def setup_account():
    return flask.render_template(
        "/setup/setupaccount.html",
        title="Setup Account"
    )