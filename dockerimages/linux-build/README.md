# Build Linux Kernel

This dockerfile provides the basic for build an upstream kernel image with make oldconfig


## Build the kernel on CentOS image:

The procedure to build (compile) and install the latest Linux kernel from source is as follows:

  * Install build deps
  * Grab the latest kernel from kernel.org
  * Untar the kernel tarball
  * Copy existing Linux kernel config file
  * Compile and build Linux kernel 5.X
  * Install Linux kernel and modules (drivers)
  * Update Grub configuration
  * (If you have EFI, update EFI)
  * Reboot the system

# Build dependencies

```
yum install -y ncurses-devel make gcc bc bison flex \
  elfutils-libelf-devel openssl-devel grub2 git
```

## Grab the latest kernel from kernel.org

Review versions at https://www.kernel.org/

```
wget https://cdn.kernel.org/pub/linux/kernel/.... 
  (here you check what version do you want)
```

## Untar the kernel tarball

```
xz -d -v linux-5.x.x.tar.xz
```

## Copy existing Linux kernel config file

```
cd linux-5.6.9
cp -v /boot/config-$(uname -r) .config
```

## Configuring the kernel

```
make menuconfig
```

## Compile and build Linux kernel 5.X

To speed up compile time, pass the -j as follows:
 
```
## use 4 core/thread ##
$ make -j 4
## get thread or cpu core count using nproc command ##
$ make -j $(nproc)

```

## Install the Linux kernel modules

```
sudo make modules_install 
```

## Install the Linux kernel

```
sudo make install 
```

## Update grub config

First is necesary to find what kernel do we want: 

```
awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
```
Will print a list of the kernels we want, such as: 

```
Linux Server, with Unbreakable Enterprise Kernel 3.8.13-94.el7uek.x86_64
Linux Server, with Unbreakable Enterprise Kernel 3.8.13-94.el7uek.x86_64 with debugging
Linux Server 7.1, with Linux 3.10.0-229.el7.x86_64
Linux Server 7.1, with Unbreakable Enterprise Kernel 3.8.13-55.1.6.el7uek.x86_64
Linux Server 7.1, with Linux 0-rescue-441e86c9ff854310a306bd33e56aae2b
```

NOTE: The first entry is denoted as Zero. So currently the Server is booted to 0th entry as per the above `uname -a` command output.

Let us modify the Kernel Version to 3.8.13-55.1.6.el7uek.x86_64 which is at line number 4 but denoted as entry 3.

```
# grub2-set-default 3
```

Changes to /etc/default/grub require rebuilding the grub.cfg file as follows:

```
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

## For EFI
IMPORTANT: Is necesary to perform previous instructions to Update grub config

```
grub2-mkconfig > /boot/efi/EFI/centos/grub.cfg
```

## Reboot and review

```
reboot

[...]

uname -a
```

## TODO

* Enable the capability to use the config file form outside the container

### Refrs

1 ) https://www.cyberciti.biz/tips/compiling-linux-kernel-26.html
2 ) https://linuxhint.com/grub2_mkconfig_tutorial/
