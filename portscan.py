import sys 
import socket 
import re

#check if target ip is in the right IPv4 format
regex = r"\b((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\b"

def is_valid_ip(ip):
    return bool(re.fullmatch(regex, ip))


args = sys.argv

print(args) #just for testing

if __init__ == "__main__":
    try:
        arg1 = arg[1]
        if len(args) == 2:
            if arg1 == "-h" or arg1 == "--help":
                print("Help on this tool : Usage : python ./portscan.py target_ip (IPv4 format) optional : port_min port_max (will only scan this range. Unspecified : scan from 0 to 65534.)")
                exit(1)
            if not is_valid_ip(arg1):
                print("Error : invalid target ip. Please use IPv4 format.")
                exit(1)
            else: 
                target_ip = arg1
        

    except Exception as e:
        print(f"Invalides arguments. Please refers to --help or -h. Error : {e}")
