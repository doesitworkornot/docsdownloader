import telebot                      #Main Telegram Library
import cfg                          #Import token and some vars
import urllib                       #To download with URLs
import os                           #To have a good split
import sqlite3                      #Typical DB
import subprocess                   #Can write in cmd line and get output
from telebot import types           #Inline Keyboard

bot = telebot.TeleBot(cfg.token)



'''#########################################################################
                        COMMANDS
#########################################################################'''



    ############# START COMMAND ################
@bot.message_handler(commands=['start'])            #When user writes /start to bot
def start(message):
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is checking all files and printing them in the scool. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored. Nothing personal :) Thats Telegram restriction. \n     You can print only 20 pages of paper, so check it before sending the file and make sure that you understand what are you printing.\n Before you need to register that helps us to know who are using scool paper. To start you just need to send file to bot thats all. To see commands list send /help  \n \nI hope you'll enjoy"
    bot.send_message(message.chat.id, hi_message)


    ############# ADMIN LIST ################
@bot.message_handler(commands=['userlist'])         #When user writes /uesrlist to bot
def userlist(message):
    userid = str(message.from_user.id)
    conn = sqlite3.connect('pplids.sqlite')
    sql = conn.cursor()
    sql.execute("SELECT Admin FROM ppls WHERE ID = %s" % userid)
    if sql.fetchone()[0] == 'True':                 #Admin check with DB
        bot.send_message(message.chat.id, 'Ok there is names of users soo')
        sql.execute("SELECT * FROM ppls")
        res = sql.fetchall()
        for row in res:
            bot.send_message(message.chat.id, row)
    elif sql.fetchone()[0] == 'False':
        bot.send_message(message.chat.id, 'You are not admin. So make your bet to solve this problem')
    else:
        bot.send_message(message.chat.id, 'Some problems with access idk what to do')


    ############# HELP COMMAND ################
@bot.message_handler(commands=['help'])         #When user writes /help to bot
def idk(message):
    bot.send_message(message.chat.id, 'Soo.. Hello there! Lets strart with /start \n /start - command that have a description inside can make you understand bot destination \n /help - now you here \n /userlist - thats showing names of registred users ADMIN STATUS REQUIRED \n Have a suggestions or need to add new type of file? write to this guy @tilliknow')



'''#########################################################################
                        ANSWERS TO DEAR USER
#########################################################################'''



    ############# IF PHOTO ################
@bot.message_handler(content_types=['photo'])           #When user sends photo to bot
def issue(message):
    bot.send_message(message.chat.id, 'Am i joke to you? You should send me FILE')


############# NOT SUPPORTS ################
def wrong_extension(file_extension, message):           #When user sends file with wrong extension
    wrong_message = 'Sorry but '+file_extension+' type file doesnt supports. Try other filetype or if you think that this is needed format you shold write to admin user'
    bot.send_message(message.chat.id, wrong_message)


############# TOO BIG ################
def toobig(message):                                    #When user sends too big file
    bot.send_message(message.chat.id, 'File is too big :) There\'s no way Telegram can\'t allow us to download this file')


############# NEED TO REGISTER ################
def notalloweduser(message):                            #When user is not registred in DB
    bot.send_message(message.chat.id, 'You need to login IRL :) Just check /start command')
    DB(message)


############# NEED TO PAY ################
def needtopay(message, available_pages):
    str = 'In your account ' + str(available_pages) + 'available pages to print left'
    bot.send_message(message.chat.id, str)



'''#########################################################################
                            CHECK SUBMIT AND DOWNLOAD
#########################################################################'''



############# GLOBAL UNITS ################
document_id = ''
mssg_id = ''
copy = 1
chat_id = ''
number_of_pages = 1
available_pages = 0
x = 1


############# FILE CHECK ################
@bot.message_handler(content_types=["document"])               #When user sends doc file to bot
def handle_docs(message):
    if message.document.file_size >= 20971520:                 #Is file too big?
        toobig(message)
    conn = sqlite3.connect('/telebot/pplids.sqlite')
    sql = conn.cursor()
    sqlstr = "SELECT * FROM ppls WHERE ID = %s"
    userid = str(message.from_user.id)
    sql.execute(sqlstr % userid)
    if sql.fetchone() is None:                              #Checking in DB is registred?
        notalloweduser(message)
    sqlstr = "SELECT AvailablePages FROM ppls WHERE ID = %s"
    sql.execute(sqlstr % userid)
    global available_pages
    available_pages = sql.fetchone()
    available_pages = ''.join(str(x) for x in available_pages)
    available_pages = int(available_pages)
    if available_pages <= 0:
        needtopay(message, available_pages)
    else:
        global document_id
        global mssg_id
        global chat_id
        chat_id = message.chat.id
        mssg_id = message.message_id
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        useless, file_extension = os.path.splitext(file_info.file_path)
        if file_extension not in cfg.allowedfiles:            #Is file unsupported
            wrong_extension(file_extension, message)
        else:
            download()                                              #User opinion


