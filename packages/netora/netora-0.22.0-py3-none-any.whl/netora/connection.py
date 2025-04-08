import subprocess
import os
import sys

from colorama import Style, Fore

def check_connection(host):
    param = "-n" if os.name == "nt" else "-c"
    command = ["ping", param, "1", host]

    try:         
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        if os.name == "nt":      
            if "Received = 1" in output:
                pass
            else:
                print(
                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.RED + "!" + Fore.WHITE + "]"
                    + Fore.RED + " Error:"
                    + Fore.WHITE + " No internet connection"
                    + Style.RESET_ALL
                )        
        else:
            if "1 packets transmitted, 1 received" in output:
                pass 
            else:
                print(
                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.RED + "!" + Fore.WHITE + "]"
                    + Fore.RED + " Error:"
                    + Fore.WHITE + " No internet connection"
                    + Style.RESET_ALL
                )  

    except subprocess.CalledProcessError as error:
        print(
            Fore.WHITE + Style.BRIGHT + "["
            + Fore.RED + "!" + Fore.WHITE + "]"
            + Fore.RED + " Error:"
            + Fore.WHITE + f" {error}"
            + Style.RESET_ALL
        )
        sys.exit(1)