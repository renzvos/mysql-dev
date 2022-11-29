import sys
import os
import zipfile
import shutil
import time
print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
from arsenal.dropbox_arsenal import DropboxArsenal
import dropbox_arsenal


class Arsenal:
    def __init__(self,workingDir="arsenal_files"):
        if not os.path.exists(workingDir):
            os.mkdir(workingDir)
            os.mkdir(workingDir +"/cache")
        self.cache = workingDir +"/cache/"
            

    def Download(self,connection,rename=None):
        if connection.cloud == "dropbox":
            if rename == None:
                DropboxArsenal.Download(connection)
            else:
                DropboxArsenal.Download(connection,rename)
        
    def DownloadLatest(self,connection,overwrite=False):
        print("Downloading latest")
        if connection.cloud == "dropbox":
            downloadedpath = DropboxArsenal.DownloadLatest(connection,self.cache)

        # Copy All of them
        self.Copy(downloadedpath,connection.local,overwrite)
 
            
        
    def RemoveLocalData(self,conn):
        for filename in os.listdir(conn.local):
            file_path = os.path.join(conn.local, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def HistoricalUpload(self,connection):
        print("Executing an Upload to " + connection.cloud)
        foldername  = str(int(time.time()))
        dropbox_arsenal.DropboxArsenal.HistoricalUpload(connection,foldername)
    

    def Copy(self, source ,destination, overwrite=False):
        if not os.path.exists(destination):
            os.mkdir(destination)
        for root, dirs, files in os.walk(source):
            cd = root[len(source) + 1:]
            destination_dir = os.path.join(destination, cd)
            if not os.path.exists(destination_dir):
                os.mkdir(destination_dir)  
            for filename in files:
                source_path = os.path.join(root, filename)
                destination_path = os.path.join(destination_dir, filename)
                if os.path.exists(destination_path):
                    if overwrite:
                        print("Overwriting   --  " + destination_path)
                        os.remove(destination_path)
                        shutil.copyfile(source_path , destination_path)
                        pass
                    else:
                        print("Skipping (Use Overwrite)   --  " + destination_path)
                else:
                    print("Copying   --  " + destination_path)
                    shutil.copyfile(source_path , destination_path)
                    pass
                             
