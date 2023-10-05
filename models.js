const { Sequelize } = require("sequelize");

const sequelize = new Sequelize("sqlite://db.sqlite3", {logging: false});

const User = sequelize.define("User", {
    id: {
        type: Sequelize.STRING,
        primaryKey: true,
        defaultValue: Sequelize.UUIDV4
    },
    email: Sequelize.STRING,
    password: Sequelize.STRING,
    username: Sequelize.STRING,
    is_admin: {
        type: Sequelize.BOOLEAN,
        defaultValue: false
    }
});

const Node = sequelize.define("Node", {
    id: {
        type: Sequelize.STRING,
        primaryKey: true,
        defaultValue: Sequelize.UUIDV4
    },
    ip: Sequelize.STRING,
    ssl_enabled: {
        type: Sequelize.BOOLEAN,
        defaultValue: true
    },
    private_key: Sequelize.STRING,
    public_key: Sequelize.STRING,
    port: Sequelize.INTEGER,
    name: Sequelize.STRING
});

const DockerImage = sequelize.define("DockerImage", {
    id: {
        type: Sequelize.STRING,
        primaryKey: true,
        defaultValue: Sequelize.UUIDV4
    },
    name: Sequelize.STRING,
    dockerfile: Sequelize.STRING
});

User.sync();
Node.sync();
DockerImage.sync();

module.exports = { User, Node, DockerImage };