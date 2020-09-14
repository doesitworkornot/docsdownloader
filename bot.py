import telebot
import cfg
import urllib
import os
from telebot import types

bot = telebot.TeleBot(cfg.token)

flag = False


############# START COMMAND ################
@bot.message_handler(commands=['start'])
def start(message):
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    bot.send_message(message.chat.id, hi_message)


############# FILE CHECK ################
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    DB(message)

    if message.document.file_size >= 20971520:
        print('too big')
        print(message.document)                                #Is file too big?
        toobig(message)
    else:
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        useless, file_extension = os.path.splitext(file_info.file_path)
        if file_extension not in cfg.allowedfiles:            #Is file unsupported
            wrong_extension(file_extension, message)
        else:                                                 #User opinion
            areusure(message)
            global flag
            while flag == True:
                download(message, file_extension, file_info)
                print('Флаг опускаем')
                flag = False

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


############# BUTTONS TEST ################
@bot.message_handler(commands = ['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    mylovestbutton = types.InlineKeyboardButton(text='Wanna check smth?', url='https://github.com/doesitworkornot?tab=repositories')
    markup.add(mylovestbutton)
    bot.send_message(message.chat.id, "you'll like it", reply_markup=markup)


############# DOWNLOAD ################
def download(message, file_extension, file_info):
    file_path = 'documents/' + str(message.from_user.id) + str(message.message_id) + str(file_extension)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_path)
    bot.send_message(message.chat.id, 'Success. You did it')


############# USER CHECK ################
def areusure(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='No', callback_data='no')
    keyboard.add(key_no)
    key_not_one= types.InlineKeyboardButton(text='Not one', callback_data='not_one')
    keyboard.add(key_not_one)
    bot.send_message(message.chat.id, text='Are you sure you want to print one copy', reply_markup=keyboard)


############# DATA CHECK ################
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        global flag                         #git fix
        flag = True
        print('Флаг сейчас:', flag)
    elif call.data == 'not_one':
        bot.send_message(call.message.chat.id, 'How much?')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Ok then')
    bot.delete_message(call.message.chat.id, call.message.message_id)



bot.polling()
