import flask

from __main__ import app, sqlquery

@app.route("/admin/images", methods=["GET"])
def images():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/images/images.html", title="Images", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/images/create", methods=["GET"])
def create_image():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/images/createimage.html", title="Images", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/images/<imageid>/view", methods=["GET"])
def view_image(imageid):
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(sqlquery("SELECT * FROM images WHERE id = ?", imageid)):
                return flask.render_template("/admin/images/viewimage.html", title="Images", sqlquery=sqlquery, imageid=imageid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")