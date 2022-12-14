import flask, os, sqlite3, json

app = flask.Flask("Xeonpanel", template_folder="themes/{}".format(json.loads(open("config.json", "r").read())["theme"]))
app.config["SECRET_KEY"] =  json.loads(open("config.json", "r").read())["secret"]

def query(sql, *parameter):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    data = cursor.execute(sql, (parameter)).fetchall()
    conn.commit()
    return data

if not os.path.isfile("database.db"):
    import routers.setup
else:
    @app.get("/setup/finish")
    def setup_reboot_server():
        return flask.redirect("/")

import routers.dashboard, routers.auth, routers.api, routers.server
import admin.settings, admin.nodes, admin.servers, admin.images, admin.users

@app.before_request
def maintenance():
    if os.getenv("MAINTENANCE_MODE"):
        flask.abort(503) 
    else:
        if not "/setup" in flask.request.path:
            if not "/static" in flask.request.path:
                if not os.path.isfile("database.db"):
                    return flask.redirect("/setup/getting-started")
        elif "/setup/reboot" in flask.request.path:
            return flask.redirect("/")

@app.errorhandler(503)
def error_503(error):
    return flask.render_template("/errors/503.html") 

@app.errorhandler(404)
def error_404(error):
    return flask.render_template("/errors/404.html") 

@app.errorhandler(401)
def error_401(error):
    return flask.render_template("/errors/401.html") 

@app.get("/logout")
def logout():
    if flask.session:
        if flask.request.args["csrf"] == flask.session["csrf_token"]:
            flask.session.clear()
        return flask.redirect("/")

@app.get("/")
def main():
    if flask.session:
        return flask.redirect("/dashboard")
    else:
        return flask.redirect("/login")

if os.getenv("DEVELOPMENT_MODE"):
    app.run(debug=True, host="0.0.0.0", port=5000)
else:
    app.run(debug=False, host="0.0.0.0", port=5000)
