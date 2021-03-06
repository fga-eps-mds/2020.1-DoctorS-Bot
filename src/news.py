from src import utils
from googlesearch import search
import re
import time

def run(update, context):
    hora = time.ctime().split()
    regex_time = r"[1][9]:[4][1]:[1][0]"

    while utils.is_logged(context.user_data):    
        hora = time.ctime().split()
        if re.search(regex_time, str(hora)):
            sendNews(update, context)
            print("Hora: :", hora[3])

    print("End Thread!")

def sendNews(update, context):
    regex = r"[Ff]acebook|[Tt]witer|[Ii]nstagram|[Ll]inked[Ii]n|[Aa]rticle"
    res = []
    for resultado in search("covid", stop=10):
        res.append(resultado)

    resultadoPrint = ""
    for resultado in res:
        if not re.search(regex, resultado):
            if len(resultado) > len(resultadoPrint):
                resultadoPrint = resultado

    print("Resul print: ", resultadoPrint)
    dateTotal = (time.strftime("%A, %d %B %Y", time.gmtime()))
    sendNew = "Olá, espero que esteja se sentindo bem! Hoje é " + str(stringDate(dateTotal)) + ".\n\n" + "A noticia do dia é: \n" + str(resultadoPrint) + "\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=sendNew
    )

def stringDate(dateTotal):
    dateTotal = dateTotal.replace('January', 'de janeiro de')
    dateTotal = dateTotal.replace('February', 'de fevereiro de')
    dateTotal = dateTotal.replace('March', 'de março de')
    dateTotal = dateTotal.replace('April', 'de abril de')
    dateTotal = dateTotal.replace('May', 'de maio de')
    dateTotal = dateTotal.replace('June', 'de junho de')
    dateTotal = dateTotal.replace('July', 'de julho de')
    dateTotal = dateTotal.replace('August', 'agosto de')
    dateTotal = dateTotal.replace('September', 'de setembro de')
    dateTotal = dateTotal.replace('July', 'de julho de')
    dateTotal = dateTotal.replace('October', 'de outubro de')
    dateTotal = dateTotal.replace('November', 'de novembro de')
    dateTotal = dateTotal.replace('December', 'de dezembro de')
    dateTotal = dateTotal.replace('Sunday', 'domingo')
    dateTotal = dateTotal.replace('Monday', 'segunda-feira')
    dateTotal = dateTotal.replace('Tuesday', 'terça-feira')
    dateTotal = dateTotal.replace('Wednesday', 'quarta-feira')
    dateTotal = dateTotal.replace('Thursday', 'quinta-feira')
    dateTotal = dateTotal.replace('Friday', 'sexta-feira')
    dateTotal = dateTotal.replace('Saturday', 'sábado')
    return dateTotal
