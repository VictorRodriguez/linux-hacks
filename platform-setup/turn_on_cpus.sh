#!/bin/bash

MAX_CPUS=63

for ((i=2; i<$MAX_CPUS; i++))
do
    echo Turning off CPU $i;
	echo 1 > /sys/devices/system/cpu/cpu$i/online
done


