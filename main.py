# Import
import threading
import time
import flask
from flask import render_template
from flask_cors import CORS, cross_origin
import paramiko
from waitress import serve

ipAddr = "Not Yet Get"
lastUpdate = "null"
host = "127.0.0.1"
user = "root"
port = 22

serverPort = 18088

app = flask.Flask(__name__,
            static_folder='./static',
            template_folder='./templates')


# Solve CORS https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def getIP():
    return render_template("index.html")

@app.route('/getIP', methods=['POST'])
def getIPAddr():
    return ipAddr

@app.route('/getLastDate', methods=['POST'])
def getLastDate():
    return lastUpdate

# SSH IP Query Thread
class QueryThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            # Try to catch paramiko exceptions
            try:
                # Declare the global variable
                global ipAddr
                global lastUpdate
                # Start SSH
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                k = paramiko.RSAKey.from_private_key_file("./id")
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=user, port=port, pkey=k)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                    "ubus call network.interface.wan status | grep '\"address\"\: \"' | grep -oE '([0-9]{1,3}.){3}.[0-9]{1,3}'")
                ipAddr = ssh_stdout.read().decode("utf-8")
                # Add last update time
                lastUpdate = "Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(ipAddr+lastUpdate)
                time.sleep(30)
            except Exception:
                print("Error, Check The network connection OR the SSH key")
                time.sleep(30)


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
