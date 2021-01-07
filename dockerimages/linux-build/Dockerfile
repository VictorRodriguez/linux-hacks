FROM centos:latest AS builder


RUN yum install -y ncurses-devel make gcc bc bison flex elfutils-libelf-devel openssl-devel grub2 git
RUN yum group install "Development Tools" -y
RUN mkdir -p /usr/src/
RUN cd /usr/src/ && \
	git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
RUN cd /usr/src/linux && \
	make oldconfig && \
	make
