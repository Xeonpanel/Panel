const express = require("express");
const crypto = require("crypto");
const { Token } = require("./models");
const jwt = require("jsonwebtoken");
const fs = require("fs");

const router = express.Router();

router.get("/jwt", async (req, res) => {
    const randomBytes = crypto.randomBytes(24).toString("hex");
    req.session.randomBytes = randomBytes;
    const token = await Token.findAll();

    if (token.length <= 0) {
        return res.status(500).send("Internal Server Error");
    }

    const publicKey = token[0].public_key;

    const encryptedBytes = crypto.publicEncrypt(publicKey, Buffer.from(randomBytes));
    const encryptedText = encryptedBytes.toString("base64");

    return res.send(encryptedText);
});

router.post("/jwt", async (req, res) => {
    const { randomBytes } = req.session;
    const { decryptedText } = req.body;

    if (!randomBytes || !decryptedText) {
        return res.status(400).send("Bad Request");
    }

    if (randomBytes !== decryptedText) {
        return res.status(401).send("Unauthorized");
    }

    const jwtToken = jwt.sign({ authorized: true }, fs.readFileSync("./ssl/key.pem"), { algorithm: "RS256" });
    res.send(jwtToken);
});

module.exports = router;