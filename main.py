# Import
import threading
import time
import flask
import paramiko
from waitress import serve

ipAddr = "Not Yet Get"
host = "127.0.0.1"
user = "root"
port = 22

serverPort = 18088

app = flask.Flask(__name__)


@app.route('/getIP', methods=['GET'])
def getIP():
    return "The Ip address is: " + ipAddr


# SSH IP Query Thread
class QueryThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            # Try to catch paramiko exceptions
            try:
                global ipAddr
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                k = paramiko.RSAKey.from_private_key_file("./id")
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=user, port=port, pkey=k)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                    "ubus call network.interface.wan status | grep '\"address\"\: \"' | grep -oE '([0-9]{1,3}.){3}.[0-9]{1,3}'")
                ipAddr = ssh_stdout.read().decode("utf-8")
                # Add last update time
                ipAddr += "Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(ipAddr)
                time.sleep(1)
            except Exception:
                print("Error, Check The network connection OR the SSH key")
                time.sleep(1)


# A Thread to run the flask server
class FlaskThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print(self.name)
        serve(app, port=serverPort)


# Define the threads
flaskThread = FlaskThread("Flask Thread")
sshThread = QueryThread("SSH Thread")

if __name__ == '__main__':
    try:
        # Run the flask server in a thread
        flaskThread.start()
        # Run the SSH query in a thread
        sshThread.start()
        print("Done")
    # Catch Ctrl+C Key
    except KeyboardInterrupt:
        print("Exiting")
        # Stop the threads
        sshThread.join()
        flaskThread.join()
        print("Stopped")
        exit(0)
