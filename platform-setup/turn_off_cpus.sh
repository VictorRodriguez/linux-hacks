#!/bin/bash

MAX_CPUS=$(cat /proc/cpuinfo | grep processor | wc -l)

for ((i=2; i<$MAX_CPUS; i++))
do
    echo Turning off CPU $i;
	echo 0 > /sys/devices/system/cpu/cpu$i/online
done


