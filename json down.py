import json
import socket
import os

ip = socket.gethostbyname(socket.gethostname())

data = {
    "ip": "0.45.068.102",
    "ip2": "fluff.fd5frt0"
}
print(data)
data['ip'] = ip
print(data.get("ip"))
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "/"
print(desktop)
directory = "Connected log"

# Parent Directory path
#
# Path
path = os.path.join(desktop, directory)
print(path)
# Create the directory
# 'GeeksForGeeks' in
'/home / User / Documents'
os.mkdir(path)
print("Directory '% s' created" % directory)
cr = open(path + "\kanna pc.txt", "w")
cr.write(str(data))
cr.writelines(desktop + "\n" + ip)

# r = open("ip_save.json" , 'r')
# de = {}
# de = r.read(100)
# # json.
# print(de[0])