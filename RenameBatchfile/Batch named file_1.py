import os
import glob

files = glob.glob('*')
print(files)
Number = 0
for OldName in files:
    Number = Number + 1
    Number1 = str(Number)
    for Places in range(4-len(str(Number))):
        Number1 = '0' + Number1
    a, b = os.path.splitext(OldName)
    os.rename(OldName, Number1+'.'+b)
