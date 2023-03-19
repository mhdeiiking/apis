import pyrogram , pyromod

from pyromod import listen
from pyrogram import Client as app, filters, enums
@app.on_message(filters.text)
async def lo(app, msg):
  await msg.reply(msg.text)
