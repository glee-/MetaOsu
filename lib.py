import glob, os, re
import shutil, errno
import eyed3

#Assumes that we are in the song directory, parses song data
def readSong():
    files = getFileNames()
    f = open(files[0], "r")
    return parse(f), files[1]

# Gets file names, and returns in the format [.osu, background]
def getFileNames():
    osuFile = None
    for file in glob.glob("*.osu"):
        osuFile = file

    #prefer jpg over png
    imageTypes = ("*.jpg", "*.png")
    images = []
    imageFile = ""
    for type in imageTypes:
        images.extend(glob.glob(type))
    for image in images:
        if image.endswith("*.jpg"):
            imageFile = image
            break
        else:
            imageFile = image

    if osuFile == None:
        raise Exception("Couldn't find osu file!")
    return [osuFile, imageFile]

# Parses .osu file, and returns in the format [song, [title, artist, source]]
def parse(f):

    currline = None
    while (currline != "[General]"):
        currline = f.readline().strip()
    song = getSongFile(f)

    while (currline != "[Metadata]"):
        currline = f.readline().strip()
    data = getSongData(f)

    return [song, data]

#Gets song data, and returns in the format [title, artist, source]
def getSongData(f):
    #Assume at [Metadata] tag, extract title, artist, source
    title, artist, source = None, None, None
    currline = "None"

    while (currline[0] != ""):
        currline = f.readline().strip().split(":")
        if (currline[0] == "Title" or currline[0] == "TitleUnicode"):
            title = currline[1].strip()
        elif (currline[0] == "Artist" or currline[0] == "ArtistUnicode"):
            artist = currline[1].strip()
        elif (currline[0] == "Source"):
            source = currline[1].strip()

    return [title, artist, source]

#Gets filename of the song, and returns in the format "song"
def getSongFile(f):
    #Assume at [General] tag, returns song title (.mp3/.ogg)
    song = None
    currline = None

    while (song == None):
        currline = f.readline().strip().split(":")
        if (currline[0] == "AudioFilename"):
            song = currline[1].strip()

    return song

def editSong(directory, outputDir):
    try:
        songdata = readSong()
    except:
        print("Couldn't find directory for %s" % directory)
        writeDir(directory,outputDir)
        return

    print("Working on %s" % songdata[0][0])

    songdir = directory + songdata[0][0]
    songname = songdata[0][1][0].replace(" ", "") + songdata[0][0][-4:]
    songname = re.sub(r'[?|$|/|!]',r'', songname)
    tempdir = directory + "temp_" + songname

    # Skip .ogg files, as eyed3 cannot open it
    if (songdir[-4:] == ".ogg"):
        print("Skipped %s, due to .ogg" % songdir)
        writeDir(songdir,outputDir)
        return

    shutil.copy(songdir, tempdir)
    metadata = songdata[0][1]

    try:
        audiofile = eyed3.load(tempdir)
    except:
        os.remove(tempdir)
        print("Couldn't load %s, deleting..." % songdir)
        writeDir(songdir,outputDir)
        return

    if audiofile.tag == None:
        print("Couldn't load %s!" % songdir)
        writeDir(songdir,outputDir)
        return

    if metadata[0] != None:
        audiofile.tag.title = metadata[0].decode('unicode-escape')
    if metadata[1] != None:
        audiofile.tag.artist = metadata[1].decode('unicode-escape')
    if metadata[2] != None:
        audiofile.tag.album = metadata[2].decode('unicode-escape')

    if songdata[1] != "":
        imagedata = open(songdata[1], "rb").read()
        if songdata[1][-4:] == ".jpg":
            audiofile.tag.images.set(3, imagedata, "image/jpeg")
        else:
            audiofile.tag.images.set(3, imagedata, "image/png")

    try:
        audiofile.tag.save()
    except NotImplementedError:
        os.remove(tempdir)
        print("File type for %s not supported, deleting..." % songdir)
        writeDir(songdir,outputDir)
        return

#File already exists, so remove current work
    try:
        shutil.move(tempdir, outputDir)
    except:
        os.remove(tempdir)
        pass

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def writeDir(directory, outputDir):
    os.chdir(outputDir)
    file = open("Unread_Songs.txt", "ab")
    file.write(directory + "\n")
    file.close()
