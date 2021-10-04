# running this will continuously ping 1.1.1.1.
# if a hop fails, it will then run trace route (via tracert.py) to 1.1.1.1 to see where the failure occurs.
# it then logs the failure into a file (c:\Work\output_trt.txt), along with its day and time

import subprocess
import tracert


def PingTest(last_ping):
    replace_dic = ['b\'', '\'', '\'b', '\\r', '\\n']
    timeout = 'timed'
    reply = "time="

    def replace_all(text, dic):
        for i in dic:
            text = text.replace(i, "")
        return text
    hostname = '1.1.1.1'
    ping = subprocess.Popen(["ping", "-t", hostname],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # continuously ping until a ping fails; log ping result on screen
    while True:
        hop = replace_all(str(ping.stdout.readline()), replace_dic).strip()
        # print(hop)
        if hop.find(timeout) > -1 and last_ping:  # looking for the word "timed" in the result ("timed out") in order
            # to know if fail
            return False
        elif hop.find(reply) > -1 and not last_ping:  # returns true to log that the connection is back if the ping
            # passes and the last_ping was fail
            return True


if __name__ == "__main__":
    print("\n\nConnection test running. Connection failures and reconnections will be logged.")
    last_ping = False
    while True:
        last_ping = PingTest(last_ping)  # infinite loop if successful, unless last run was fail
        last_ping = tracert.trace_route(last_ping)  # this will log if connection restored, or trace if failure
