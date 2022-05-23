import subprocess
import os

def RunSQLFile(filename , password):
    print("Creating Dump Config")
    if not os.path.exists("/dumpconf.cnf"):
        fp = open('/dumpconf.cnf', 'w')
        fp.write("[mysql]\n" )
        fp.write("password="+password)
        fp.close()
    print("Restoring from " + filename)
    p = subprocess.Popen(['mysql --defaults-file=/dumpconf.cnf -u root < ' + filename], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output)
    if output.decode() == "" and err == None:
        return True
    else:
        return False

def RunMySQLDump(location,password):
    print("Creating Dump Config")
    if not os.path.exists("/dumpconf.cnf"):
        fp = open('/dumpconf.cnf', 'w')
        fp.write("[mysqldump]\n" )
        fp.write("password="+password)
        fp.close()
    print("Executing a MYSQL Dump")
    p = subprocess.Popen(['mysqldump --defaults-file=/dumpconf.cnf -u root --all-databases > ' + location], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output)
    if output.decode() == "" and err == None:
        return True
    else:
        return False
