import flask, sqlite3, requests, os, sys, json

app = flask.Flask("Xeon Panel")

def sqlquery(sql, *parameter):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    data = cursor.execute(sql, (parameter))
    conn.commit()
    return data

import routes.api, routes.auth, routes.dashboard, routes.setup, routes.server, routes.admin

for addon in os.listdir("addons/"):
    if not addon == "__pycache__":
        try:
            __import__("addons.{}".format(os.path.splitext(addon)[0]))
            print("Loaded {}".format(addon))
        except Exception:
            pass

@app.route("/logout", methods=["GET"])
def logout():
    if flask.request.args["csrf"] == flask.session["csrf_token"]:
        flask.session.clear()
    return flask.redirect("/")

@app.route("/", methods=["GET"])
def main():
    if not os.path.isfile("database.db"):
        return flask.redirect("/setup/getting-started")
    else:
        if flask.session:
            return flask.redirect("/dashboard")
        else:
            return flask.redirect("/login")

app.config["THEME"] = json.loads(open("config.json", "r").read())["theme"]
app.config["SECRET_KEY"] = os.urandom(500).hex()
app.run(debug=True, host="0.0.0.0", port=80)