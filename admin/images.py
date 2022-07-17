import flask

from __main__ import app, sqlquery

@app.route("/admin/images", methods=["GET"])
def admin_images():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/images/images.html".format(app.config["THEME"]),
                title="Images",
                page="images",
                images=sqlquery("SELECT * FROM images ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/images/create", methods=["GET"])
def create_image():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/images/createimage.html".format(app.config["THEME"]),
                title="Images",
                page="images",
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/images/<imageid>/view", methods=["GET"])
def view_image(imageid):
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM images WHERE id = ?", int(imageid),).fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/images/viewimage.html".format(app.config["THEME"]),
                    title="Images",
                    page="images",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0], 
                    image=sqlquery("SELECT * FROM images WHERE id = ?", int(imageid),).fetchall()[0],
                    variables=sqlquery("SELECT * FROM variables WHERE imageid = ?", int(imageid),).fetchall(),
                )
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

