import sys 
import socket 
import re
import threading
from datetime import datetime


#check if target ip is in the right IPv4 format
regex = r"\b((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\b"

def is_valid_ip(ip):
    return bool(re.fullmatch(regex, ip))

args = sys.argv

#Using sockets : 

def scan_port(target_ip, port, display_banner, results, banners):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)  # Timeout pour éviter de bloquer
        test = s.connect_ex((target_ip, port))

        if test == 0:
            results[port] = f'Port {port} is \033[32m[open]\033[0m'

            if display_banner:
                try:
                    banner = s.recv(1024).decode().strip()

                    if banner:
                        str_banner = f"\nOn port {port} :\n"
                        
                        # Si la réponse est un JSON ou ressemble à un dictionnaire
                        if "{" in banner and "}" in banner:
                            import json
                            try:
                                banner_dict = json.loads(banner)  # Convertir en dict
                                for key, value in banner_dict.items():
                                    str_banner += f"{key} : \033[31m{value}\033[0m\n"
                            except json.JSONDecodeError:
                                str_banner += f"\033[31m{banner}\033[0m\n"
                        else:
                            str_banner += f"\033[31m{banner}\033[0m\n"

                        banners[port] = str_banner
                    else:
                        banners[port] = f"On port {port} : Unable to retrieve banner"

                except Exception as e:
                    banners[port] = f"On port {port} : Error retrieving banner - {e}"


        

#Principal function : using multithread to optimize the search.
def portscanner(target_ip, port_range, display_banner):
    print(f"Scanning target --> {target_ip} on port range {port_range}")

    thread_list = []
    results = {}  
    banners = {}

    try :
        start_time = datetime.now()

        for port in range(port_range[0], port_range[1] + 1):
            scan = threading.Thread(target=scan_port, args=(target_ip, port, display_banner, results, banners))
            thread_list.append(scan)
            scan.start()
        
        for scan in thread_list:
            scan.join()
        
        end_time = datetime.now()

        
        for port in sorted(results.keys()):
            print(results[port])
            print(banners[port])

        print(f"Port scanning ended in {end_time - start_time}.")

    except Exception as e:
        print(f"Something went wrong. Please refer to --help/-h. Error : {e}.")
try:
    arg1 = args[1]
    if len(args) == 2:
        if arg1 == "-h" or arg1 == "--help":
            print("Help on this tool : Usage : python ./portscan.py target_ip (IPv4 format). optional : port_min port_max (will only scan this range. Unspecified : scans from 0 to 65535.) -b or --banner : show infos about the running service.")
            exit(1)
        if not is_valid_ip(arg1):
            print("Error : invalid target ip. Please use IPv4 format.")
            exit(1)
        else: 
            target_ip = arg1

    target_ip = args[1]
    if not is_valid_ip(target_ip):
        print("Error : invalid target ip. Please use IPv4 format.")
        exit(1)

#optional arguments gestion
    min_presence, max_presence, showall = False, False, False

    if len(args) > 5:
        print("Too much arguments. Please refer to --help or -h.")
    
    try: 
        min_port = int(args[2])
        if not min_port >= 0 or not min_port <= 65535:
            print("Error : minimal port (optional argument) is not in port range. Please refer to --help or -h.")
            exit(1)
        min_presence = True

    except:
        pass

    if min_presence:
        try:
            max_port = int(args[3])
            if not max_port >= 0 or not max_port <= 65535:
                print("Error : maximal port (optional argument) is not in port range. Please refer to --help or -h.")
                exit(1)
            max_presence = True

        except:
            pass

#show argument place prediction.
    if min_presence and max_presence: 
        s_place = 4
    elif min_presence and not max_presence:
        s_place = 3
    else:
        s_place = 2

    try:
        banner_arg = args[s_place]
        if not banner_arg == '-b' and not banner_arg == '--banner':
            print("Error : invalid last argument. Please refer to --help/-h.")
        else:
            display_banner = True
    except:
        pass


    port_range = [0 if not min_presence else min_port, 65535 if not max_presence else max_port]

#execution of our fonction : 

    if __name__ == "__main__":
        portscanner(target_ip, port_range, display_banner)

except Exception as e:
    print(f"Invalids arguments. Please refer to --help or -h. Error : {e}")


#To Do : 
#Remove the -s arg : was only here for test purpose.
#Add banner grabbing : display informations about the service running on a port. 
#Add a function to use a list of ip instead of only one each time.