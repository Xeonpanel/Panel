from __main__ import sqlquery

sqlquery("""
    CREATE TABLE "users" (
        "id"	INTEGER UNIQUE,
        "username"	VARCHAR(255),
        "email"	VARCHAR(255),
        "password"	VARCHAR(255),
        "user_type"	VARCHAR(255),
        "api_key"	VARCHAR(255),
        PRIMARY KEY("id" AUTOINCREMENT)
    );
""")

sqlquery("""
    CREATE TABLE "servers" (
        "id"	INTEGER UNIQUE,
        "name"	VARCHAR(255),
        "ownerid"	INTEGER,
        "nodeid"	VARCHAR(255),
        "memory"	VARCHAR(255),
        "disk"	VARCHAR(255),
        "uuid"	VARCHAR(255),
        "owneremail"	VARCHAR(255),
        "start_command"	VARCHAR(255),
        "image"	VARCHAR(255),
        "nodeip"	VARCHAR(255),
        PRIMARY KEY("id" AUTOINCREMENT)
    );
""")

sqlquery("""   
    CREATE TABLE "nodes" (
        "id"	INTEGER UNIQUE,
        "name"	VARCHAR(255),
        "ip"	VARCHAR(255),
        "memory"	VARCHAR(255),
        "disk"	VARCHAR(255),
        "node_api"	VARCHAR(255),
        PRIMARY KEY("id" AUTOINCREMENT)
    );
""")

sqlquery("""   
    CREATE TABLE "settings" (
        "panel_name"	VARCHAR(255)
    );
""")

sqlquery("""
    CREATE TABLE "images" (
        "id"	INTEGER UNIQUE,
        "name"	VARCHAR(255),
        "startup_command"	VARCHAR(255),
        "docker_image"	VARCHAR(255),
        PRIMARY KEY("id" AUTOINCREMENT)
    );
""")