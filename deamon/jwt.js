const crypto = require("crypto");
const jwt = require("jsonwebtoken");
const { Token } = require("./models");

async function requireJWT(req, res, next) {
    const jwtToken = req.headers["x-access-token"];

    if (!jwtToken) {
        return res.json({ success: false, error: "Unauthorized" });
    }

    try {
        const token = await Token.findAll();

        if (token.length <= 0) {
            return res.json({ success: false, error: "Internal Server Error" });
        }

        const jwtKey = token[0].jwt_key;
        const decoded = jwt.verify(jwtToken, jwtKey);
        if (!decoded.authorized) {
            return res.json({ success: false, error: "Unauthorized" });
        }
        next();
    } catch (err) {
        return res.json({ success: false, error: "Unauthorized" });
    }
};

module.exports = { requireJWT };