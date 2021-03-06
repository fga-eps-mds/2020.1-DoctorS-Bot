from telegram.ext import CommandHandler, Filters, CallbackQueryHandler, MessageHandler, Updater
from src import handlers, news, daily_report
from pathlib import Path

class Bot:

    def __init__(self):

        try:
            # Le o token no arquivo 'token.txt' e passa para a variavel
            current_path = Path(__file__).parent.absolute()
            f = open(str(current_path) + "/../config/token.txt", "r")
            TELEGRAM_TOKEN = f.read()
            f.close()

            # Estrutura responsavel por verificar todas novas mensagens
            self.updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

            # Estrutura responsavel por interpretar mensagens recebidas e respondelas
            # de acordo com a interpretacao de cada uma
            dispatcher = self.updater.dispatcher

            # Mensagens reconhecidas
            dispatcher.add_handler(CommandHandler("start", handlers.start)) # Menu inicial
            dispatcher.add_handler(CommandHandler("menu", handlers.start)) # Menu inicial
            dispatcher.add_handler(MessageHandler(Filters.text("Sobre"), handlers.sobre)) # Sobre o bot
            dispatcher.add_handler(MessageHandler(Filters.text("Finalizar"), handlers.finalizar )) # Finalizar conversa
            dispatcher.add_handler(CommandHandler('noticia', news.sendNews))
            dispatcher.add_handler(CommandHandler('report', daily_report.report_requested))

            # Handler para mostrar informações do usuário
            dispatcher.add_handler(MessageHandler(Filters.text("Minhas informações"), handlers.get_user_info)) 
            
            # Estrutura para registros
            dispatcher.add_handler(handlers.signup_handler())
            
            # Estrutura para login
            dispatcher.add_handler(handlers.login_handler())

            # Estrutura para dicas
            dispatcher.add_handler(handlers.tips_handler())
            
            # Estrutura para mostrar o perfil/editar perfil
            dispatcher.add_handler(handlers.perfil_handler())

            # Função de logout
            dispatcher.add_handler(MessageHandler(Filters.text("Logout"), handlers.logout))

            # Função tutorial
            dispatcher.add_handler(MessageHandler(Filters.text("Ajuda"), handlers.ajuda))

            # Notificações diárias
            dispatcher.add_handler(MessageHandler(Filters.text('Habilitar Notificações'), handlers.daily_report, pass_job_queue=True))
            dispatcher.add_handler(MessageHandler(Filters.text('Cancelar Notificações'), daily_report.cancel_daily, pass_job_queue=True))

            # Feedback diario
            dispatcher.add_handler(CallbackQueryHandler(daily_report.good_report, pattern='^good_report$'))
            dispatcher.add_handler(handlers.bad_report_handler())

            # Callback query do calendário
            dispatcher.add_handler(CallbackQueryHandler(handlers.birthDayCallBack, pattern='^((?!good_report|bad_report).)*$'))

            dispatcher.add_handler(MessageHandler(Filters.text("Relatório de Saúde"), handlers.get_report_status))

            # Mensagens não reconhecidas, serão respondidas aqui por uma mensagem generica
            dispatcher.add_handler(MessageHandler(Filters.all , handlers.unknown)) 
           
            

        except Exception as e:
            print(e)
            print("Token não encontrado, alguns motivos:\n"
                  "1 - Executou na pasta raiz?\n"
                  "2 - Realmente tem um arquivo token.txt na pasta config?")

    def run(self):
        #Mantem o bot rodando localmente enquanto o programa estiver sendo executado
        self.updater.start_polling()
        self.updater.idle()
