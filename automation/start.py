import os
import sys
from scripts import mysql_company_startup
import main
import threading
import signal
import scripts.setting_mycnf
from getvars import getvars
config = getvars()

print("Starting RENZVOS SERVER")

server = mysql_company_startup.MICROSOFTSQL()
automation = main.Automation()


scripts.setting_mycnf.main(config["config_mysql_type"])
server_thread = threading.Thread(target=server.main, args=())
automation_init = threading.Thread(target=automation.init, args=())


def onStop(signal,frame):
    import backup
    backup.backup()
    print("Gracefully closed server")
    os._exit(0)
    




signal.signal(signal.SIGTERM, onStop)

server_thread.start()
automation_init.start()





