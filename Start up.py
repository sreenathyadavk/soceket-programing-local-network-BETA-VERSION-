import os
import platform, socket, re, uuid, json, logging
import ctypes
import psutil
import time


def sys_info():
    global sys_info_

    create_log(sys_info_json=sys_info_)


def getSystemInfo():
    # print(str('ram :' + str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"))#out  , remove
    try:
        info = {
            '"platform"': platform.system(), '"platform-release"': platform.release(),
            '"platform-version"': platform.version(), '"architecture"': platform.machine(),
            '"hostname"': socket.gethostname(), '"ip-address"': socket.gethostbyname(socket.gethostname()),
            '"mac-address"': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            '""processor""': platform.processor(),
            '"ram"': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        }
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

    # startup_log_js = open(resource_folder + "startup.json", "w")
    # startup_log = open(resource_folder + "startup.txt" ,"w")


def create_log(Device_path, sys_info_json):
    startup_log_js = open(Device_path + "startup.json", "w")
    startup_log = open(Device_path + "startup.txt", "w")
    welcome_file = open(Device_path + "Welcome to kHack.txt", "w")
    global settings
    settings = {
        "start_up": "False",
        "device_directory": ("" + Device_path),
        "connected_log_dir": connected_log_dir,
        "SYSTEM_INFORMATION": sys_info_json
    }

    try:
        startup_log_js.write(str(json.dumps(settings)))
        startup_log.write("start up successfully completed with out any errors...")
        welcome_file.write("Welcome to kHack....." + "\n" + "Warning : This is only for Local Network....")
        startup_log.close()
        startup_log_js.close()
        welcome_file.close()
    except:
        startup_log_js.close()
        startup_log.close()
        print("----SOME OPERATIONS ARE FAILED IN THIS DEVICE-----TRY AGAIN , BY DELETING ALL LOG FILES IN THIS "
              "DIRECTORY")


print("---------------WELCOME--TO--START-UP--CHECK-------------")
print("THIS PROCESS WILL START IN FEW SECONDS")
#
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'desktop/')
print("------------------GATHERING REQUIRE FILES------------------")
resource_folder = "Resources/"
connected_log_dir = desktop + resource_folder + "Connected log/"
Res_path = os.path.join(desktop, resource_folder)
# os.mkdir(Res_path)
Connected_log_directory = "Connected log/"
Conn_log_path = os.path.join(desktop + resource_folder, Connected_log_directory)
# os.mkdir(Conn_log_path)
Device_log_dir = "Devices/"
Device_path = os.path.join(desktop + resource_folder + Connected_log_directory, Device_log_dir)
# os.mkdir(Device_path)
print("------------LOGGING THE REQUIRED FILES ------ PLEASE WAIT FOR FEW SECONDS---------------")
try:
    os.mkdir(Res_path)
except OSError as msg:
    ar = "It's look's like there is already a resources folder is present in your Desktop ," \
         + '\n' + "For star up " \
                  "check , " \
                  "you need to " \
                  "move the resource folder to " \
                  "another directory , Try Again" + "\n" + str(msg)
    ctypes.windll.user32.MessageBoxW(0, ar, "ERROR", 1)
    exit()
try:
    os.mkdir(Conn_log_path)
    os.mkdir(Device_path)
except OSError as msg_:
    ctypes.windll.user32.MessageBoxW(0, str(msg_), "ERROR", 1)

print("------GATHERING YOUR SYSTEM INFORMATION------")
sys_info_ = getSystemInfo()
create_log(Device_path, sys_info_)
print("---------********************START UP PROGRESS IS OVER******************-----------")
print("    ************            HAPPY HACKING  :)      **********")
time.sleep(6)
exit()