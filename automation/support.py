import subprocess
import os
import re

def RunSQLFile(filename , username , password):
    CreateDumpConfig(password)
    print("Restoring from " + filename)
    p = subprocess.Popen(['mysql --defaults-file=/dumpconf.cnf -u '+ username +' < ' + filename], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output)
    if output.decode() == "" and err == None:
        return True
    else:
        return False

def RunMySQLDump(location,username,password):
    CreateDumpConfig(password)
    print("Executing a MYSQL Dump")
    p = subprocess.Popen(['mysqldump --defaults-file=/dumpconf.cnf -u '+username+' --all-databases --no-tablespaces --no-create-info -f >' + location], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output)
    if output.decode() == "" and err == None:
        return True
    else:
        return False

def CreateDumpConfig(password):
    print("Creating Dump Config")
    if not os.path.exists("/dumpconf.cnf"):
        fp = open('/dumpconf.cnf', 'w')
        fp.write("[mysql]\n" )
        fp.write("password="+password + "\n")
        fp.write("[mysqldump]\n" )
        fp.write("password="+password + "\n")
        fp.close()

def backupname_regex(item):
    r = re.compile('backup_data_(.*?)_destination')
    m = r.search(item)
    if m:
        projectname = m.group(1)
        return projectname
    else:
        return False