import subprocess
import tracert


def PingTest():
        replace_dic = ['b\'', '\'', '\'b', '\\r', '\\n']
        timeout = 'timed'

        def replace_all(text, dic):
                for i in dic:
                        text = text.replace(i, "")
                return text
        hostname = '1.1.1.1'
        ping = subprocess.Popen(["ping", "-t", hostname],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
                hop = ping.stdout.readline()
                hop = str(hop)
                hop = replace_all(str(hop), replace_dic).strip()
                print(hop)
                if hop.find(timeout) > 0:
                    return False


if __name__ == "__main__":
    while True:
        if PingTest():
            pass
        else:
            tracert.trace_route()
