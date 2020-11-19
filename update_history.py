from pyrogram import Client

import os, logging, json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

##############################################
api_id = 314504
api_hash = "8c64c308e6f0186d495ae1e92a1c228d"
##############################################

decr8 = -1001280481543

with Client("history_update", api_id, api_hash) as app:
    logging.info("Getting history.")
    d = {
        msg.audio.file_name: msg.message_id
        for msg in (app.iter_history(decr8))
        if msg.audio
        if not None
    }
    logging.info("Done.")
    with open(
            "/home/ayuko/decr8/res/decr8_data.json",
            "w",
            encoding="utf-8"
    ) as f:
        logging.info("Writing history to json file.")
        json.dump(d, f)
        logging.info("Done.")
