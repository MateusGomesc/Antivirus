import os

caminho = 'C:/Users/Mateus/Documents/Projetos/Antivirus/tests/teste.txt'

try:
    os.unlink(caminho)
    print("Arquivo deletado!")
except PermissionError:
    print(PermissionError)
except FileNotFoundError:
    print(FileNotFoundError)
except Exception:
    print(Exception)