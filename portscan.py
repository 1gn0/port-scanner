import sys 
import socket 
import re

#check if target ip is in the right IPv4 format
regex = r"\b((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\b"

def is_valid_ip(ip):
    return bool(re.fullmatch(regex, ip))

args = sys.argv

#Principal function used : 
def portscan(target_ip, port_range):
    pass


try:
    arg1 = args[1]
    if len(args) == 2:
        if arg1 == "-h" or arg1 == "--help":
            print("Help on this tool : Usage : python ./portscan.py target_ip (IPv4 format). optional : port_min port_max (will only scan this range. Unspecified : scans from 0 to 65534.)")
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

#optionals arguments gestion
    min_presence, max_presence = False, False

    if len(args) > 4:
        print("Too much arguments. Please refer to --help or -h.")
    
    try: 
        min_port = int(args[2])
        if not min_port >= 0 or not min_port <= 65354:
            print("Error : minimal port (optional argument) is not in port range. Please refer to --help or -h.")
            exit(1)
        min_presence = True

    except:
        pass

    if min_presence:
        try:
            max_port = int(args[3])
            if not max_port >= 0 or not max_port <= 65354:
                print("Error : maximal port (optional argument) is not in port range. Please refer to --help or -h.")
                exit(1)
            max_presence = True

        except:
            pass

    port_range = [0 if not min_presence else min_port, 65534 if not max_presence else max_port]

    #execution of our fonction : 

    if __name__ == "__main__":
        portscan(target_ip, port_range)

except Exception as e:
    print(f"Invalids arguments. Please refer to --help or -h. Error : {e}")
