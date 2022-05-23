from arsenal import dropbox
import os
class connection:
    def __init__(self,name,local_dir):
        self.name = name
        self.local = local_dir   
        if not os.path.exists(self.local):
            print("Folder does not exist - Creating Folder " + self.local)
            os.mkdir(self.local)

    def dropbox(self,access,cloud_dir):
        self.cloud = "dropbox"
        self.cloudpath = cloud_dir
        print("Creating a dropbox connection")
        self.client = dropbox.Dropbox(access)
