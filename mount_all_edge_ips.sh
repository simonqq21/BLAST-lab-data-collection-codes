#!/bin/bash
sshfs pi@192.168.1.102: edge-pi1 -o nonempty
sshfs pi@192.168.1.103: edge-pi2 -o nonempty
sshfs pi@192.168.1.104: edge-pi3 -o nonempty
sshfs pi@192.168.1.105: edge-pi4 -o nonempty
sshfs pi@192.168.1.106: edge-pi5 -o nonempty
