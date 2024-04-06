__author__ = 'jiayingyu'
#<a href="http://pymotw.com/2/socket/udp.html">UDP client and server</a>

import socket
import time
import argparse

output = {
    "packetLoss": 0,
    "minRTT": 9999,
    "maxRTT": 0
}

parser = argparse.ArgumentParser()
parser.add_argument('--host', dest="host", type=str, action='store', help='set host', default=None)
parser.add_argument("--port", dest="port", type=int, action='store', help="set UDP port", default=12000)
parser.add_argument("-t", dest="timeout", type=int, action='store', help="timeout in seconds", default=1)
parser.add_argument("-c", dest="count", type=int, action='store', help="count", default=4)
args=parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.host, args.port)
sock.settimeout(args.timeout)

try:
    for i in range(args.count):
        start = time.time()
        message = 'Ping #' + str(i) + " " + time.ctime(start)
        try:
            sent = sock.sendto(message.encode('utf-8'), server_addr)
            print("Sent " + message)
            data, server = sock.recvfrom(4096)
            print("Received " + data.decode("utf-8"))
            end = time.time();
            elapsed = end - start

            if elapsed < output["minRTT"]:
                output["minRTT"] = elapsed
            if elapsed > output["maxRTT"]:
                output["maxRTT"] = elapsed

            print("RTT: " + str(elapsed) + " seconds\n")

        except socket.timeout:
            print("#" + str(i) + " Requested Time out\n")
            output["packetLoss"] += 1

finally:
    print("closing socket\n")
    sock.close()

print("Summary:")
print("rtt min / max:", output["minRTT"], "/", output["maxRTT"])
print("packet loss ", output["packetLoss"], "from", args.count)
