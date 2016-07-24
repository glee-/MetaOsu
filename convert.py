from lib import *
import shutil, os, errno
import eyed3
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
    return parse(f), files[1]

songdata = readSong()
print(songdata)
songdir = directory + songdata[0][0]
tempdir = directory + "temp_" + songdata[0][0]

shutil.copy2(songdir, tempdir)
metadata = songdata[0][1]

audiofile = eyed3.load(tempdir)
audiofile.tag.title = metadata[0].decode('unicode-escape')
audiofile.tag.artist = metadata[1].decode('unicode-escape')
audiofile.tag.album = metadata[2].decode('unicode-escape')
if songdata[1] != "":
    imagedata = open(songdata[1], "rb").read()
    if songdata[1][-4:] == ".jpg":
        audiofile.tag.images.set(3, imagedata, "image/jpeg")
    else:
        audiofile.tag.images.set(3, imagedata, "image/png")

audiofile.tag.save()

shutil.move(tempdir, outputDir)
