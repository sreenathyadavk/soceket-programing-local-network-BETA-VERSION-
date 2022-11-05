import json
import socket
import sys
import os

global conn_number
conn_number = 0
print('conn_number = 0')


def device_log(conn_device_log):
    global path
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'desktop/')
    resource_folder = "./Resources/"
    connected_log_dir = resource_folder + "Connected log/"
    device_directory = "Devices/"
    print('closed-log')
    device_data = json.loads(conn_device_log)
    global dn
    dn = str(device_data["hostname"])
    try:
        path = os.path.join(desktop + "/Resources/Connected log/Devices/", str(device_data["hostname"]))
        os.mkdir(path)
    except OSError as error:
        print(error)

    d = open(path + "/" + str(device_data["hostname"]) + ".json", "w")
    d.write(str(conn_device_log))
    d.close()
    print('f cl')


def create_socket():
    try:
        global s
        global host
        global device_name
        global port
        device_name = socket.gethostname()
        host = socket.gethostbyname(device_name)
        # host = "103.159.249.42"
        s = socket.socket()
        port = 9898
        print('Socket created')
        print('-----DEVICE-DETAILS-------')
        print('Device Name : ' + device_name)
        print('Device IP : ' + host)
        print('Current running port : ', port)
        print('---------------------------------------')
    except socket.error as msg:
        print('socket creation error : ' + str(msg) + '\n' + 'Retrying...')
        create_socket()


def bind_socket():
    try:
        global host
        global port
        global s
        global Addr
        global conn_number
        Addr = (host, port)
        print('Binding the port & host' + str(Addr))
        s.bind(Addr)
        conn_number = conn_number + 2
        s.listen(3)  # no . of connection , should accept , if limit reach out then Error
        print('Waiting of client...')
    except socket.error as msg:
        print(str(msg))


# global CONN_IMG
# CONN_IMG = False


def send_command(conn):
    respone_size = 40000
    line = 0
    # global conn_device_log

    print("***********************************TIPS***************************")
    print("1) TO EDIT EXISTING FILE OR CREATE NEW FILE AND WRITE DATA , TYPE -> 'edit' <- **[WITH OUT QUOTES , "
          "CASE SENSITIVE]")
    print("2) TO READ FILES , TYPE -> 'read' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
    print("3) TO GET DEVICE INFORMATION , TYPE ->'device_info <-'**' [WITH OUT QUOTES, CASE SENSITIVE]")
    print("3) TO EXIT , TYPE -> 'quit_app' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
    print("***********************************TIPS***************************")

    conn_device_log = conn.recv(2000).decode('utf-8')
    print('bytes 2000')
    device_log(conn_device_log)
    print(conn_device_log)
    while True:
        global CONN_IMG
        cmd = input('Send Command [CMD] : ')

        if cmd == 'quit_app':
            global CONN_IMG
            CONN_IMG = False
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(respone_size), 'utf-8')
            conn.close()
            print(client_response)
            sys.exit()
        if cmd == 'help':
            CONN_IMG = False
            print("***********************************HELP-COMMAND-CALLED***************************")
            print("1) TO EDIT EXISTING FILE OR CREATE NEW FILE AND WRITE DATA , TYPE -> 'edit' <- **[WITH OUT QUOTES , "
                  "CASE SENSITIVE]")
            print("2) TO READ FILES , TYPE -> 'read' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
            print("3) TO GET DEVICE INFORMATION , TYPE ->'device_info <-'**' [WITH OUT QUOTES, CASE SENSITIVE]")
            print("3) TO EXIT , TYPE -> 'quit_app' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
            print("***********************************HELP-COMMAND-CALLED***************************")

        if cmd == "copy_img":
            # Fname = input("Enter file name with in the local directory... [img response size changed to 10000000(10mb)] : ")
            conn.send(str.encode(cmd))
            CONN_IMG = True
            client_response = str(conn.recv(respone_size), 'utf-8')
         #   print(client_response)
            Fname = input(client_response)
            conn.send(str.encode(Fname))
            if s.recv(respone_size).__eq__("CI-000"):
                respone_size = 1000000000000000000000000000
               # respone_size=108000
                print(respone_size)
                s.send(str.encode("CI-000-accepted"))
                print('ci-00-acc')
                file_name = s.recv(respone_size).decode('utf-8')
                s.send(str.encode("ID-ACCEPTED"))
                print('id-acc')
                CI_DATA = s.recv(respone_size).decode('utf-8')
                print("SUCCESSFULLY RECEIVED CI_DATA...")
                # open(file_name,'w')
                print(CI_DATA)
                print(type(CI_DATA))
                print(file_name)

            # respone_size = 10000000
            # IMG_DATA = str(conn.recv(respone_size).decode('utf=8'))
            # print(IMG_DATA)
            # writter = open('xxx.txt', 'wb')
            # writter.write(bytes(IMG_DATA, encoding='utf8'))

        if len(str.encode(cmd)) > 0 and cmd != 'help':
            CONN_IMG = False
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(respone_size), 'utf-8')
            # client_response = str(conn.recv(20000),'utf-8')
            print("****************************WARNING**********************************")
            respone_size += 20000
            print("[RESPONSE SIZE]...", 'Current Max Bytes for This Response : ', respone_size, "....")
            print('Keep your Eye ...', 'This Response is Constantly updating by 20,000 Bytes per a single request: ',
                  respone_size)
            print("****************************WARNING**********************************")
            line += 1
            print('Response : ', client_response, "line : ", line)
        if CONN_IMG:
            pass

def socket_accept():
    conn, addr = s.accept()  # indirectly conn = socket
    print('Connection has been established! ' + 'IP : '
          + addr[0] + " | Port : " + str(addr))
    send_command(conn)
    conn.close()


def main():
    create_socket()
    bind_socket()
    socket_accept()


# if error the go again

# with open("bhagawad gita.jpg", "rb") as image:
#     f = image.read()
#     b = bytearray(f)
#     print(b[0])
#
while True:
    try:
        main()
    except OSError as er:
        print("MAIN----ERROR")
        print("RETRYING.....")
        print(str(er))
        main()
