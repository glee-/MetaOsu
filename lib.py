import glob, os
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

# Gets file names, and returns in the format [.osu, background]
def getFileNames():
    for file in glob.glob("*.osu"):
        osuFile = file

    #prefer jpg over png
    imageTypes = ("*.jpg", "*.png")
    images = []
    for type in imageTypes:
        images.extend(glob.glob(type))
    for image in images:
        if image.endswith("*.jpg"):
            imageFile = image
            break
        else:
            imageFile = image

    return [osuFile, imageFile]
