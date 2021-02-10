from pyrogram import Client

app = Client("decr8")

@app.on_message()
async def hello(client, message):
    await message.reply_text(f"Hello {message.from_user.mention}")

app.run()
