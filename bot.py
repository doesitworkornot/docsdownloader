import telebot
import cfg
import urllib
import os

bot = telebot.TeleBot(cfg.token)


############# START COMMAND ################
@bot.message_handler(commands=['start'])
def start(message):
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    bot.send_message(message.chat.id, hi_message)


############# FILE CHECK AND DOWNLOAD ################
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    DB(message)
    if message.document.thumb == None:                        #Is file too big?
        toobig(message)
    else:
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        useless, file_extension = os.path.splitext(file_info.file_path)
        if file_extension not in cfg.allowedfiles:            #Is file unsupported
            wrong_extension(file_extension, message)
        else:                                                 #All is fine lets download
            file_path = 'documents/' + str(message.from_user.id) + str(message.message_id) + str(file_extension)
            link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
            urllib.request.urlretrieve(link, file_path)
            bot.send_message(message.chat.id, 'Succsess. You did it')


############# HELP COMMAND ################
@bot.message_handler(commands=['help'])
def idk(message):
    bot.send_message(message.chat.id, 'Have a question or suggestions? - /start or write to this guy @tilliknow')


############# IF PHOTO ################
@bot.message_handler(content_types=['photo'])
def issue(message):
    bot.send_message(message.chat.id, 'Am i joke to you?')


############# LOG ################
def DB(message):
    log = open('DB.txt', 'a')
    newstr = str(message.from_user.id) + '  ' + str(message.message_id) + '  ' + '@' + str(message.from_user.username) +  '  ' + str(message.from_user.first_name) + '  ' + str(message.from_user.last_name)
    log.write(newstr+'\n')
    log.close()


############# TOO BIG ################
def toobig(message):
    bot.send_message(message.chat.id, 'File is too big :) There\'s no way')


############# NOT SUPPORTS ################
def wrong_extension(file_extension, message):
    wrong_message = 'Sorry but '+file_extension+' type file doesnt supports. Try other filetype'
    bot.send_message(message.chat.id, wrong_message)


bot.polling()
