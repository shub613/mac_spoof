# MAC Spoof

Random MAC Address Spoofer For Linux System which also checks networking is working or not after changing MAC Address

## Getting Started

These instructions will guide you to run the script on your local machine for development and testing and usage. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

#####Python 2.7

re

subprocess

random

### Deployment

Find the interface names from running 'ifconfig' command from terminal and choose the right interface to spoof the MAC Address.

Open mac.py file and set your interface name in 'DEVICE_NAME' variable and set your desired hostname to ping for 
working internet in 'HOSTNAME' variable
#### Example
DEVICE_NAME = 'eth0'

HOSTNAME = '8.8.8.8'

### Running

* Run with superuser privileges

sudo python mac.py

### Built With

* Python 2.7 - The language used
* random - For generation of random MAC Address
* re module  - For checking validity of MAC Address generated
* subprocess - To run the OS Commands in separate process

### Version

1.1

## Authors

* Miller - *Initial work*

