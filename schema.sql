CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"email"	VARCHAR(255),
	"password"	VARCHAR(255),
	"token"	VARCHAR(255),
	"user_type"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "settings" (
	"panel_name"	VARCHAR(255),
	"panel_logo"	VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "nodes" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"memory"	VARCHAR(255),
	"disk"	VARCHAR(255),
	"ip"	VARCHAR(255),
	"token"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "servers" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"memory"	VARCHAR(255),
	"disk"	VARCHAR(255),
	"ip_port"	VARCHAR(255),
	"node_id"	VARCHAR(255),
	"image_id"	VARCHAR(255),
	"owner_id"	VARCHAR(255),
	"suspended"	INTEGER,
	"uuid"	VARCHAR(255),
	"startup"	VARCHAR(255),
	"image"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "images" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"startup"	VARCHAR(255),
	"image"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "images" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"startup"	VARCHAR(255),
	"image"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "image_variables" (
	"id"	INTEGER UNIQUE,
	"name"	VARCHAR(255),
	"variable"	VARCHAR(255),
	"image_id"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "server_variables" (
	"id"	INTEGER UNIQUE,
	"data"	VARCHAR(255),
	"image_id"	VARCHAR(255),
	"server_id"	VARCHAR(255),
	"variable_id"	VARCHAR(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "settings" (panel_name) VALUES ("Xeonpanel");