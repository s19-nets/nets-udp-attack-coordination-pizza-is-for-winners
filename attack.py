#! /usr/bin/env python3


import time, os
pid = os.getpid()

print("dummy attack program with pid %d.  do not trust my results" % pid)

time.sleep(1)                        # sleep for 1 second

print("%d: attacking at %s" % (pid, time.asctime(time.localtime()))) # print time
