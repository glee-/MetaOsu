from lib import *
import shutil, os
directory = "/home/geo/git/MetaOsu/"
outputDir = "./"

os.chdir(directory)
files = getFileNames()
f = open(files[0], "r")
data = parse(f)
print(data)
# f = open("test.txt", "r")
# f.readline()
# a = f.readline()
# print(a == None)
