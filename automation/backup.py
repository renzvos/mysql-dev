import os
from arsenal import Arsenal
from arsenal.connection import connection
import support
import getvars

config = getvars.getvars()



if(config['config_log_everysteps'] == "true"):logall = True
else:logall = False
cloud_dir = "/mysqlserver-one"
access = "un4M5SV-S6oAAAAAAAAAAf4uaRk4usNoEuOAx0hPTR5kOB2ZYr_UN9KKS6v9ble1"
conn = connection("mysql-server-dump",config["config_datadir"])
conn.dropbox(access,cloud_dir)
arsenal = Arsenal()
arsenal.RemoveLocalData(conn)
status = support.RunMySQLDump(config["config_datadir"] + "/data.sql",config["MYSQL_ROOT_PASSWORD"])
if status : arsenal.HistoricalUpload(conn)
else : print("Error on MYSQLDump")

