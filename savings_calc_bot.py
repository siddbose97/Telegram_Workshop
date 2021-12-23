import telegram
from telegram import replymarkup
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# The API Key we received for our bot
API_KEY = ["USE YOUR OWN"]
updater = Updater(API_KEY)
dispatcher = updater.dispatcher

FIRSTSTEP, SECONDSTEP, THIRDSTEP, FOURTHSTEP, FIFTHSTEP, SIXTHSTEP = range(6)

def periodic_investment(rate, num_investments, years):
    result = ((1+(rate/num_investments))**(num_investments*years)-1)/(rate/num_investments)
    return result

def help(update_obj, context):
    try:
        help_string = """
This is a Savings bot! Thanks for coming
        """

        update_obj.message.reply_text(help_string)
        return ConversationHandler.END

    except Exception as e:
        cancel(update_obj, context)
        return ConversationHandler.END
#=================================================================================================================
class Input:
    def __init__(self,age):
        self.age = age
        self.input = 0
inputs = {}
# The entry function
def start(update_obj, context):
  
    try:
        update_obj.message.reply_text("Hello there, how old are you?")
    # go to the Batallion state
        return FIRSTSTEP
    except Exception as e:
        cancel(update_obj, context)

def choice_step(update_obj, context):
      
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        inputs[chat_id] = Input(int(msg))

        list1 = [[telegram.KeyboardButton(text=choice)] for choice in ["Total Savings", "Savings Per Month"]]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)
        update_obj.message.reply_text("Thank you for your age, what would you like to calculate", reply_markup=kb)
    # go to the Batallion state
        return SECONDSTEP
    except Exception as e:
        cancel(update_obj, context)



def check_choice(update_obj, context):
      
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text

        if msg == "Total Savings":
            update_obj.message.reply_text("You want to calculate Total Savings. How much will you save per month?")
            return THIRDSTEP
        elif msg == "Savings Per Month":
            update_obj.message.reply_text("You want to calculate Savings per month. How much is your end goal?")
            return FOURTHSTEP    
    except Exception as e:
        cancel(update_obj, context)

def total_savings_step(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text

        age = inputs[chat_id].age
        monthly_savings = int(msg)

        end_result_5_percent = round(periodic_investment(0.05, 12, 60-age)*monthly_savings,2)
        end_result_7_percent = round(periodic_investment(0.07, 12, 60-age)*monthly_savings,2)
        end_result_10_percent = round(periodic_investment(0.10, 12, 60-age)*monthly_savings,2)

        ret_string = (f"""
        If you save ${"{:,}".format(monthly_savings)} per month, then at 60 you will have:
    
        ${"{:,}".format(end_result_5_percent)} at 5% per year
        ${"{:,}".format(end_result_7_percent)} at 7% per year
        ${"{:,}".format(end_result_10_percent)} at 10% per year""")

        update_obj.message.reply_text(ret_string)
        return ConversationHandler.END 
    except Exception as e:
        cancel(update_obj, context)

def monthly_savings_step(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text

        age = inputs[chat_id].age
        end_goal = int(msg)

        periodic_payment_5_percent = round(end_goal/periodic_investment(0.05, 12, 60-age),2)
        periodic_payment_7_percent = round(end_goal/periodic_investment(0.07, 12, 60-age),2)
        periodic_payment_10_percent = round(end_goal/periodic_investment(0.10, 12, 60-age),2)
        
        ret_string = (f"""
        To save ${"{:,}".format(end_goal)} by age 60 you need to save:
        
        ${"{:,}".format(periodic_payment_5_percent)} per month at 5% per year
        ${"{:,}".format(periodic_payment_7_percent)} per month at 7% per year
        ${"{:,}".format(periodic_payment_10_percent)} per month at 10% per year""")
        update_obj.message.reply_text(ret_string)
        return ConversationHandler.END 
    except Exception as e:
        cancel(update_obj, context)


def cancel(update_obj, context):
    # get the user's first name
    update_obj.message.reply_text(
        f"Okay, bad input, press /start to try again",reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END       

def main():

    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('help', help)],
        states={
                FIRSTSTEP: [MessageHandler(Filters.text, choice_step)],
                SECONDSTEP: [MessageHandler(Filters.text, check_choice)],
                THIRDSTEP: [MessageHandler(Filters.text, total_savings_step)],
                FOURTHSTEP: [MessageHandler(Filters.text, monthly_savings_step)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()