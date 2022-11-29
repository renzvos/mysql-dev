import subprocess
import sys

class MICROSOFTSQL:
    def terminate(self):
        self.p.kill()

    def main(self):
        print("Starting Microsoft's Startup File")
        cmd= '/automation/company_startup/entrypoint.sh'
        for arg in sys.argv[1:]:
            cmd = cmd + " " + arg    
        self.p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        (output, err) = self.p.communicate()  
        p_status = self.p.wait()
        print(output.decode())
        print("Microsoft MYSQL is no longer running")