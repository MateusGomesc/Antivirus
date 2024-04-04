from pathlib import Path
from os import path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, LoggingEventHandler
import time
import logging
import os
from getpass import getuser

class Sentinela():
    def __init__(self):
        self.routeBadFileNames = path.join(path.abspath('./resource'), 'filenames.txt')
        self.routeLogs = path.join(path.abspath('./resource'), 'dev.log')
        self.pathMonitored = f'C:/Users/{getuser()}'

    def verifyFilesExists(self):
        """Serch in computer if have any bad file

        Returns:
            False: if don't have any bad file
            List: list of bad file names that have in computer
        """

        
        badFilesExisting = []

        with open(self.routeBadFileNames, "r") as file:
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


    def watchBadFiles(self):
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
                with open(Sentinela().routeBadFileNames, "r") as file:
                    lines = file.readlines()
                    eventPath = Path(event.src_path)

                    for line in lines:
                        line = Path(line.replace("%", "").capitalize())
                        fullLine = path.join(Path(f'C:/Users/{getuser()}'), line)

                        if fullLine == eventPath:
                            os.unlink(eventPath)
                    
                    file.close()

        observer = Observer()

        eventHandlerFunctions = Handler()
        eventHandlerLogging = LoggingEventHandler()

        observer.schedule(eventHandlerLogging, self.pathMonitored, recursive=True)
        observer.schedule(eventHandlerFunctions, self.pathMonitored, recursive=True)

        observer.start()

        try:
            while True:
                self.keepsLogs()
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()


    def keepsLogs(self):
        """
            Keeps the log in file in small size
        """
        with open(self.routeLogs, "r") as fileRead:
            while True:
                lines = fileRead.readlines()
                sizeOfFile = 100
                
                if len(lines) >= sizeOfFile:
                    del lines[-1]
                
                with open(self.routeLogs, "w") as fileWrite:
                    fileWrite.writelines(lines)
                    fileWrite.close()
                time.sleep(1)

            fileRead.close()
