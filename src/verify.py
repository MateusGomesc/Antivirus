from pathlib import Path
from os import path


def verifyFiles():
    """Serch in computer if have any bad file

    Returns:
        False: if don't have any bad file
        List: list of bad file names that have in computer
    """

    # Receive absolute path
    route = path.join(path.abspath('./resource'), "filenames.txt")
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