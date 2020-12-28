import telebot
from telebot import types
import sqlite3

bot_token = '0' #BotFather token

with sqlite3.connect('data_vk') as con:
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM users')
    except sqlite3.OperationalError:
        cur.execute('CREATE TABLE users(user_id INTEGER, status INTEGER, token TEXT)')
if con:
    con.commit()
    con.close()

def get_users_data(user_id):
    # Creator -  @lastwek
    with sqlite3.connect('data_vk') as con:
        cur = con.cursor()
        try:
            return cur.execute(f'SELECT * FROM users WHERE user_id="{user_id}"').fetchall()[0]
        except:
            return False
    if con:
        con.commit()
        con.close()

def new_user(user_id):
    with sqlite3.connect('data_vk') as con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO users VALUES("{user_id}", "0", "token")')
    if con:
        con.commit()
        con.close()

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    keys = types.InlineKeyboardMarkup()
    keys.add(types.InlineKeyboardButton(text='Ссылка', url='https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'))
    if get_users_data(user_id) is False:
        new_user(user_id)
        # Creator  - @lastwek
        bot.send_message(user_id, 'Привет, введи ссылку в чат, чтобы запустить АвтоСтатус. Для получения ссылки нажмите на кнопку ниже, потом в браузере кнопку "Разрешить"\nПосле чего отправьте ссылку в чат', reply_markup=keys)
    else:
        bot.send_message(user_id, 'Привет, введи ссылку в чат, чтобы запустить АвтоСтатус. Для получения ссылки нажмите на кнопку ниже, потом в браузере кнопку "Разрешить"\nПосле чего отправьте ссылку в чат', reply_markup=keys)


@bot.message_handler(content_types=['text'])
def get_token(message):
    try:
        token = message.text.split('=')[1].split('&')[0]
        status_stop = types.InlineKeyboardMarkup()
        status_stop.add(types.InlineKeyboardButton(text='Остановить АвтоСтатус', callback_data='stop'))
        with sqlite3.connect('data_vk') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE users SET token="{token}" WHERE user_id="{message.chat.id}"')
            cur.execute(f'UPDATE users SET status="1" WHERE user_id="{message.chat.id}"')
        if con:
            con.commit()
            con.close()
        bot.send_message(message.chat.id, 'АвтоСтатус будет установлен в течении двух минут\nДля остановки АвтоСтатуса нажмите на кнопку ниже, после чего сотрите статус на своей странице', reply_markup=status_stop)
    except:
        user_id = message.chat.id
        keys = types.InlineKeyboardMarkup()
        # Creator - @lastwek
        keys.add(types.InlineKeyboardButton(text='Ссылка', url='https://oauth.vk.com/authorize?client_id=7614641&scope=1024&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'))
        if get_users_data(user_id) is False:
            new_user(user_id)
            bot.send_message(user_id, 'Привет, введи ссылку в чат, чтобы запустить АвтоСтатус. Для получения ссылки нажмите на кнопку ниже, потом в браузере кнопку "Разрешить"\nПосле чего отправьте ссылку в чат', reply_markup=keys)
        else:
            bot.send_message(user_id, 'Привет, введи ссылку в чат, чтобы запустить АвтоСтатус. Для получения ссылки нажмите на кнопку ниже, потом в браузере кнопку "Разрешить"\nПосле чего отправьте ссылку в чат', reply_markup=keys)
    
@bot.callback_query_handler(func=lambda call: True)
def call(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'stop':
        with sqlite3.connect('data_vk') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE users SET token="token" WHERE user_id="{chat_id}"')
            cur.execute(f'UPDATE users SET status="0" WHERE user_id="{chat_id}"')
        if con:
            # Creator -  @lastwek
            con.commit()
            con.close()
        keys = types.InlineKeyboardMarkup()
        keys.add(types.InlineKeyboardButton(text='Ссылка', url='https://oauth.vk.com/authorize?client_id=7614641&scope=1024&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Привет, введи ссылку в чат, чтобы запустить АвтоСтатус. Для получения ссылки нажмите на кнопку ниже, потом в браузере кнопку "Разрешить"\nПосле чего отправьте ссылку в чат', reply_markup=keys) 

print('BOT started')

bot.polling(none_stop=True)
