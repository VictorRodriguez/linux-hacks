# How to set up and use KDUMP to debug Kernel panics


## Build the kernel with proper flags:

 First and foremost, your kernel should have the following components statically built in to its image:

```
CONFIG_RELOCATABLE=y
CONFIG_KEXEC=y
CONFIG_CRASH_DUMP=y
CONFIG_DEBUG_INFO=y
CONFIG_MAGIC_SYSRQ=y
CONFIG_PROC_VMCORE=y

```

Refer to [linux build information](https://github.com/VictorRodriguez/linux-hacks/tree/master/dockerimages/linux-build)
to have a proper set up enviroment to build and install proper linux kernel image.

##  Install the kexec-tools package

To use the kdump service, you must have the kexec-tools package installed. If not already installed, install the kexec-tools.

```
yum install kexec-tools
```

## Configuring Memory Usage in GRUB2

To configure the amount of memory that is reserved for the kdump kernel, modify
/etc/default/grub and modify GRUB_CMDLINE_LINUX , set crashkernel=[size]
parameter to the list of kernel options.

```
vim /etc/default/grub
```

In line "BOOT_IMAGE" confirm "crashkernel=256M" is there, also append  these
parameters "console=ttyS0,115200 console=tty0" finally remove "quiet"

## Configuring Core Collector

To reduce the size of the vmcore dump file, kdump allows you to specify an
external application to compress the data, and optionally leave out all
irrelevant information. Currently, the only fully supported core collector is
makedumpfile. To enable the core collector, modify configuration file
/etc/kdump.conf, remove the hash sign (“#”) from the beginning of the

```
core_collector makedumpfile -c –message-level 1 -d 31
```

## Changing Default Action

We can also specify the default action to perform when the core dump fails to
generate at the desired location. If no default action is specified, “reboot”
is assumed default. For example:

```
default halt
```

## Configuring Dump Location

To configure kdump, we need to edit the configuration file /etc/kdump.conf. The
default option is to store the vmcore file is the /var/crash/ directory of the
local file system. To change the local directory in which the core dump is to
be saved and replace the value with desired directory path.  For example:

```
path /usr/local/cores
```


## Re-regerate the grub files

```
grub2-mkconfig -o /boot/grub2/grub.cfg
grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
reboot
```

IMPORTANT! For Centos 8 follow grubby tool
https://docs.fedoraproject.org/en-US/Fedora/23/html/System_Administrators_Guide/sec-Configuring_GRUB_2_Using_the_grubby_Tool.html


## Start kdump daemon

Check and make sure kernel command line includes the kdump config and memory
was reserved for crash kernel:

```
cat /proc/cmdline
BOOT_IMAGE=/vmlinuz-3.8.13-98.2.1.el7uek.x86_64 root=/dev/mapper/rhel-root \
rord.lvm.lv=rhel/root crashkernel=256M rd.lvm.lv=rhel/swap \
vconsole.font=latarcyrheb-sun16 vconsole.keymap=us rhgb quiet nomodeset
```

Set kdump service can be started when system rebooted.

```
systemctl enable kdump.service
```

To start the service in the current session, use the following command:

```
systemctl start kdump.service
```

## Testing kdump (manually trigger kdump)

To test the configuration, we can reboot the system with kdump enabled, and make sure that the service is running.

For example:

```
systemctl is-active kdump
active
```

```
service kdump status
	Redirecting to /bin/systemctl status  kdump.service
	kdump.service - Crash recovery kernel arming
	Loaded: loaded (/usr/lib/systemd/system/kdump.service; enabled)
	Active: active (exited) since 一 2015-08-31 05:12:57 GMT; 1min 6s ago
	Process: 19104 ExecStop=/usr/bin/kdumpctl stop (code=exited, status=0/SUCCESS)
	Process: 19116 ExecStart=/usr/bin/kdumpctl start (code=exited, status=0/SUCCESS)
	Main PID: 19116 (code=exited, status=0/SUCCESS)
	Aug 31 05:12:57 ol7 kdumpctl[19116]: kexec: loaded kdump kernel
	Aug 31 05:12:57 ol7 kdumpctl[19116]: Starting kdump: [OK]
	Aug 31 05:12:57 ol7 systemd[1]: Started Crash recovery kernel arming.
```

Then type the following commands at a shell prompt:

```
echo 1 > /proc/sys/kernel/sysrq
echo c > /proc/sysrq-trigger
```

This will force the Linux kernel to crash, and the
address-YYYY-MM-DD-HH:MM:SS/vmcore file will be copied to the location you have
selected in the configuration (that is, to /var/crash/ by default)


## Analyze kernel debug information

To analyze dump files kernel-debuginfo is needed. First enable debuginfo repo

```
vim /etc/yum.repos.d/CentOS-Linux-Debuginfo.repo
```

Change enabled=0 to 1

```
yum install yum-utils
```
Check kernel version -- uname -r -- and download kernel source
```
debuginfo-install kernel-`uname -r`
```
If you re behind a proxy, make sure that debuginfo-install has proxy configured

After the kernel debug info is install we can use crash tool to analyze:

```
cd /var/crash/** folder name crash
crash /usr/lib/debug/lib/modules/4.18.0-240.el8.x86_64/vmlinux /var/crash/<>/vmcore
```

# Debug a Kernel driver with null pointer using Kdump

Please refer to null_pointer.c code to build and insmod a driver with kernel
panic, after the vmcore is generated we can use crash to show this information

```

      KERNEL: /usr/lib/debug/vmlinux-4.9.0-8-amd64
    DUMPFILE: dump.201902261035  [PARTIAL DUMP]
        CPUS: 4
        DATE: Tue Feb 26 10:37:47 2019
      UPTIME: 00:11:16
LOAD AVERAGE: 0.24, 0.06, 0.02
       TASKS: 102
    NODENAME: deb-panic
     RELEASE: 4.9.0-8-amd64
     VERSION: #1 SMP Debian 4.9.144-3 (2019-02-02)
     MACHINE: x86_64  (2592 Mhz)
      MEMORY: 4 GB
       PANIC: "BUG: unable to handle kernel NULL pointer
 ↪dereference at 0000000000000001"
         PID: 1493
     COMMAND: "insmod"
        TASK: ffff893c5a5a5080 [THREAD_INFO: ffff893c5a5a5080]
         CPU: 3
       STATE: TASK_RUNNING (PANIC)

```

## References

[1] https://www.thegeekdiary.com/centos-rhel-7-how-to-configure-kdump/
[2] https://www.linuxjournal.com/content/oops-debugging-kernel-panics-0


