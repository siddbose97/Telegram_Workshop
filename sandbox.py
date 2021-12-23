import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

FIRSTSTEP = 0
SECONDSTEP = 1
THIRDSTEP = 2

# The API Key we received for our bot
#API_KEY = '5062654174:AAEg0b-JUF46drA87A4jnnmRohav0LyUBYA'
updater = Updater(API_KEY)
dispatcher = updater.dispatcher

class Human:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.gender = ""

humans = {}


# The entry function
def start(update_obj, context):
    try:
        update_obj.message.reply_text("Hello there, what is your name?")
        return FIRSTSTEP
    except Exception:
        error(update_obj, context)

def name_step(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id] = Human(msg)
        
        update_obj.message.reply_text("How old are you?")
        return SECONDSTEP
    except Exception:
        error(update_obj, context)

def gender_step(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id].age = msg
        
        list1 = [[telegram.KeyboardButton(text="Male")],[telegram.KeyboardButton(text="Female")]]

        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text("What is your gender?",reply_markup=kb)
        return THIRDSTEP
    except Exception:
        error(update_obj, context)
def end(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id].gender = msg
        
        update_obj.message.reply_text(
            f"Thank you {humans[chat_id].name}, you are a {humans[chat_id].gender} and {humans[chat_id].age} years old", reply_markup=telegram.ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    except Exception:
        error(update_obj, context)
        
def error(update_obj, context):
    update_obj.message.reply_text("There was an error. Click /start to start again!")
    return ConversationHandler.END

def main():
    
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRSTSTEP: [MessageHandler(Filters.text, name_step)],
            SECONDSTEP: [MessageHandler(Filters.text, gender_step)],
            THIRDSTEP:[MessageHandler(Filters.text, end)]

        },
        fallbacks=[CommandHandler('cancel', error)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()





