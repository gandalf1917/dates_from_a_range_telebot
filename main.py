from datetime import datetime, timedelta
import telebot


# функция для поиска дат с учетом дня недели
def find_weekday_dates(start_date, end_date, target_weekday):
    try:
        start_date_converted = datetime.strptime(start_date, '%d.%m.%Y')
        end_date_converted = datetime.strptime(end_date, '%d.%m.%Y')
    #отладка
    except ValueError:
        print("Ошибка при конвертации даты")
        print("start_date:", start_date)
        print("end_date:", end_date)
        return []  # Возвращаем пустой список, если даты введены некорректно

    result_dates = []
    current_date = start_date_converted
    print("start_date_converted:", start_date_converted)
    print("end_date_converted:", end_date_converted)
    print("target_weekday:", target_weekday)

    while current_date <= end_date_converted:
        if current_date.weekday() == target_weekday:
            result_dates.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    return result_dates


bot = telebot.TeleBot("Yor token")

#  хранение данных
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую!"
                                      "\nЯ могу вывести все определенные дни в заданном промежутке. "
                                      "\nНапример, тебе нужны все субботы месяца, просто введи начальную дату и конечную, а затем номер дня!"
                                      "\nДля начала работы набери команду /setup")


# Обработчик команды setup
@bot.message_handler(commands=['setup'])
def setup_message(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Введите start_date (в формате DD.MM.YY):")


@bot.message_handler(commands=['target_weekday'])
def target_weekday_command(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Введите номер дня недели (0 - Пн, 1 - Вт, ..., 6 - Вс):")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        user_info = user_data[chat_id]
        if "start_date" not in user_info:
            user_info["start_date"] = message.text
            bot.send_message(chat_id, "Введите end_date (в формате DD.MM.YY):")
        elif "end_date" not in user_info:
            user_info["end_date"] = message.text
            bot.send_message(chat_id, "Введите номер дня недели (0 - Пн, 1 - Вт, ..., 6 - Вс):")
        elif "target_weekday" not in user_info:
            target_weekday = message.text.strip()
            if target_weekday in ("0", "1", "2", "3", "4", "5", "6"):
                target_weekday = int(target_weekday)
                start_date = user_info["start_date"]
                end_date = user_info["end_date"]
                result_dates = find_weekday_dates(start_date, end_date, target_weekday)
                bot.send_message(chat_id, f"Найденные даты: {', '.join(result_dates)}")
                user_data.pop(chat_id, None)
            else:
                bot.send_message(chat_id, "я даун")

# Запуск бота
bot.polling()

