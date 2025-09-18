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

def proxy(listen_host, listen_port, server_host, server_port, buffer, alc_allowIp, alc_denyIp):
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((listen_host,listen_port))
    proxy.listen(5)
    print(f"[Azurite] Listening on {listen_host}:{listen_port} → {server_host}:{server_port}")

    while True:
        clientSock, addr = proxy.accept()

        if alc_allowIp[0] and addr[0] not in alc_allowIp[1]:
            clientSock.close()
            continue
        if alc_denyIp[0] and addr[0] in alc_denyIp[1]:
            clientSock.close()
            continue
        threading.Thread(target=handle, args=(clientSock, server_host, server_port, buffer)).start()

def start():
    load_config()

    listen_host = config.get("forward").get("listen_address")
    listen_port = config.get("forward").get("listen_port")

    server_host = config.get("forward").get("server-address")
    server_port = config.get("forward").get("server-port")

    buffer = config.get("forward").get("buffer-size")

    access_control_allowIp_status = config.get("forward").get("allow-ips").get("enable")
    access_control_denyIp_status = config.get("forward").get("deny-ips").get("enable")

    access_control_allowIp_list = config.get("forward").get("allow-ips").get("ip-list")
    access_control_denyIp_list = config.get("forward").get("deny-ips").get("ip-list")

    configReload = threading.Thread(target=config_reload, args=(5), daemon=True)
    main = threading.Thread(target=proxy, args=(listen_host
                                                    , listen_port
                                                    , server_host
                                                    , server_port
                                                    , buffer
                                                    , [access_control_allowIp_status, access_control_allowIp_list]
                                                    , [access_control_denyIp_status, access_control_denyIp_list]))

    configReload.start()
    main.start()



