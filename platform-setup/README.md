#Set up the number of cores:


* First we have 4 cores:

```
$ cat /proc/cpuinfo | grep processor
processor             : 0
processor             : 1
processor             : 2
processor             : 3
```


Then we disable them:

```
# echo 0 > /sys/devices/system/cpu/cpu3/online
# echo 0 > /sys/devices/system/cpu/cpu2/online
# echo 0 > /sys/devices/system/cpu/cpu3/online
```


# only two are visible:

```
# cat /proc/cpuinfo | grep processor
processor             : 0
processor             : 1
```

* We can enable them back as:

```
$ echo 1 > /sys/devices/system/cpu/cpu3/online
$ echo 1 > /sys/devices/system/cpu/cpu2/online
$ cat /proc/cpuinfo | grep processor
processor             : 0
processor             : 1
processor             : 2
processor             : 3
```


To make it permanent in kernel boot args, add nr_cpus=N to your GRUB_CMDLINE_LINUX:

```
# cat /etc/sysconfig/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet nr_cpus=2 "
GRUB_DISABLE_RECOVERY="true"
```

Use grub2-mkconfig command to regenerate the /boot/grub2/grub.cfg file:

```
$ grub2-mkconfig -o /boot/grub2/grub.cfg
```

Reboot and verify:

```
$ reboot

$ cat /proc/cpuinfo | grep processor
processor             : 0
processor             : 1
```

## Set up the frequency:

you can set the frequency manually:

```
echo value > /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
```



