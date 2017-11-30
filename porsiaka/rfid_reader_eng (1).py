import sys

while 1:
    line = sys.stdin.readline()
    if line == '':
        break
    if not line.startswith("New tag"):
        continue
    serial = line.split()[-1].split("=", 1)[1]
    print(serial)

