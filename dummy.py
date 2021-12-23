import telegram
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# The API Key we received for our bot
API_KEY = '5062654174:AAEg0b-JUF46drA87A4jnnmRohav0LyUBYA'
updater = Updater(API_KEY)
dispatcher = updater.dispatcher

FIRSTSTEP, SECONDSTEP, THIRDSTEP = range(3)

     
def help(update_obj, context):
    try:
        help_string = """
This is a dummy bot! Thanks for coming
        """

        update_obj.message.reply_text(help_string)
        return ConversationHandler.END

    except Exception as e:
        cancel(update_obj, context)
        return ConversationHandler.END
#=================================================================================================================

class Human:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.gender = ""

humans = {}


# The entry function
def start(update_obj, context):
  
    try:
        
        chat_id = update_obj.message.chat_id
        update_obj.message.reply_text("Hello there, what is your name?")
        return FIRSTSTEP
    except Exception:
        cancel(update_obj, context)


def name_step(update_obj, context):
      
    try:
        
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id] = Human(msg)
        list1 = [[telegram.KeyboardButton(text=gender)] for gender in ["Male", "Female"]]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text("What is your gender?",reply_markup=kb)
    # go to the Batallion state
        return SECONDSTEP
    except Exception as e:
        cancel(update_obj, context)

def gender_step(update_obj, context):
      
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id].gender = msg
        
        update_obj.message.reply_text("How old are you?")
        return THIRDSTEP
    except Exception as e:
        cancel(update_obj, context)

def end(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        humans[chat_id].age = msg
        
        update_obj.message.reply_text(
            f"Thank you {humans[chat_id].name}, you are a {humans[chat_id].gender} and {humans[chat_id].age} years old", reply_markup=telegram.ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END 


def cancel(update_obj, context):
    # get the user's first name
    update_obj.message.reply_text(
        f"Okay, bad input, press /start to try again",reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END       

def main():

    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('help', help)],
        states={
                FIRSTSTEP: [MessageHandler(Filters.text, name_step)],
                SECONDSTEP: [MessageHandler(Filters.text, gender_step)],
                THIRDSTEP: [MessageHandler(Filters.text, end)],
        },
        fallbacks=[CommandHandler('cancel', end)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()





