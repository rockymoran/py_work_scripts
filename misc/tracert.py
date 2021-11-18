# running this on its own will just test the connection once. it will run a trace route to 1.1.1.1
# this file is used by tracert_ping.py to find out where on the route failures are happening when a ping test fails.

import subprocess
import time
import os
import pandas as pd

file = r"c:\Work\output_trt.txt"
max_filesize = 1_000_000


def trace_route(previous):
    f = open(file, 'a')
    replace_dic = ['b\'', '\'', '\'b', '\\r', '\\n']

    def replace_all(text, dic):
        for i in dic:
            text = text.replace(i, "")
        return text

    hostname = '1.1.1.1'
    unreachable = 'Destination host unreachable'
    traceroute = subprocess.Popen(["tracert", '-w', '100', hostname],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    current_time = time.strftime("%a %b %d %Y %I:%M:%S %p", time.localtime())
    if not previous:
        print("\nConnection failure detected at %s. Testing tracert..." % current_time)
        f.write("Connection failure detected at %s. Testing tracert... \n" % current_time)
        down = False
        while True:
            hop = traceroute.stdout.readline()
            if not hop:
                f.write('\n')
                break
            hop = replace_all(str(hop), replace_dic).strip()
            print(hop)
            if hop.find(unreachable) > -1:
                down = True
            f.write(hop + '\n')
        if down:
            f.write("\nConnection failure. Tracert unsuccessful at %s \n" % current_time)
            print("The internet is currently down.")
        f.close()
    else:
        print("\nConnection restored at %s" % current_time)
        f.write("\nConnection restored at %s \n\n\n" % current_time)
    if os.path.getsize(file) > max_filesize:
        clean_file()
    return previous


def clean_file():
    df = pd.read_csv(file, sep='\n', skiprows=16, skip_blank_lines=False)
    df.to_csv(file, index=False, na_rep=" ")


if __name__ == '__main__':
    for n in range(1):
        trace_route()
        time.sleep(1)
