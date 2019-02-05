# nets-udp-attack-coordination

Your task is create a program named attack.py.  It is to be used by
two military battalians to coordinate a joint attack.  It's imperative
that they attack at the same time, lest both groups lose battles sequentially.

Two instances of this program will negotiate with each other to
determine a future time of coordinated attack.  Once an instance has
determined its time of attack, it should print that time and
terminate.  It's critical that both instances agree on the same
(future) time.

An instance of Attack.py must inform its user if it fails to
coordinate an attack time with the other instance.  While this is
better than falsely reporting an incorrectly coordinated attack time,
this event would nonetheless be considered a catasrophic failure.


Attack should accept the parameters:
-l <listen address:port>           -- specify address:port on which to listen
-s <send address:port>     -- specify address:port to which messages are sent
-v                         -- print verbose (debugging) output

For example, a session of attack could be run as follows:

$ ./attack.py -l localhost:50000 -s localhost:50001 &
$ ./attack.py -s localhost:50000 -l localhost:50001 &
$ wait

Note that the file ./attack.py is a placeholder dummy program that
(essentially) just prints the time.  Your task is to modify it to
implement "coordinated attack" protocol.

Students are encouraged to study the script ./run-attack.sh, which starts
proxies, then runs attack, and then kills the proxies.

# Important
Note that, in the real world, UDP may arbitrarily delay or lose
messages.  Your implementation of attack should be tolerant of this.

Towards that end, you are encouraged to employ a proxy that simulate
that behavior.  One such proxy is in directory ./proxy.  That
directory includes a README that describes its usage.

