import re
import telnetlib
import getpass
import time

HOST = "192.168.1.1"
user = "admin"
password = "admin"

base_string = "VCC     Service         Interface       Proto.  IGMP    Src?    MLD     Src?    IPv4Status      IPv4            IPv6Status      IPv6           "
def get_positions(base_string):
    headers = re.split("\s+", base_string)
    positions = []
    for index, header in enumerate(headers):
        print("Index = %d" % index)
        if index < len(headers) - 1:
            position = base_string.index(header + "  ")
            print(position)
            obj = {}
            obj[header] = position
            print(obj)
            positions.append(obj)
        else:
            match = re.search("(.*\s+)" + re.escape(header) + "$", base_string)
            rest_length = len(match.group(1))
            obj = {}
            obj[header] = rest_length
            positions.append(obj)


    return positions

def get_pos(column):
    pos = get_positions(base_string)
    def get_item(key):
        pr1 = filter(lambda x: list(x[1].keys())[0] == key, enumerate(pos))
        return list(pr1)
    pr1 = get_item(column)
    index = pr1[0][0]
    start = pr1[0][1][list(pr1[0][1].keys())[0]]
    if (index + 1) < len(pos):
        pr2 = pos[index + 1][list(pos[index + 1].keys())[0]]
    else:
        pr2 = len(base_string) - 1
    return {
        "start": start,
        "end": pr2
    }
def get_val(needle, haystack):
    p = get_pos(needle)
    x1 = haystack[p['start']:p['end']]
    x2 = x1.strip()
    #print("x1111","'" + x2 + "'")
    return x2

def initiate_connection():
    tn = telnetlib.Telnet(timeout=10)
    tn.open(HOST)

    tn.read_until(b"Login: ")
    tn.write(user.encode("ascii") + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")
    return tn

def show_wan_services(tn):

    tn.write(b"wan show service\n")
    output1 = str(tn.read_until(b"FIN\n", timeout=2).strip())
    return output1
def get_current_services(tn, base_string):
    output1 = show_wan_services(tn)
    with open("ssh_output_1.txt", "w") as file_1:
        file_1.write(output1)
    data1 = re.sub(".*" + re.escape(base_string) + "\\s+?\\\\r\\\\n", "", output1)
    data2 = re.split("\\\\r\\\\n", data1)
    ret = []
    for index, data in enumerate(data2):
        if index < len(data2) - 1 and index > 0:
            protocol = get_val("Proto.", data2[index])
            interface = get_val("Interface", data2[index])
            ret.append({
                "protocol": protocol,
                "interface": interface
            })
    return ret


def check_and_configure_service(service):
    tn = initiate_connection()
    services = get_current_services(tn, base_string)
    print("services:")
    print(services)
    if len(services) == 1:
        if services[0]['protocol'] == service:
            print(service + " already configured")
            return True
        else:
            print("Currently " + services[0]['protocol'] + " is in use")
            if service == "IPoE":
                print("Adding Service DHCP")
                add_service_dhcp(tn)
                print("Deleting Service PPPoE")
                delete_service(tn, "PPPoE", services)
            else:
                print("Adding Service PPPoE")
                add_service_pppoe(tn)
                print("Deleting Service DHCP")
                delete_service(tn, "IPoE", services)
    elif len(services) == 2:
        if service == "IPoE":
            print("Deleting Service PPPoE")
            delete_service(tn, "PPPoE", services)
        else:
            print("Deleting Service DHCP")
            delete_service(tn, "IPoE", services)
    else:
        print("----------- UNEXPECTED NUMBER OF SERVICES FOUND -----------")

    tn.close()
    return "end_of_function"

def add_service_pppoe(tn):
    command = "wan add service veip0 --protocol pppoe --username clear --password access"
    command = bytes(command, "utf8")
    tn.write(b"" + command + b"\n")
    time.sleep(10)
    return "end_of_function"

def delete_service(tn, service, current_services):
    service_object_list = list(filter(lambda s:s["protocol"] == service, current_services))
    if len(service_object_list) > 0:
        command = "wan delete service " + service_object_list[0]["interface"]
        command = bytes(command, "utf8")
        tn.write(b"" + command + b"\n")
    time.sleep(10)
    return "end_of_function"


def add_service_dhcp(tn):
    command = "wan add service veip0 --protocol ipoe --dhcpclient enable"
    command = bytes(command, "utf8")
    tn.write(b"" + command + b"\n")
    time.sleep(10)
    return "end_of_function"

