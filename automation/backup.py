#!/usr/bin/python3

import os
from arsenal import Arsenal
from arsenal.connection import connection
import support
import getvars

config = getvars.getvars()
arsenal = Arsenal()

def backup():
    if(config['config_log_everysteps'] == "true"):logall = True
    else:logall = False
    conns = []
    for item,val in config.items():
        if item.startswith("backup_data_") and item.endswith("_destination"):
            name = support.backupname_regex(item)
            if name == False:
                print("Couldnt parse backup name")
            else:
                if config['backup_data_' + name + '_destination'] == "dropbox":
                    print("Found Backup Delivery Location named " + name + " to Dropbox" )
                    cloud_dir = config['backup_data_' + name + '_dropbox_dir']
                    access = config['backup_data_' + name + '_dropbox_access']
                    conn = connection("mysql-server-dump",config["config_datadir"])
                    conn.dropbox(access,cloud_dir)
                    conns.append(conn)


    for conn in conns:
        print("Executing a Backup")
        arsenal.RemoveLocalData(conn)
        status = support.RunMySQLDump(config["config_datadir"] + "/data.sql", "backupclient" , config["MYSQL_ROOT_PASSWORD"])
        if status : arsenal.HistoricalUpload(conn)
        else : print("Error on MYSQLDump")

if __name__ == "__main__":
    backup()