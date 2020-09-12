import telebot
import cfg
import urllib

bot = telebot.TeleBot(cfg.token)
print('still alive')

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    print(hi_message)
    bot.send_message(message.chat.id, hi_message)

@bot.message_handler(content_types=["document"])
def handle_docs(message):
    print('Got it')
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_info.file_path)

@bot.message_handler(content_types=['text'])
def idk(message):
    bot.send_message(message.chat.id, 'Have a question? - /start')

@bot.message_handler(content_types=['text'])
def issue(message):
    bot.send_message(message.chat.id, 'Hi there you should send me as file NOT AS PHOTO. Got it?')

bot.polling()
