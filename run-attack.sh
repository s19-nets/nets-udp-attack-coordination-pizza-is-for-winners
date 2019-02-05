#! /usr/bin/env bash

#Run two instances of attack via proxies at addresses 50010 ad 50020

# start proxies
proxy/udpProxy.py --clientPort 50010 --serverAddr localhost:50000 --pDelay 0.5 --pDrop 0.1 --pDup 0.1 --quiet &
PR_PIDS=$!
proxy/udpProxy.py --clientPort 50011 --serverAddr localhost:50001 --pDelay 0.5 --pDrop 0.1 --pDup 0.1 --quiet &
PR_PIDS="$PR_PIDS $!"

sleep 0.5			# wait for proxies to start
echo "Proxies started (pids=$PR_PIDS)"

# start attack programs
./attack.py -l localhost:50000 -s localhost:50011 &
A_PIDS=$!
./attack.py -s localhost:50001 -s localhost:50010 &
A_PIDS="$A_PIDS $!"

echo "$0: waiting for attacks (pids=$A_PIDS) to compute attack time"
# wait for attackers to terminate
for A_PID in $A_PIDS ; do
    wait $A_PID
done

echo "$0: killing proxies with pids=$PR_PIDS"
# kill proxies
kill -9 $PR_PIDS




