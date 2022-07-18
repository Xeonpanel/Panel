import flask, os, sqlite3, logging

logging.basicConfig(filename="logs/log.txt", level=logging.DEBUG)
app = flask.Flask("Xeonpanel", template_folder="themes/default")
app.config["DATABASE_FILE"] = "database.db"
app.config["MAINTENANCE_MODE"] = False
app.config["SECRET_KEY"] = "test"

# Do not change this line
# This can give an attacker access on your panel
if not os.path.exists("database.db"):
    import routers.setup

def sqlquery(sql, *parameter):
    conn = sqlite3.connect(app.config["DATABASE_FILE"], check_same_thread=False)
    cursor = conn.cursor()
    data = cursor.execute(sql, (parameter)).fetchall()
    conn.commit()
    return data

import routers.dashboard, routers.auth, routers.api, routers.server
import admin.settings, admin.nodes, admin.servers, admin.images, admin.users

@app.before_request
def maintenance():
    if app.config["MAINTENANCE_MODE"]:
        flask.abort(503) 

@app.before_first_request
def setup():
    if not os.path.isfile("database.db"):
        return flask.redirect("/setup/getting-started")

@app.errorhandler(503)
def error_503(error):
    return flask.render_template("/errors/503.html") 

@app.errorhandler(404)
def error_404(error):
    return flask.render_template("/errors/404.html") 

@app.errorhandler(401)
def error_401(error):
    return flask.render_template("/errors/401.html") 

@app.route("/logout", methods=["GET"])
def logout():
    if flask.session:
        if flask.request.args["csrf"] == flask.session["csrf_token"]:
            flask.session.clear()
        return flask.redirect("/")

@app.route("/", methods=["GET"])
def main():
    if flask.session:
        return flask.redirect("/dashboard")
    else:
        return flask.redirect("/login")

app.run(debug=True, host="0.0.0.0", port=80)