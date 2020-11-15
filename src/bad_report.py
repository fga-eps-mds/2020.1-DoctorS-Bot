from telegram import ReplyKeyboardMarkup
import requests
import json
from src import getters, utils, handlers

CHOOSING = 0

sintomas = ["Dor de Cabeça", "Febre", "Tosse", "Falta de Ar"]

markup = ReplyKeyboardMarkup([ ['Dor de Cabeça', 'Febre'],
                               ['Falta de Ar', 'Tosse'],
                               ['Done']],
        resize_keyboard=True,
        one_time_keyboard=True)

def start(update, context):
    context.user_data['Symptoms'] = list()

    update.callback_query.edit_message_text(
        "Obrigado por nos informar!"
        )

    context.bot.send_message(
        text='Selecione os sintomas que sentiu nas últimas 24 horas!',
        chat_id=update.effective_chat.id,
        reply_markup=markup
    )

    return CHOOSING


def regular_choice(update, context):

    message = update.message.text

    if message in sintomas and not message in context.user_data['Symptoms']:
        context.user_data['Symptoms'].append(update.message.text)

    string = utils.list_to_str(context.user_data['Symptoms'])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{string}\nSelecione os sintomas que sentiu, lembrando que é necessário nos fornecer sua localização antes de enviar.",
        reply_markup=markup
    )

    return CHOOSING


def done(update, context):


    headers =  {'Accept' : 'application/vnd.api+json', 'Content-Type' : 'application/json', 'Authorization' : str(context.user_data['AUTH_TOKEN'])}

    json_entry = {
        "survey" : {
                "symptom": context.user_data['Symptoms']
        }
    }

    url = f"http://localhost:3001/users/{context.user_data['id']}/surveys"

    req = requests.post(headers=headers, json=json_entry, url=url)

    if req.status_code != 200:
        print(req.status_code)

    handlers.menu(update.context)

    return -1 # END
