from pathlib import Path
from os import path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, LoggingEventHandler
import time
import logging
import re

# Receive absolute path
route = path.join(path.abspath('./resource'), "filenames.txt")

def verifyFilesExists():
    """Serch in computer if have any bad file

    Returns:
        False: if don't have any bad file
        List: list of bad file names that have in computer
    """

    
    badFilesExisting = []

    with open(route, "r") as file:
        lines = file.readlines()

        # Verify if files exists
        for line in lines:
            filePath = Path(line)

            if filePath.exists():
                badFilesExisting.append(line)
        
        file.close()

    if not badFilesExisting:
        return False
    else:
        return badFilesExisting



def watchBadFiles():
    # Configure log
    logging.basicConfig(filemode='a', filename='resource/dev.log', level=logging.INFO, 
                    format='%(message)s %(process)d',
                    datefmt='%Y-%m-%d %H:%M:%S')
    
    class Handler(PatternMatchingEventHandler):
        def __init__(self):
            PatternMatchingEventHandler.__init__(self)

        def on_any_event(self, event):
            with open(route, "r") as file:
                lines = file.readlines()

                for line in lines:
                    if line == event.src_path:
                        print('Deu ruim cumpade')
                
                file.close()

    
    path = 'C:/Users/Mateus'

    observer = Observer()

    eventHandlerFunctions = Handler()
    eventHandlerLogging = LoggingEventHandler()

    observer.schedule(eventHandlerLogging, path, recursive=True)
    observer.schedule(eventHandlerFunctions, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

watchBadFiles()