from telegram import ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
import requests
import src.utils as utils
import src.signup as signup
import src.login as login
import time


#Envia o menu para o usuario
def start(update, context):
    print(update.effective_chat.id)

    reply_keyboard = [['Login','Registrar'],
                      ['Sobre','Finalizar']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    resposta = ("Bem vindo ao DoctorS Bot, selecione a opção desejada.\n\n"
                "Caso deseje voltar ao menu, digite /menu ou /start.\n")

    update.message.reply_text(
        resposta, reply_markup=markup
    )

#Cadastra novo user
def signup_handler():
    return ConversationHandler(
            entry_points=[MessageHandler(Filters.text("Registrar"), signup.start)],
            states={
                signup.CHOOSING: [MessageHandler(Filters.regex('^(Username|Email|Senha|Genero sexual|Raça|Trabalho)$'),
                                        signup.regular_choice)
                        ],
                signup.TYPING_CHOICE: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                                signup.regular_choice)],
                signup.TYPING_REPLY: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                                signup.received_information)],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), signup.done)],
            allow_reentry=True
            )


#Login de usuario
def login_handler():
    return ConversationHandler(
            entry_points=[MessageHandler(Filters.text("Login"), login.start)],
            states={
                login.CHOOSING: [MessageHandler(Filters.regex('^(Email|Senha)$'),
                                        login.regular_choice)
                        ],
                login.TYPING_CHOICE: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                                login.regular_choice)],
                login.TYPING_REPLY: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                                login.received_information)],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), login.done)],
            allow_reentry=True
            )


#Envia informaçoes sobre o bot
def sobre(update, context):
    resposta = 'O DoctorS é um Telegram Bot criado para ajudar a população no combate ao novo Corona Vírus(SARS-CoV-2).'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=resposta
    )
    

def finalizar(update, context):
    resposta = """Já vai? Tudo bem, sempre que quiser voltar, digite /menu ou /start e receberá o menu inicial.\n\nObrigado por usar o DoctorS!"""

    context.bot.send_message(chat_id=update.effective_chat.id,
    text=resposta)


#Mensagens não reconhecidas
def unknown(update, context):
    resposta = "Não entendi. Tem certeza de que digitou corretamente?"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=resposta,
    )




