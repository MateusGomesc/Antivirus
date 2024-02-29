import subprocess
import ctypes
import sys

#Executar o script como administrador
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)

#Executa comando para regras do firewall
comando = ['powershell', 'Get-NetFirewallRule']
res = subprocess.run(comando, capture_output=True, text=True)
print(res.stdout)

input()