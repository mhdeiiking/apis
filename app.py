import pyrogram , pyromod

from pyromod import listen
from .keep import alive
from pyrogram import Client, filters, enums
p = dict(root='plugins')
x=Client(name='loclhost', api_id=15102119, api_hash='3dfdcee3e3bedad4738f81287268180f', bot_token='6172993508:AAHCBVM-QeFEb9VoHj8Kygd71TWCuoyIKwg', workers=20, plugins=p, parse_mode=enums.ParseMode.DEFAULT)
alive()
x.run()
