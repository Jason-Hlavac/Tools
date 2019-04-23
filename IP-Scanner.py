import subprocess
import socket
log = []
answer = input(""" Please select a corresponding number:
1)Enter an IP Adress
2)Enter a website URL to scan
""")
  
def scan(ip):
    print("=" * 40)
    total = input("Please enter a max iteration range: ")
    for ping in range(1, int(total)): 
        address = str(ip) + str(ping) 
        res = subprocess.call(['ping', '-c', '3', address]) 
        if res == 0: 
            print( "ping to", address, "OK") 
        elif res == 2: 
            print("no response from", address) 
        else: 
            print("ping to", address, "failed!") 
def get_IP(host):
    ip = socket.gethostbyname(host)
    return ip
    
if (int(answer) == 1):
    print ("=" *40)
    adress = input("Please enter an IP adress: ")
    print ("=" *40)
    scan(adress)
    
elif(int(answer) == 2):
    print ("=" *40)
    url = input("Please enter a URL: ")
    print ("=" *40)
    ip = get_IP(url)
    scan(ip)
else:
    print ("=" *40)
    print("That is not a valid input")
    print ("=" *40)
