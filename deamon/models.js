const { Sequelize } = require("sequelize");

const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "./db.sqlite3",
    logging: false
});

const Token = sequelize.define("token", {
    public_key: {
        type: Sequelize.STRING,
        allowNull: false
    }
});

Token.sync();

module.exports = { Token }