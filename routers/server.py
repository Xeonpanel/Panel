import flask, requests, json

from __main__ import app, sqlquery

from waitress import serve

@app.route("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in sqlquery("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = sqlquery("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/server.html", title="Console", sqlquery=sqlquery, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/files")
def server_files(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            return flask.render_template("/server/files.html", title="File Manager", sqlquery=sqlquery, serverid=serverid, requests=requests, json=json)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/configuration")
def server_configuration(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in sqlquery("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = sqlquery("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/configuration.html", title="Configuration", sqlquery=sqlquery, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")