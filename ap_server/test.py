import os
import platform

# This is the path to the ORACLE client files
lib_dir = r"C:\Users\learn\Desktop\instantclient_21_6"

# Diagnostic output to verify 64 bit arch and list files
print("ARCH:", platform.architecture())
print("FILES AT lib_dir:")
for name in os.listdir(lib_dir):
    print(name)