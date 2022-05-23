from main import init
from scripts import mysql_company_startup
from main import init,looper
import threading

print("Starting RENZVOS SERVER")

server_thread = threading.Thread(target=mysql_company_startup.main, args=())
automation_init = threading.Thread(target=init, args=())
automation_looping = threading.Thread(target=looper, args=())

server_thread.start()
automation_init.start()
automation_looping.start()

server_thread.join()
automation_init.join()

print("Exiting RENZVOS SERVER")