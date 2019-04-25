from tkinter import *
import subprocess
import socket
master = Tk() 
def get_ip():
    a= e1.get()
    t= e2.get()
    scan_ip(a, t)
    
def scan_ip(ip, total):
    for ping in range(1, int(total)): 
        address = str(ip) + str(ping) 
        res = subprocess.call(['ping', '-c', '3', address]) 
        if res == 0:  
            Label(master, text=("Enter an IP",address,"OK")).grid(row=ping+3) 
        elif res == 2: 
            Label(master, text=("No response from",address)).grid(row=ping+3) 
        else: 
            Label(master, text=("Ping to ",address," failed")).grid(row=ping+3)
            
Label(master, text="Enter an IP").grid(row=0) 
Label(master, text="Enter number of ports").grid(row=1)
e1 = Entry(master) 
e2 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1,  column = 1)
sub = Button(master, text = "Start Scan", command = get_ip)
sub.grid(row = 3, column = 1)

mainloop() 
