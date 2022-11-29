import time
from getvars import getvars
config = getvars()
if not config["dev"]:
    import mysql.connector
import os
from arsenal import Arsenal
from arsenal.connection import connection
import support
import sys

class Automation:
    def __init__(self) -> None:
        self.arsenal = Arsenal()
    
    def terminate(self):
        sys.exit()

    def init(self):
        if(config["startup_restore_structure"] == "true"):
            print("Restoring Structure")
            if(config["startup_restore_structure_source"] == "dropbox"):
                cloud_dir = config['startup_restore_structure_dropbox_dir']
                access = config['startup_restore_structure_dropbox_access']
                conn = connection("mysql-server-structure",config["config_structuredir"])
                conn.dropbox(access,cloud_dir)
                self.arsenal.RemoveLocalData(conn)
                self.arsenal.Download(conn,"structure.sql")
            if(config["startup_restore_structure_source"] == "local_volume"):
                print("Restoring from Volume")
                pass


        if(config["startup_restore_data"] == "true"):
            if(config["startup_restore_data_source"] == "dropbox"):
                print("Doing a Latest Import from Dropbox")
                cloud_dir = config['startup_restore_data_dropbox_dir']
                access = config['startup_restore_data_dropbox_access']
                conn = connection("mysql-server-dump",config["config_datadir"])
                conn.dropbox(access,cloud_dir)
                self.arsenal.RemoveLocalData(conn)
                self.arsenal.DownloadLatest(conn,overwrite=True)

        serverready = False
        while not serverready:
            try:
                mysqlc = mysql.connector.connect(host="localhost",user=config["MYSQL_USER"],password=config["MYSQL_PASSWORD"])
                mysqlc.close()
                print("Server Ready")
                serverready = True
                self.OnServerReady(config["startup_restore_structure_source"])
            except Exception as e:
                print("RENZVOS - Waiting for Server -- " + str(e))
            time.sleep(3)
        
        


    def OnServerReady(self, struct_source ):
        if not os.path.exists("/restoreflag"):
            if(struct_source == "dropbox"):
                print("Restoring Structure from Dropbox")
                result = support.RunSQLFile(config["config_structuredir"] + "/structure.sql" , "root" ,  config["MYSQL_ROOT_PASSWORD"])
                if(result == False) : exit()
            if(struct_source == "local_volume"):
                print("Restoring Structure From Local Volume")
                result = support.RunSQLFile(config["startup_restore_structure_local_path"], "root" ,  config["MYSQL_ROOT_PASSWORD"])
                if(result == False) : exit()

            if(config["startup_restore_data"] == "true"):
                if(config["startup_restore_data_source"] == "dropbox"):
                    print("Restoring Data")
                    support.RunSQLFile(config["config_datadir"] + "/data.sql" , "root" ,  config["MYSQL_ROOT_PASSWORD"])
                fp = open('/restoreflag', 'w')
                fp.write("ok")
                fp.close()
        else:
            print("Already restored")

        while True:
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

            print("Backing up within next " + config["backup_data_interval"] + "seconds")
            time.sleep(int(config["backup_data_interval"]))

            for conn in conns:
                print("Executing a Backup")
                self.arsenal.RemoveLocalData(conn)
                status = support.RunMySQLDump(config["config_datadir"] + "/data.sql", "backupclient" , config["MYSQL_ROOT_PASSWORD"])
                if status : self.arsenal.HistoricalUpload(conn)
                else : print("Error on MYSQLDump")



