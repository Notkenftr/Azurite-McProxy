# Azurite McProxy

Azurite McProxy is a secure intermediary layer that helps you connect to Minecraft servers safely and privately. When using this proxy, your real IP address will never be exposed – instead, the server will only see the proxy’s IP.

# 📃Requirements

```
- python 3.8+
- Port forwarding
- Potato pc
```

# ⚡ Install

## Step 1 download Azurite-McProxy:

using:
```git clone https://github.com/Notkenftr/Azurite-McProxy```

## Step 2 config

The azurite.yml file is where you configure all proxy settings. Below is a detailed explanation of each field:
```yaml
forward:
  listen_address: 0.0.0.0   # Address the proxy will listen on.

  listen_port: 25565        # Port where the proxy listens (your Minecraft client connects here)

  server-address: 123.45.67.89  # Real Minecraft server address (the proxy forwards traffic here)
  server-port: 25565            # Real Minecraft server port

  buffer-size: 128              # Buffer size (KB) for forwarding data
                                # - 64  = 64KB  (lighter, uses less RAM)
                                # - 128 = 128KB (recommended, balanced)
                                # - 256 = 256KB (faster, higher RAM usage)

```
Example Setup

Forwarding to the real server play.hypixel.net, port 25565
```yaml
forward:
  listen_address: 0.0.0.0
  listen_port: 25566

  server-address: play.hypixel.net
  server-port: 25565

  buffer-size: 128
```


# Setup Guide: Running Proxy & Connecting from Minecraft


## Preparation

1. Make sure the file proxy.py is ready and the proxy port is configured (e.g., 9999 or 25565).

2. Install Python (usually python3).

3. If running on a VPS/home server, open the proxy port in the firewall/router (if needed).

##  1. Run the Proxy
Open a terminal on the machine where the proxy will run, go to the folder containing proxy.py, then execute:
```bash
# Linux / macOS
python3 proxy.py

# Windows (if Python is bound to the command "python")
python proxy.py

```

After running, the console should show something like:
```
[Azurite] Listening on 0.0.0.0:xxxx → 192.168.1.100:xxxx
```

If you don’t see this, check for errors such as bind failure / Address already in use / missing permissions.

## 2. Get Proxy IP & Port


Find public IP if the client is connecting from the internet:

- On the proxy machine: curl ifconfig.me or visit a site like whatismyip.

Port = proxy listening port (e.g., 25562).

Example server address:

```
203.0.113.5:25562

```

If the proxy runs behind a router (home VPS), remember to set up port forwarding: ``public_port → internal_ip:proxy_port``.

## 3. Add Server in Minecraft (Client)

- Open Minecraft → go to Multiplayer.
- Click **Add Server** (or Direct Connect if you want to join immediately).
- Server Name: set any name (e.g., “Azurite Proxy”).
- Server Address: enter IP:PORT (e.g., 203.0.113.5:9999).
   - If the port is 25565 (default), you can just enter the IP.
- Save → select the server → Play / Join Server.

# Troubleshooting

## A. If Minecraft disconnects instantly
- Try increasing ``BUFFER_SIZE`` (e.g., 128KB) to reduce packet split issues.

- Check if proxy is forwarding properly in both directions.

- Verify the real server (target_host:target_port) is online.

## B. Check log proxy

- When a client connects, the proxy console should show:
```
Incoming connection from ('client_ip', 41123)
[C→S] Forwarded 256 bytes
[S→C] Forwarded 1024 bytes
```
- If you don’t see logs:
  -  The proxy may not be working, please check the setup steps again.


# License

This project is licensed under the MIT License.

You are free to:

✅ Use this project for personal or commercial purposes

✅ Modify and adapt it to your needs

✅ Distribute it, with or without modifications

However, you must:

📄 Include this license and credit the original author (kenftr)

In short: The software is provided "as-is", without warranty of any kind.

Learn more about MIT License
