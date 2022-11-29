
import imp
from arsenal_support import FindLatest
from dropbox_arsenal.support import Dropbox_MakeFilesFolderList
from dropbox_arsenal.support import RemoveSourceFromAddress
import os
import zipfile
import shutil

class DropboxArsenal:


    def DownloadLatest(connection,cache):
        print("Executing Dropbox download")
        response = connection.client.files_list_folder(path=connection.cloudpath)
        print(FindLatest(Dropbox_MakeFilesFolderList(response)))
        latest = FindLatest(Dropbox_MakeFilesFolderList(response))
        cloudpath = connection.cloudpath + '/' + latest
        if not os.path.exists(cache + connection.name):
            os.mkdir(cache + connection.name)
        print("Downloading from folder " + cloudpath)
        connection.client.files_download_zip_to_file(cache + connection.name + "/!data.zip", cloudpath)
        try:
            with zipfile.ZipFile(cache + connection.name + "/!data.zip") as z:
                z.extractall(cache + connection.name)
                print("Extracted all")
        except:
            print("Invalid ZIP file to extract")
        latestdir = cache + connection.name + "/" + FindLatest(os.listdir(cache + connection.name))

        return latestdir
    

    def HistoricalUpload(connection,epochtime):
        locallist = []
        for root, dirs, files in os.walk(connection.local):
            for filename in files:
                local_path = os.path.join(root, filename)
                addr = RemoveSourceFromAddress(connection.local, local_path)
                locallist.append(addr)

        print(files)
        for addr in files:
            print(addr)
            localpath = os.path.join(connection.local,addr)
            print(localpath)
            dbd = connection.cloudpath + '/' + epochtime
            dropbox_path = os.path.join(dbd, addr).replace('\\','/')
            with open(localpath, 'rb') as f:
               print("Real Link " + localpath)
               print("Dropbox Link " + dropbox_path)
               connection.client.files_upload(open(local_path, "rb").read(), dropbox_path)
               pass
    
    def Download(connection,rename=None):
        if rename != None:
            localpath = os.path.join(connection.local,rename)
        else:
            filename = os.path.basename(connection.cloudpath)
            localpath = os.path.join(connection.local,filename)
        print("Cloud Path " + connection.cloudpath)
        print("Initiating Dropbox Download " + connection.name )
        print("Saving to Local Path " + localpath)
        with open(localpath, "wb") as f:
            metadata, res = connection.client.files_download(path=connection.cloudpath)
            print(res.content.decode())
            f.write(res.content)
            f.close()
        