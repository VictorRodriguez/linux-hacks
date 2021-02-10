import subprocess

output = subprocess.check_output(["cat","/sys/class/thermal/thermal_zone0/type"],universal_newlines=True)
print(output)
output = subprocess.check_output(["cat","/sys/class/thermal/thermal_zone0/temp"],universal_newlines=True)
print(int(output)/1000)
