# wpa_cli_py
A collection of python scripts to interact with wpa_supplicant.

The purpose of this scripts collection is to simplify the use and configuration of wpa_supplicant.

## Install

To install the library just execute:
    
    sudo ./install.sh
    
This will copy the python script in /sbin/ removing the .py extension and adjust the files permission to make them executable.


## Prerequisites

Prerequisites for the scripts to work are:

1) the file: 
    
        /etc/wpa_supplicant/wpa_supplicant.conf
    
    need to contain these configuration params:
    
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1

2) the user calling the script need to be part of the group:
    
        netdev



## Commands description


    wpa_cli_py -h
    usage: wpa_cli_py.py [-h] ifname command [params [params ...]]
    
    Send command directly to wpa_supplicant. Similar to wpa_cli, but command line
    only.
    
    positional arguments:
      ifname      Specify the interface that is being configured.
      command     Run a command. See wpa_cli manual for all the possible options.
      params      Command params. See wpa_cli manual for all the possible options.
    
    optional arguments:
      -h, --help  show this help message and exit

-----
  
    wpa_cli_py_connect_to_network -h
    usage: wpa_cli_py_connect_to_network.py [-h] ifname idNetwork
    
    Force wpa_supplicant to connect to a specific network.
    
    positional arguments:
      ifname      Specify the interface that is being used.
      idNetwork   Specify the network id to connect to.
    
    optional arguments:
      -h, --help  show this help message and exit
  
---

    wpa_cli_py_create_network -h
    usage: wpa_cli_py_create_network.py [-h] [-s SSID] [-b BSSID] [-P PASSWORD]
                                        [-r PRIORITY] [-e]
                                        [-k {WPA-PSK,WPA-EAP,NONE,WPA-NONE,FT-PSK,FT-EAP,FT-EAP-SHA384,WPA-PSK-SHA256,WPA-EAP-SHA256,SAE,FT-SAE,WPA-EAP-SUITE-B,WPA-EAP-SUITE-B-192,OSEN,FILS-SHA256,FILS-SHA384,FT-FILS-SHA256,FT-FILS-SHA384,OWE,DPP}]
                                        [-I IDENTITY]
                                        [-E {PEAP,TLS,TTLS,PWD,SIM,AKA,AKA,FAST,LEAP}]
                                        ifname {OPEN,WEP,WPA,WPA2,EAP}
    
    Set WIFI connection parameters using wpa_supplicant. For more information see:
    https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf
    
    positional arguments:
      ifname                Specify the interface that is being used.
      {OPEN,WEP,WPA,WPA2,EAP}
                            Specify the protocol used by the wifi network. Needed
                            to setup the required parameters.
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SSID, --ssid SSID  The SSID of the network.
      -b BSSID, --bssid BSSID
                            The BSSID of the network.
      -P PASSWORD, --password PASSWORD
                            The network password. Converted in the right
                            parameters needed by the network protocol.
      -r PRIORITY, --priority PRIORITY
                            The network priority.
      -e, --enabled         Enable the network.
      -k {WPA-PSK,WPA-EAP,NONE,WPA-NONE,FT-PSK,FT-EAP,FT-EAP-SHA384,WPA-PSK-SHA256,WPA-EAP-SHA256,SAE,FT-SAE,WPA-EAP-SUITE-B,WPA-EAP-SUITE-B-192,OSEN,FILS-SHA256,FILS-SHA384,FT-FILS-SHA256,FT-FILS-SHA384,OWE,DPP}, --keyMgmt {WPA-PSK,WPA-EAP,NONE,WPA-NONE,FT-PSK,FT-EAP,FT-EAP-SHA384,WPA-PSK-SHA256,WPA-EAP-SHA256,SAE,FT-SAE,WPA-EAP-SUITE-B,WPA-EAP-SUITE-B-192,OSEN,FILS-SHA256,FILS-SHA384,FT-FILS-SHA256,FT-FILS-SHA384,OWE,DPP}
                            EAP type for EAP connections. See: https://w1.fi/cgit/
                            hostap/plain/wpa_supplicant/wpa_supplicant.conf
      -I IDENTITY, --identity IDENTITY
                            Identity for EAP connections.
      -E {PEAP,TLS,TTLS,PWD,SIM,AKA,AKA,FAST,LEAP}, --eap {PEAP,TLS,TTLS,PWD,SIM,AKA,AKA,FAST,LEAP}
                            EAP type for EAP connections.See: https://w1.fi/cgit/h
                            ostap/plain/wpa_supplicant/wpa_supplicant.conf

---

    wpa_cli_py_scan_results -h
    usage: wpa_cli_py_scan_results.py [-h] ifname
    
    Performs scan e scan_results commands and returns the WIFI networks found.
    
    positional arguments:
      ifname      Specify the interface that is being used.
    
    optional arguments:
      -h, --help  show this help message and exit

---

    wpa_cli_py_wps_connect_to_network -h
    usage: wpa_cli_py_wps_connect_to_network [-h] [-p PIN] [-b BSSID] ifname
    
    Force wpa_supplicant to connect to a network using wps.
    
    positional arguments:
      ifname                Specify the interface that is being used.
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PIN, --pin PIN     If present, the wps_pin connection will be use.
      -b BSSID, --bssid BSSID
                            The BSSID of the network. Specific for connections
                            using pin. The default value is any.