############# CALLBACK AND Q TO USER ################
def hope():
    def areusure():
        global number_of_pages
        global available_pages
        if number_of_pages > available_pages:
            notenoughpages(number_of_pages, available_pages)
        else:
            keyboard = types.InlineKeyboardMarkup()
            key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
            keyboard.add(key_yes)
            key_no= types.InlineKeyboardButton(text='No', callback_data='no')
            keyboard.add(key_no)
            global copy
            global chat_id
            global x
            not_one_and_how = 'Not ' + str(copy)
            key_not_one= types.InlineKeyboardButton(text=not_one_and_how, callback_data='not_one')
            keyboard.add(key_not_one)
            if number_of_pages == 1:
                bot.send_message(chat_id, 'In your file 1 page')
            else:
                bot.send_message(chat_id, 'in your file %s pages' % str(number_of_pages))
            x = int(number_of_pages) * copy
            str4ka= 'Are you sure you want to print ' + str(copy) + ' copy. Total ' + str(x) + ' pages of paper will be used'
            if x > available_pages:
                bot.send_message(chat_id, 'Thats too much, change the file. %s pages thats your limit' % available_pages)
            else:
                bot.send_message(chat_id, text=str4ka, reply_markup=keyboard)
    def call():
        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if call.data == 'yes':
                bot.send_message(chat_id, 'Success. You did it')
                try:
                    global x
                    global available_pages
                    user_id = str(call.message.from_user.id)
                    conn = sqlite3.connect('/telebot/pplids.sqlite')
                    sql = conn.cursor()
                    after = str(available_pages - x)
                    newsql = "UPDATE ppls SET AvailablePages = ? WHERE ID = ?"
                    sql.execute(newsql (available_pages, user_id))
                    conn.commit()
                    sql.close()
                    print(after)
                except sqlite3.Error as error:
                    print("Failed to update sqlite table", error)
                finally:
                    if (conn):
                        conn.close()
                        print("The sqlite connection is closed")
                print('Тут должен быть вызов на печать')
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, 'Ok then')
            elif call.data == 'not_one':
                bot.send_message(call.message.chat.id, 'And how much?')
                bot.register_next_step_handler(call.message, how_much)
    areusure()   #Making Inline Keyboard
    call()              #Cheking callback data


############# HOW MUCH ################
def how_much(message):
    global copy
    global available_pages
    try:
        copy = int(message.text)
        if copy > available_pages or copy < 1:
            bot.send_message(message.chat.id, 'Wrong. This is more than i can let you or less than 1. Try again')
            copy = 1
    except Exception:
        bot.send_message(message.chat.id, 'Write in numbers please and without float numbers')
    hope()               #Calling Inline Keyboard to ask again after checking number of copies


############# DOWNLOAD ################
def download():
    global document_id
    global mssg_id
    global copy
    global chat_id
    file_info = bot.get_file(document_id)     #Getting sended file info
    useless, file_extension = os.path.splitext(file_info.file_path)
    file_name = str(chat_id) + '.' + str(mssg_id)
    file_path = '/telebot/documents/' + file_name + str(file_extension)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_path)         #File downloaded
    copy = 1
    convertthat(file_path, file_name)           #Sending just downloaded file to LibreOffice


############# COPY CONVERT AND NUMBER OF PAGES ################
def convertthat(file_path, file_name):
    cmd = ['lowriter', '--convert-to', 'pdf', '--outdir', '/telebot/PDF', file_path]
    traceback = subprocess.run(cmd, check=True)             #Converting file to PDF so printer can print that
    if traceback.returncode == 0:
        global number_of_pages
        pdf_file_path = '/telebot/PDF/' + file_name + '.pdf'
        cmd_line = 'pdfinfo ' + pdf_file_path + ' | grep Pages | awk \'{print$2}\''
        number_of_pages = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, encoding='utf-8').communicate()[0]   #Number of pages is finally there
        number_of_pages = int(number_of_pages)
        hope()
    else:                   #Non zero val == Err
        print('not good yet:', traceback)


############# LOG ################
def DB(message):
    log = open('DB.txt', 'a')                   #Opening DB to write new user data
    newstr = str(message.from_user.id) + '  ' + str(message.message_id) + '  ' + '@' + str(message.from_user.username) +  '  ' + str(message.from_user.first_name) + '  ' + str(message.from_user.last_name)
    log.write(newstr+'\n')
    log.close()


############# JUST VIBING ################
if __name__ == '__main__':
    bot.infinity_polling(True)
