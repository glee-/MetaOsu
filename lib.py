import glob, os
import shutil, errno
import eyed3

#Assumes that we are in the song directory, parses song data
def readSong():
    files = getFileNames()
    f = open(files[0], "r")
    return parse(f), files[1]

# Gets file names, and returns in the format [.osu, background]
def getFileNames():
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
    songdata = readSong()
    print("Working on %s" % songdata[0][0])
    songdir = directory + songdata[0][0]
    tempdir = directory + "temp_" + songdata[0][0]

    # Skip .ogg files, as eyed3 cannot open it
    if (songdir[-4:] == ".ogg"):
        print("Skipped %s, due to .ogg" % songdata[0][0])
        return

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

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
