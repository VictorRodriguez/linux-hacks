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

```
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo grubby --set-default /boot/vmlinuz-5.6.9
```

You can confirm the details with the following commands:
```
grubby --info=ALL | more
grubby --default-index
grubby --default-kernel
```

## For EFI

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
