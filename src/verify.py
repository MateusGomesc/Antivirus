from pathlib import Path
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler, LoggingEventHandler, RegexMatchingEventHandler
import time
import logging
import re

# Receive absolute path of files
routeBadFileNames = path.join(path.abspath('./resource'), 'filenames.txt')
routeLogs = path.join(path.abspath('./resource'), 'dev.log')

def verifyFilesExists():
    """Serch in computer if have any bad file

    Returns:
        False: if don't have any bad file
        List: list of bad file names that have in computer
    """

    
    badFilesExisting = []

    with open(routeBadFileNames, "r") as file:
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



def watchBadFiles(path):
    """keep watching the events that happening

    Args:
        path (string): path will be monitored
    """
    # Configure log
    logging.basicConfig(filemode='a', filename='resource/dev.log', level=logging.INFO, 
                    format='%(message)s %(process)d',
                    datefmt='%Y-%m-%d %H:%M:%S')
    
    class Handler(PatternMatchingEventHandler):
        def __init__(self):
            PatternMatchingEventHandler.__init__(self)

        def on_any_event(self, event):
            with open(routeBadFileNames, "r") as file:
                lines = file.readlines()

                for line in lines:
                    if line == event.src_path:
                        print('Deu ruim cumpade')
                
                file.close()

    observer = Observer()

    eventHandlerFunctions = Handler()
    eventHandlerLogging = LoggingEventHandler()

    observer.schedule(eventHandlerLogging, path, recursive=True)
    observer.schedule(eventHandlerFunctions, path, recursive=True)

    observer.start()

    try:
        while True:
            keepsLogs()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def keepsLogs():
    with open(routeLogs, "r") as fileRead:
        while True:
            lines = fileRead.readlines()
            sizeOfFile = 100
            
            if len(lines) >= sizeOfFile:
                del lines[-1]
            
            with open(routeLogs, "w") as fileWrite:
                fileWrite.writelines(lines)
                fileWrite.close()
            time.sleep(1)
        fileRead.close()


watchBadFiles()