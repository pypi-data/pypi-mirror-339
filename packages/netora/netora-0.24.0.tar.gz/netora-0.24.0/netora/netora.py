#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import requests
import sys
import time

from colorama import Style, Fore, init

try:
    from netora.__init__ import import_error
except ImportError:
    print(
        Fore.WHITE + Style.BRIGHT + "\n["
        + Fore.RED + "!" + Fore.WHITE + "]"
        + Fore.RED + " Error:"
        + Fore.WHITE + " Did you run netora with "
        + Fore.WHITE + "`python3 netora/netora.py ...`?"
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN + Style.BRIGHT + "\n["
        + Fore.BLUE + "i" + Fore.GREEN + "]"
        + Fore.GREEN + " This method is no longer supported. Refer to "
        + Fore.WHITE + "\033[4mhttps://nativevoid.mintlify.app/installation\033[24m" 
        + Fore.GREEN + " for the current installation guide."
        + Style.RESET_ALL
    )
    sys.exit(1)

from netora.getinfo import get_ip_info
from netora.validation import validate_ip
from netora.connection import check_connection

def main():
    try: 
        check_connection("8.8.8.8")
        parser = ArgumentParser(
            description="Netora: Quickly uncover details and geolocation for any IP address (Version: 0.24.0)"
        )
        parser.add_argument(
            "--version",
            action="version",
            version="Netora v0.24.0",
            help="Display version information.",
        )
        parser.add_argument(
            "ip",
            metavar="IP_ADDRESSES",
            nargs="+",
            action="store",
            help="One or more IP addresses for looking up location and network information.",
        )
        parser.add_argument(
            "--folderoutput",
            "-fo",
            dest="folderoutput",
            help="Multiple IP addresses can be used, and the results will be saved in this folder."
        )    
        parser.add_argument(
            "--output",
            "-o", 
            dest="output", 
            help="Only one IP address can be used, and the result will be saved to this file.",
        )
        parser.add_argument(
            "--no-color",
            action="store_true",
            dest="no_color",
            default=False,
            help="Don't color terminal output",
        )

        args = parser.parse_args()

        if args.no_color:
            init(strip=True, convert=False)
        else:
            init(autoreset=True)

        if args.output is not None and len(args.ip) != 1:
            print(
                Fore.WHITE + Style.BRIGHT + "\n["
                + Fore.RED + "!" + Fore.WHITE + "]"
                + Fore.RED + " Error:"
                + Fore.WHITE + " You can only use --output with a single username" 
                + Style.RESET_ALL
            )
            sys.exit(1)

        for target_ip in args.ip:
            time.sleep(2)
            if not validate_ip(target_ip):
                print(
                    Fore.WHITE + Style.BRIGHT + "\n["
                    + Fore.RED + "!" + Fore.WHITE + "]"
                    + Fore.RED + " Error:"
                    + Fore.WHITE  + " Invalid IP address" 
                    + Style.RESET_ALL
                )
                continue

            print(
                Fore.GREEN + Style.BRIGHT + "\n["
                + Fore.YELLOW + "*" 
                + Fore.GREEN + "]"
                + " Retrieving" + Fore.WHITE 
                + " IP" + Fore.GREEN + " information"
                + Style.RESET_ALL
            )

            response = requests.get(f"https://ipapi.co/{target_ip}/json")
            response2 = requests.get(f"https://api.db-ip.com/v2/free/{target_ip}")

            if response.status_code == 200 and response2.status_code == 200:
                ip_info = response.json()
                ip_info2 = response2.json()

                ip_data = get_ip_info(ip_info, ip_info2)
                ip_location = f"https://www.openstreetmap.org/?mlat={ip_data['latitude']}&mlon={ip_data['longitude']}"
                ip_location_response = requests.get(ip_location)

                if ip_location_response.status_code == 200:          
                    ip_data = get_ip_info(ip_info, ip_info2, ip_location)               
                else:
                    ip_location = "Not Found"
                    ip_data = get_ip_info(ip_info, ip_info, ip_location)

                results_count = len(ip_data)

                for attribute, lookup_result in ip_data.items():
                    if "Not Found" in str(lookup_result):
                        results_count -= 1

                time.sleep(2.5)
                print(
                    Fore.WHITE + Style.BRIGHT + "\n[" 
                    + Fore.GREEN + "+" 
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Data"
                    + Fore.WHITE + " retrieved successfully"
                    + Style.RESET_ALL
                )
                time.sleep(1.5)

                print(
                    Fore.WHITE + Style.BRIGHT + "\n\n" + "[" 
                    + Fore.GREEN + "+" 
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Target:" 
                    + Style.RESET_ALL +  f" {ip_data['ip']}" + "\n" + 

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " IP version:" 
                    + Style.RESET_ALL + f" {ip_data['ipv']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " ISP:" 
                    + Style.RESET_ALL + f" {ip_data['isp']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Continent:" 
                    + Style.RESET_ALL + f" {ip_data['continent_name']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Continent code:" 
                    + Style.RESET_ALL + f" {ip_data['continent_code']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Country:" 
                    + Style.RESET_ALL + f" {ip_data['country']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]"
                    + Fore.GREEN + " Country code:" 
                    + Style.RESET_ALL + f" {ip_data['country_code']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Country capital:" 
                    + Style.RESET_ALL + f" {ip_data['country_capital']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Phone code:" 
                    + Style.RESET_ALL + f" {ip_data['phone_code']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " City:" 
                    + Style.RESET_ALL + f" {ip_data['city']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Latitude:" 
                    + Style.RESET_ALL + f" {ip_data['latitude']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Longitude:" 
                    + Style.RESET_ALL + f" {ip_data['longitude']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Location link:" 
                    + Style.RESET_ALL + f" {ip_data['location_link']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Currency name:" 
                    + Style.RESET_ALL + f" {ip_data['currency_name']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Currency symbol:" 
                    + Style.RESET_ALL + f" {ip_data['currency_symbol']}" + "\n" +

                    Fore.WHITE + Style.BRIGHT + "["
                    + Fore.GREEN + "+"
                    + Fore.WHITE + "]" 
                    + Fore.GREEN + " Local time:" 
                    + Style.RESET_ALL + f" {ip_data['local_time']}" + "\n\n" +
                
                    Fore.GREEN + Style.BRIGHT + "["
                    + Fore.YELLOW + "*"
                    + Fore.GREEN + "]"
                    + f" IP lookup completed with {Fore.WHITE}{results_count}{Fore.GREEN} results" 
                    + Style.RESET_ALL,
                    flush=True
                )

                if args.output is not None:
                   with open(args.output, "w") as result_file:
                      for attribute, lookup_result in ip_data.items():
                         result_file.write(f"{attribute}: {lookup_result}\n")
                      result_file.write(f"\n[*] IP lookup completed with {results_count} results")

                elif args.folderoutput:
                    result_file = f"{ip_data['ip']}.txt"
                    os.makedirs(args.folderoutput, exist_ok=True) 
                    result_file = os.path.join(args.folderoutput, result_file)  

                    with open(args.output, "w") as result_file: 
                        for attribute, lookup_result in ip_data.items(): 
                            result_file.write(f"{attribute}: {lookup_result}\n")   
                        result_file.write(f"\n[*] IP lookup completed with {results_count} results")

    except KeyboardInterrupt:
        print(
            Fore.WHITE + Style.BRIGHT + "\n[" 
            + Fore.YELLOW + "-" 
            + Fore.WHITE + "]"
            + Fore.YELLOW + " Keyboard interrupt detected" 
            + Style.RESET_ALL 
        )
        print(
            Fore.GREEN + Style.BRIGHT + "["
            + Fore.YELLOW + "*"
            + Fore.GREEN + "]"
            + Fore.GREEN + " Exiting program..."
            + Style.RESET_ALL    
        )
        time.sleep(1.5)
        sys.exit(1)

if __name__ == "__main__":
    main()