import telebot
import cfg
import urllib
import os
import sqlite3
import subprocess
from telebot import types

bot = telebot.TeleBot(cfg.token)



'''#########################################################################
                        ANSWERS AND OTHER
#########################################################################'''


    ############# START COMMAND ################
@bot.message_handler(commands=['start'])
def start(message):
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    bot.send_message(message.chat.id, hi_message)


    ############# ADMIN LIST ################
@bot.message_handler(commands=['userlist'])
def userlist(message):
    userid = str(message.from_user.id)
    conn = sqlite3.connect('pplids.sqlite')
    sql = conn.cursor()
    sql.execute("SELECT Admin FROM ppls WHERE ID = %s" % userid)
    if sql.fetchone()[0] == 'True':
        bot.send_message(message.chat.id, 'Ok')
        sql.execute("SELECT * FROM ppls")
        res = sql.fetchall()
        for row in res:
            bot.send_message(message.chat.id, row)

    elif sql.fetchone()[0] == 'False':
        bot.send_message(message.chat.id, 'You are not admin')
    else:
        bot.send_message(message.chat.id, 'Some problems with access')




    ############# HELP COMMAND ################
@bot.message_handler(commands=['help'])
def idk(message):
    bot.send_message(message.chat.id, 'Have a question or suggestions? - /start or write to this guy @tilliknow')


    ############# IF PHOTO ################
@bot.message_handler(content_types=['photo'])
def issue(message):
    bot.send_message(message.chat.id, 'Am i joke to you?')


############# NOT SUPPORTS ################
def wrong_extension(file_extension, message):
    wrong_message = 'Sorry but '+file_extension+' type file doesnt supports. Try other filetype'
    bot.send_message(message.chat.id, wrong_message)


############# TOO BIG ################
def toobig(message):
    bot.send_message(message.chat.id, 'File is too big :) There\'s no way')


############# NEED TO REGISTER ################
def notalloweduser(message):
    bot.send_message(message.chat.id, 'You need to login IRL :)')
    DB(message)





'''#########################################################################
                            CHECK AND DOWNLOAD
#########################################################################'''


document_id = ''
mssg_id = ''
copy = 1



############# FILE CHECK ################
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    if message.document.file_size >= 20971520:                 #Is file too big?
        toobig(message)
    conn = sqlite3.connect('/telebot/pplids.sqlite')
    sql = conn.cursor()
    sqlstr = "SELECT * FROM ppls WHERE ID = %s"
    userid = str(message.from_user.id)
    sql.execute(sqlstr % userid)
    if sql.fetchone() is None:
        notalloweduser(message)
    else:
        global document_id
        global mssg_id
        mssg_id = message.message_id
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        useless, file_extension = os.path.splitext(file_info.file_path)
        if file_extension not in cfg.allowedfiles:            #Is file unsupported
            wrong_extension(file_extension, message)
        else:
            hope(message)                                              #User opinion


def hope(message):
    def areusure(message):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='No', callback_data='no')
        keyboard.add(key_no)
        global copy
        not_one_and_how = 'Not ' + str(copy)
        key_not_one= types.InlineKeyboardButton(text=not_one_and_how, callback_data='not_one')
        keyboard.add(key_not_one)
        str4ka= 'Are you sure you want to print ' + str(copy) + ' copy'
        bot.send_message(message.chat.id, text=str4ka, reply_markup=keyboard)
    def call():
        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if call.data == 'yes':
                download(call.message.chat.id)
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, 'Ok then')
                pass
            elif call.data == 'not_one':
                bot.send_message(call.message.chat.id, 'And how much?')
                bot.register_next_step_handler(message, how_much)
                pass
    areusure(message)
    call()


############# HOW MUCH ################
def how_much(message):
    global copy
    try:
        copy = int(message.text)
        if copy > 20 or copy < 1:
            bot.send_message(message.chat.id, 'Wrong')
            copy = 1
    except Exception:
        bot.send_message(message.chat.id, 'Write in numbers please')
    hope(message)



############# DOWNLOAD ################
def download(userid):
    global document_id
    global mssg_id
    global copy
    file_info = bot.get_file(document_id)
    useless, file_extension = os.path.splitext(file_info.file_path)
    file_name = str(copy) + '.' + str(userid) + '.' + str(mssg_id)
    file_path = '/telebot/documents/' + file_name + str(file_extension)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_path)
    bot.send_message(userid, 'Success. You did it')
    copy = 1
    printthat(file_path, file_name)



############# COPY ################
def printthat(file_path, file_name):
    sum = file_path.split('.')
    folder = sum[0]
    quantity = folder[10:]
    cmd = ['lowriter', '--convert-to', 'pdf', '--outdir', '/telebot/PDF', file_path]
    traceback = subprocess.run(cmd, check=True)
    if traceback.returncode == 0:
        print('good good')
        pdf_file_path = '/telebot/PDF/' + file_name + '.pdf'
        traceback = subprocess.run(['pdfinfo', pdf_file_path], stdout=subprocess.PIPE, encoding='utf-8')
        print(traceback)
    else:
        print('not good yet:', traceback)



############# LOG ################
def DB(message):
    log = open('DB.txt', 'a')
    newstr = str(message.from_user.id) + '  ' + str(message.message_id) + '  ' + '@' + str(message.from_user.username) +  '  ' + str(message.from_user.first_name) + '  ' + str(message.from_user.last_name)
    log.write(newstr+'\n')
    log.close()


bot.polling()
