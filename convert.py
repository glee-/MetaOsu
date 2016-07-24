from lib import *
import shutil, os, errno
import mutagen
directory = "/home/geo/git/MetaOsu/"
outputDir = "output/"

os.chdir(directory)

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# f = open("test.txt", "r")
# f.readline()
# a = f.readline()
# print(a == None)

#Assumes that we are in the song directory, parses song data
def readSong():
    files = getFileNames()
    f = open(files[0], "r")
    return parse(f)
    # return files



songdata = readSong()
print(songdata)
songdir = directory + songdata[0]
tempdir = directory + "temp_" + songdata[0]

shutil.copy2(songdir, tempdir)

shutil.move(tempdir, outputDir)
