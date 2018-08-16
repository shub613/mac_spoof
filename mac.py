import sys
import os
import re
import random
import subprocess
from time import sleep

__version__ = '1.0'
# Return Codes
SUCCESS = 200

DEVICE_NAME = 'enp2s0'
HOSTNAME = "8.8.8.8"

MAC_ADDRESS_R = re.compile(r"""
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})
    """,
                           re.I | re.VERBOSE
                           )


def random_mac_address(local_admin=False):
    """
    Generates and returns a random MAC address.
    """
    # Randomly assign a VM vendor's MAC address prefix, which should
    # decrease chance of colliding with existing device's addresses.
    vendor = random.SystemRandom().choice((
        (0x00, 0x05, 0x69),  # VMware MACs
        (0x00, 0x50, 0x56),  # VMware MACs
        (0x00, 0x0C, 0x29),  # VMware MACs
        (0x00, 0x16, 0x3E),  # Xen VMs
        (0x00, 0x03, 0xFF),  # Microsoft Hyper-V, Virtual Server, Virtual PC
        (0x00, 0x1C, 0x42),  # Parallells
        (0x00, 0x0F, 0x4B),  # Virtual Iron 4
        (0x08, 0x00, 0x27))  # Sun Virtual Box
    )

    mac = [
        vendor[0],
        vendor[1],
        vendor[2],
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]

    if local_admin:
        # Universally administered and locally administered addresses are
        # distinguished by setting the second least significant bit of the
        # most significant byte of the address. If the bit is 0, the address
        # is universally administered. If it is 1, the address is locally
        # administered. In the example address 02-00-00-00-00-01 the most
        # significant byte is 02h. The binary is 00000010 and the second
        # least significant bit is 1. Therefore, it is a locally administered
        # address.[3] The bit is 0 in all OUIs.
        mac[0] |= 2

    return ':'.join('{0:02X}'.format(o) for o in mac)


def check_ping():
    response = os.system("ping -c 1 " + HOSTNAME)
    print(response)
    return response


def set_interface_mac(device, mac):
    """
    Set the device's mac address.  Handles shutting down and starting back up interface.
    """
    # turn off device
    cmd = "ip link set {} down".format(device)
    subprocess.call(cmd.split())
    print('Shutting Down Interface...')
    sleep(1)
    # print (cmd)
    # set mac
    cmd = "ip link set {} address {}".format(device, mac)
    subprocess.call(cmd.split())
    print('Setting MAC Address....!!!')
    sleep(1)
    # print (cmd)
    # turn on device
    cmd = "ip link set {} up".format(device)
    subprocess.call(cmd.split())
    print('Switching ON Interface...')
    sleep(1)
    # print (cmd)


print("This is the MAC Address generated for you---")
mac_address = random_mac_address()
print(mac_address)
set_interface_mac(DEVICE_NAME, mac_address)

while 1:
    if not check_ping():
        print('SUCCESS!!')
        sys.exit()
    else:
        sleep(1)
        command = "ip link set {} up".format(DEVICE_NAME)
        subprocess.call(command.split())
        command = "service network restart"
        subprocess.call(command.split())
