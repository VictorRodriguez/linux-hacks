# Systemd services 

systemd is used in many mainstream Linux distributions. It provides
an easy way to manage and control services and a simple method of creating your
own services. This will cover the process of creating and managing your own
custom service.

You should copy your .service file to /etc/systemd/system. 

```
cp personal.service /etc/systemd/system/
```

Example of .service: 


```
[Unit]
Description=My Miscellaneous Service
After=network.target

[Service]
Type=simple
User=nanodano
WorkingDirectory=/home/nanodano
ExecStart=/home/nanodano/my_daemon --option=123
Restart=on-failure # or always, on-abort, etc

[Install]
WantedBy=multi-user.target
```

There are more options you can specify. For example, in addition to ExecStart
you can specify ExecStop and ExecReload to control what happens when stopping
and restarting. Those are not required though.

```
man systemd.service
```

Or: 

* https://www.freedesktop.org/software/systemd/man/systemd.service.html

##Controlling the Service

### Control whether service loads on boot
systemctl enable
systemctl disable

### Manual start and stop
systemctl start
systemctl stop

### Restarting/reloading
systemctl daemon-reload # Run if .service file has changed
systemctl restart

## Controlling the Service

### See if running, uptime, view latest logs
systemctl status

### See all systemd logs
journalctl

### Tail logs
journalctl -f

## Show logs for specific service
journalctl -u my_daemon.service


For our case we coudl do: 

```
$ systemctl enable personal.service
$ sudo systemctl restart personal.service
$ systemctl status personal.service

● personal.service - personal
   Loaded: loaded (/etc/systemd/system/personal.service; enabled; vendor preset: disabled)
   Active: inactive (dead) since Fri 2018-04-20 17:44:03 UTC; 3s ago
  Process: 15353 ExecStart=/usr/bin/ls (code=exited, status=0/SUCCESS)
 Main PID: 15353 (code=exited, status=0/SUCCESS)

Apr 20 17:44:03 vrodri3-work ls[15353]: mnt
Apr 20 17:44:03 vrodri3-work ls[15353]: proc
Apr 20 17:44:03 vrodri3-work ls[15353]: root
Apr 20 17:44:03 vrodri3-work ls[15353]: run
Apr 20 17:44:03 vrodri3-work ls[15353]: sbin
Apr 20 17:44:03 vrodri3-work ls[15353]: srv
Apr 20 17:44:03 vrodri3-work ls[15353]: sys
Apr 20 17:44:03 vrodri3-work ls[15353]: tmp
Apr 20 17:44:03 vrodri3-work ls[15353]: usr
Apr 20 17:44:03 vrodri3-work ls[15353]: var

```
