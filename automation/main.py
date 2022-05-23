import time
import mysql.connector
from arsenal import Arsenal
from arsenal.connection import connection
import support
from getvars import getvars

config = getvars()
arsenal = Arsenal()

def init():
    print("Doing a Latest Import from Dropbox")
    cloud_dir = "/mysqlserver-one"
    access = "un4M5SV-S6oAAAAAAAAAAf4uaRk4usNoEuOAx0hPTR5kOB2ZYr_UN9KKS6v9ble1"
    conn = connection("mysql-server-dump",config["config_datadir"])
    conn.dropbox(access,cloud_dir)
    arsenal.RemoveLocalData(conn)
    arsenal.DownloadLatest(conn,overwrite=True)
    serverready = False
    while not serverready:
        try:
            mysqlc = mysql.connector.connect(host="localhost",user=config["MYSQL_USER"],password=config["MYSQL_PASSWORD"])
            mysqlc.close()
            print("Server Ready")
            serverready = True
            OnServerReady(conn)
        except Exception as e:
            print("RENZVOS - Waiting for Server -- " + str(e))
        time.sleep(3)
    
    


def OnServerReady(conn):
    print("Restoring")
    support.RunSQLFile(config["config_datadir"] + "/data.sql" , config["MYSQL_ROOT_PASSWORD"])
    while True:
        print("Backing up within next " + str(84600) + "seconds")
        time.sleep(86400)
        arsenal.RemoveLocalData(conn)
        status = support.RunMySQLDump(config["config_datadir"] + "/data.sql",config["MYSQL_ROOT_PASSWORD"])
        if status : arsenal.HistoricalUpload(conn)
        else : print("Error on MYSQLDump")




def looper():
    pass