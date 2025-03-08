import telebot
import models
import os  

bot = telebot.TeleBot('ZAMENITb')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне фото")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_name = file_info.file_path.split('/')[-1]  
        downloaded_file = bot.download_file(file_info.file_path) 

        # Сохраняем файл на компьютере
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, f"Файл сохранен под именем {file_name}")

        with open(file_name, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=models.prediction(file_name))

 
        os.remove(file_name)  
        bot.reply_to(message, f"Файл {file_name} удален с сервера")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, "Пожалуйста, отправьте изображение")

bot.polling()
