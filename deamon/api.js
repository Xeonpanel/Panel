const express = require("express");
const crypto = require("crypto");
const { Token } = require("./models");

const router = express.Router();

router.get("/jwt", async (req, res) => {
    const randomBytes = crypto.randomBytes(24).toString("hex");
    const publicKey = await Token.findOne().public_key;

    const encryptedBytes = crypto.publicEncrypt(publicKey, Buffer.from(randomBytes));
    const encryptedText = encryptedBytes.toString("base64");

    return res.send(encryptedText);
});

module.exports = router;