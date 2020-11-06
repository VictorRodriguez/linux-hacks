#!/bin/bash

# Install the GNOME desktop environment. Follow our guide on how to install
# GNOME desktop on RHEL 8 / CentOS 8 Linux or simply execute:

dnf groupinstall workstation

# (Optional) Enable GUI to start after reboot.

systemctl set-default graphical.target

# Start GUI on RHEL 8 / CentOS 8 without the need for reboot by using the
# systemctl command:

systemctl isolate graphical

