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

def forward(src, dst, BUFFER_SIZE, direction="C→S"):
    """
    Forward data between two sockets.

    Args:
        src (socket.socket): The source socket to read data from.
        dst (socket.socket): The destination socket to send data to.
        BUFFER_SIZE (int): The maximum amount of data to read at once (bytes).
        direction (str, optional): A string indicating the forwarding direction,
            e.g. "C→S" for Client to Server or "S→C" for Server to Client.

    Returns:
        None

    Raises:
        ConnectionResetError: If the peer unexpectedly resets the connection.
        BrokenPipeError: If the socket is closed and cannot send data.
        Exception: For any other unexpected errors during forwarding.
    """
    try:
        while True:
            # Receive data from the source socket
            data = src.recv(BUFFER_SIZE)
            if not data:
                break # Receive data from the source socket

            # Send the received data to the destination socket
            dst.sendall(data)
            print(f"[Azurite] [{direction}] Forwarded {len(data)} bytes", flush=True)
    except (ConnectionResetError, BrokenPipeError):
        print(f"[Azurite] Connection reset by peer -> closing sockets", flush=True)
    except Exception as e:
        print(f"[Azurite] Unexpected error in forward: {e}", flush=True)