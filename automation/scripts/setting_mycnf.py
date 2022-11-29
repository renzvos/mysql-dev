import os
import shutil

defaultloc = "/automation/mysqlcnfs/default.cnf"
lowram = "/automation/mysqlcnfs/lowram.cnf"


target = "/etc/my.cnf"
targetdir = "/etc/"

def main(option):
    if os.path.exists(target):
        os.remove(target)
    if option == "low-ram":
        print("Setting up Low-Ram Mode")
        shutil.copy(lowram,target)
    else:
        print("Setting up Default Mode")
        shutil.copy(defaultloc,target)


