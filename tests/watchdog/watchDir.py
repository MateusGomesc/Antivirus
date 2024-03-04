import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler
import logging
import getpass
import os
import shutil


class Handler(PatternMatchingEventHandler):
    def __init__(self) -> None:
        PatternMatchingEventHandler.__init__(self, patterns=['*.csv', '*.txt'], ignore_directories=True, case_sensitive=False)

    def on_any_event(self, event):
        """
            Salvar arquivos que foram modificados
            return: void
        """
        
        backupPath = 'C:/Users/Mateus/Documents/Projetos/Antivirus/tests/watchdog/backup/'

        #Salva os arquivos na pasta backup
        for file in os.listdir(path):
            #Constroe arquivo e destino
            source = os.path.join(path, file)
            destination = os.path.join(backupPath, file)

            #copia arquivos
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                print(f'copied: {file}')


if __name__ == '__main__':
    #Receber user
    user = getpass.getuser()

    logging.basicConfig(filemode='a', filename='dir.log',level=logging.INFO,
                        format='%(asctime)s - %(message)s - %(process)d ' + f'- {user}',
                        datefmt='%Y-%m-%d %H:%M:%S')

    #Diretório a ser monitorado
    path = sys.argv[1] if len(sys.argv) > 1 else './'
    
    #Define observer
    observer = Observer()

    #Define Handler
    eventHandlerFunctions = Handler()
    eventHandlerLogin = LoggingEventHandler()

    #Salva arquivos modificados
    # eventHandler.on_modified = onModified
    
    #Programa monitoramento
    observer.schedule(eventHandlerFunctions, path, recursive=True)
    observer.schedule(eventHandlerLogin, path, recursive=True)

    #inicia monitoramento
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()