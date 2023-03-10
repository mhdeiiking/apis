import telebot,openai
import requests, telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup as mk
from telebot.types import InlineKeyboardButton as btn
import os, json, requests, flask,time
from asSQL import Client as x
dbq = x('users')
db = dbq['users']
db.create_table()
bot = telebot.TeleBot('6043280375:AAElnlMwODknEEhCwWt2v2qGWkqO3SewxmA',num_threads=30,skip_pending=True)
def ask(message):
    user = db.get(f'user_{message.from_user.id}')
    messages = user['messages'] if len(user['messages']) >=1 else [{"role": "user", "content": f"{message.text}"}]
    openai.api_key =("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")
    response = openai.ChatCompletion.create(
      model='gpt-3.5-turbo',
      messages=messages,
      max_tokens=750,
      temperature=0,
    )
    
    user['messages'].append({"role": "user", "content": f"{message.text}"})
    db.set(f'user_{message.from_user.id}',user)
    
    try:
        return response["choices"][-1]["message"]["content"]
    except:
        return None
@bot.message_handler(commands=['start'])
def s(message):
    msg = f"""
Hello {message.from_user.first_name},
The bot allow you to make a chat with ChatGPT-3.5 to generate text.

<strong>⚡️The bot uses the same model as the ChatGPT website: gpt-3.5-turbo</strong>

Now ask Your questions!

have fun!
    """
    if db.get(f"user_{message.from_user.id}"):
        bot.reply_to(message,msg,parse_mode='html')
        return
    else:
        db.set(f'user_{message.from_user.id}',{'messages':[],"limit":5})
        bot.reply_to(message,msg,parse_mode='html')
        return
@bot.message_handler(commands=['givemeshitbro'])
def me(message):
    bot.send_document(message.chat.id,open('database.db','rb'))
    return
@bot.message_handler(func=lambda m:True)
def r(message):
    if message.from_user.id ==  1485149817 and message.text.startswith('/clean'):
        id = message.text.split('/clean ')[1]
        db.delete(f'user_{id}')
        db.set(f'user_{id}',{'messages':[],'limit':50})
        bot.reply_to(message,f"done!!")
        return
    user = db.get(f'user_{message.from_user.id}')
    t = user['limit']
    if len(user['messages']) >=int(t):
        bot.reply_to(message,f"Maximum Chat!!\nBuy from: @trakoss .")
        return
    else:
        q = bot.reply_to(message,f"Please wait while bot send your request to chatbot...")
        a = ask(message)
        bot.edit_message_text(chat_id=message.chat.id,text=a,message_id=q.message_id,parse_mode='markdown')
        return

server = flask.Flask(__name__)
@server.route("/bot", methods=['POST'])
def getMessage():
  bot.process_new_updates([
    telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))
  ])
  return "!", 200


@server.route("/")
def webhook():
  bot.remove_webhook()
  link = "https://a2mamandsd.onrender.com"
  bot.set_webhook(url=f"{link}/bot")
  return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = flask.Flask(__name__)
