import subprocess
import time
import os
import pandas as pd

file = r"c:\Work\output_trt.txt"
max_filesize = 1_000_000


def trace_route():
        f = open(file, 'a')
        replace_dic = ['b\'', '\'', '\'b', '\\r', '\\n']

        def replace_all(text, dic):
                for i in dic:
                        text = text.replace(i, "")
                return text
        hostname = '1.1.1.1'
        traceroute = subprocess.Popen(["tracert", '-w', '100', hostname],
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        current_time = time.strftime("%a %I:%M:%S %p", time.localtime())
        print(current_time)
        f.write(current_time)
        while True:
                hop = traceroute.stdout.readline()
                if not hop:
                        f.write('\n')
                        break
                hop = replace_all(str(hop), replace_dic).strip()
                print(hop)
                f.write(hop + '\n')
        f.close()
        if os.path.getsize(file) > max_filesize:
                clean_file()


def clean_file():
        df = pd.read_csv(file, sep='\n', skiprows=16, skip_blank_lines=False)
        df.to_csv(file, index=False, na_rep=" ")


if __name__ == '__main__':
        for n in range(1):
                trace_route()
                time.sleep(1)
