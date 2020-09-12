import telebot
import cfg
import urllib
import os

bot = telebot.TeleBot(cfg.token)
print('still alive')


###########HelloWorld################
@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    print(hi_message)
    bot.send_message(message.chat.id, hi_message)


###########FileDownload################
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    print('Got it')
    DB(message)
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_info.file_path)


###########NotNowBuddy################
@bot.message_handler(content_types=['text'])
def idk(message):
    DB(message)
    bot.send_message(message.chat.id, 'Have a question? - /start')


###########False################
@bot.message_handler(content_types=['photo'])
def issue(message):
    bot.send_message(message.chat.id, 'Am i joke to you?')


###########LOG################
def DB(message):
    log = open('DB.txt', 'a')
    newstr = str(message.from_user.id) + '  ' + '@' + str(message.from_user.username) +  '  ' + str(message.from_user.first_name) + '  ' + str(message.from_user.last_name)
    print(newstr)
    log.write(newstr+'\n')
    log.close()



bot.polling()
