import flask, os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = flask.Flask("Xeonpanel", template_folder=f"themes/default")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

import routers.dashboard, routers.auth, routers.api, routers.server
import admin.settings, admin.nodes, admin.servers, admin.images, admin.users

@app.before_request
def check_maintenance():
    if os.getenv("MAINTENANCE_MODE"):
        flask.abort(503) 

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
