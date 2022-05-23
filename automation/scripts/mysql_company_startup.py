import subprocess
import sys


def main():
    print("Starting Microsoft's Startup File")
    cmd= '/automation/company_startup/entrypoint.sh'
    for arg in sys.argv[1:]:
        cmd = cmd + " " + arg    
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print(output.decode())