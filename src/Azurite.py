#MIT License

#Copyright (c) 2025 kenftr

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import socket
import threading
import time

import yaml

from src.utils.pathManager import path
from src.handle import handle

#init variable
config = {}



def load_config():
    global config
    try:
        with open(path.config(), 'r', encoding='utf-8') as yamlData:
            config = yaml.load(yamlData, Loader=yaml.SafeLoader)
    except Exception as e:
        print(f"[Azurite] {e}")

def config_reload(interval=5):
    while True:
        load_config()
        time.sleep(interval)

def proxy(listen_host,
          listen_port,
          server_host,
          server_port,
          buffer,
          alc_allowIp: list,
          alc_denyIp: list):
    """
    Start a TCP proxy that listens for incoming client connections and forwards traffic
    to a specified server, while applying optional IP allow/deny rules.

    :param listen_host: The host/IP address where the proxy will listen (e.g., "0.0.0.0").
    :param listen_port: The port number where the proxy will listen for client connections.
    :param server_host: The target server's host/IP address to forward traffic to.
    :param server_port: The target server's port number to forward traffic to.
    :param buffer: The buffer size (in bytes) for reading and forwarding data.
    :param alc_allowIp: A list of allowed client IPs. Only these IPs can connect if not empty.
    :param alc_denyIp: A list of denied client IPs. Any IPs in this list will be blocked.
    :return: None. The function runs continuously until terminated.
    """
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((listen_host,
                listen_port))
    proxy.listen(5)
    print(f"[Azurite] Listening on {listen_host}:{listen_port} → {server_host}:{server_port}")

    while True:
        clientSock, addr = proxy.accept()

        #here alc_allowIp[0] is a status of acess-control.allow-ips.enable and alc_allowIp is a acess-control.allow-ips.iplist
        # alc.denyIp[0] is a status of acess-control.deny-ips.enable and alc_denyIp[1] is a acess-control.deny-ips.iplist

        if alc_allowIp[0] and addr[0] not in alc_allowIp[1]:
            #if alc_allowIp = True and client ip not in iplist
            # alc_allowIp[1] contains the non-blocked IPs.
            clientSock.close()
            continue
        if alc_denyIp[0] and addr[0] in alc_denyIp[1]:
            # if alc_denyIp = True and client ip in iplist
            # alc_denyIp[1] contains the blocked IPs.
            clientSock.close()
            continue
        threading.Thread(target=handle, args=(clientSock,
                                              server_host,
                                              server_port,
                                              buffer)).start()

def start():
    """
    Entry point to initialize and start the proxy service.

    This function sets up the listening socket, applies access control rules
    (allow/deny IP), and begins handling client connections.

    :return: None. Runs indefinitely until manually stopped.
    """

    load_config()
    time.sleep(0.2)


    listen_host = config.get("forward").get("listen_address")
    listen_port = config.get("forward").get("listen_port")

    server_host = config.get("forward").get("server-address")
    server_port = config.get("forward").get("server-port")

    buffer = config.get("forward").get("buffer-size")

    access_control_allowIp_status = config.get("forward").get("access-control").get("allow-ips").get("enable")
    access_control_denyIp_status = config.get("forward").get("access-control").get("deny-ips").get("enable")

    access_control_allowIp_list = config.get("forward").get("access-control").get("allow-ips").get("ip-list")
    access_control_denyIp_list = config.get("forward").get("access-control").get("deny-ips").get("ip-list")

    configReload = threading.Thread(target=config_reload, args=(5,), daemon=True) # auto reload config after 5s
    main = threading.Thread(target=proxy, args=(listen_host
                                                    , listen_port
                                                    , server_host
                                                    , server_port
                                                    , buffer * 1024
                                                    , [access_control_allowIp_status, access_control_allowIp_list]
                                                    , [access_control_denyIp_status, access_control_denyIp_list]))

    configReload.start()
    main.start()



