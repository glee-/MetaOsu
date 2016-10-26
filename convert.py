from lib import *
import os

directory = "Directory here"
outputDir = "Directory here"

#Examples
# directory = "/home/geo/git/MetaOsu/Songs/"
# outputDir = "/home/geo/git/MetaOsu/output/"


os.chdir(directory)

if (directory[-1:] != '/'):
    directory += '/'

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

tempdirs = []

for root, dirs, files in walklevel(directory):
    tempdir = root + '/'
    if not directory == (tempdir):
        tempdirs.append(tempdir)

for tempdir in tempdirs:
    os.chdir(tempdir)
    editSong(tempdir, outputDir)

os.chdir(outputDir)
tempfiles = os.listdir(outputDir)
for i in range(len(tempfiles)):
    if (tempfiles[i][:5]) == "temp_":
        os.rename(tempfiles[i], tempfiles[i][5:])
