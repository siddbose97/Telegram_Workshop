import telegram
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

class Human:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.gender = ""

humans_dict = {}

API_KEY = "5062654174:AAEg0b-JUF46drA87A4jnnmRohav0LyUBYA"
updater = Updater(API_KEY)
dispatcher = updater.dispatcher

FIRSTSTEP = 1
SECONDSTEP = 2
THIRDSTEP = 3

def start(update_obj, context):
  update_obj.message.reply_text("Hello there, what is your name?")
  return FIRSTSTEP

def ask_age_step(update_obj, context):
  chat_id = update_obj.message.chat_id
  name = update_obj.message.text
  humans_dict[chat_id] = Human(name)

  update_obj.message.reply_text("How old are you?")
  return SECONDSTEP
  
def ask_gender_step(update_obj, context):
  chat_id = update_obj.message.chat_id
  age = update_obj.message.text
  user = humans_dict[chat_id]
  user.age = age

  list1 = [[telegram.KeyboardButton(text="Male")],[telegram.KeyboardButton(text="Female")]]
  
  kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

  update_obj.message.reply_text("What is your gender?",reply_markup=kb)
  
  return THIRDSTEP

def output_info_step(update_obj, context):
  chat_id = update_obj.message.chat_id
  gender = update_obj.message.text
  user = humans_dict[chat_id]
  user.gender = gender
  
  update_obj.message.reply_text(
      f"Thank you {user.name}, you are a {user.gender} and {user.age} years old", reply_markup=telegram.ReplyKeyboardRemove()
  )
  return ConversationHandler.END

def main():
    
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
          FIRSTSTEP: [MessageHandler(Filters.text, ask_age_step)],
          SECONDSTEP: [MessageHandler(Filters.text, ask_gender_step)],
          THIRDSTEP: [MessageHandler(Filters.text, output_info_step)]
          
        },
        fallbacks=[],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()


