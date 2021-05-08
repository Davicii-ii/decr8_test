from pyrogram import Client

api_id = 314504
api_hash = "8c64c308e6f0186d495ae1e92a1c228d"

app = Client("decr8_win8", api_id=api_id, api_hash=api_hash)

@app.on_message()
async def hello(client, message):
    await message.reply_text(f"Hello {message.from_user.mention}")

app.run()
