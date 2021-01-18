#!/usr/bin/env python3

import os

path = "/var/crash"
crash_dir = os.listdir(path)
debuginfo = "/usr/lib/debug/lib/modules/4.18.0-240.el8.x86_64/vmlinux"
inputfile = "crash_cmd.txt"
outputfile = "crash_summary.log"


# Checking if the crash_dir is empty or not
if len(crash_dir) == 0:
    print("Empty directory")
else:
    print("Not empty directory")
    for directory in crash_dir:
        crash_dir_date = os.path.join(path, directory)
        crash_dir_vmcore = os.path.join(crash_dir_date, "vmcore")
        if os.path.isfile(crash_dir_vmcore):
            print("VMORE exists")
            outputfile_path = os.path.join(crash_dir_date, outputfile)
            cmd = "crash %s %s < %s > %s "\
                % (debuginfo, crash_dir_vmcore, inputfile, outputfile_path)
            print(cmd)
            ret = os.system(cmd)
            print("Debug in %s dump correctly to %s " %
                  (directory,
                   outputfile_path))
