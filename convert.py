from lib import *
import shutil, os, errno

# directory = "/home/geo/git/MetaOsu/Songs/"
directory = "/home/geo/PlayOnLinux's virtual drives/osu_on_linux/drive_c/Program Files/osu!/Songs/"
outputDir = "/home/geo/git/MetaOsu/output/"

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
    os.rename(tempfiles[i], tempfiles[i][5:])
