import subprocess
import time

f = open(r"c:\Work\output_trt.txt", 'w')


def TraceRoute():
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
                    break
                hop = replace_all(str(hop), replace_dic).strip()
                print(hop)
                f.write(hop + '\n')


for n in range(2):
        TraceRoute()
        time.sleep(15)
f.close()
