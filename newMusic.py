#! c:/python34/scripts python
#creates an album and an artist folder in music and album art directory of both

import os, argparse, requests, json, urllib

def getArtist(args):
    if args.a:
        return getLastArtist()
    else:
        artist = getInput("artist")
        writeFile(artist)
        return artist

def getAlbum(args, artistName):
    if args.s:
        return artistName
    else:
        return getInput("album")

def validateName(name, foo):
    try:
        if "/" in name:
            raise OSError()
        os.makedirs("C://{0}".format(name))
        os.removedirs("C://{0}".format(name))
        return True
    except OSError:
        print("Invalid character for file name, please "
              + "input a different " + foo + " name")
        return False
    
def getInput(foo):
    while True:
        name = str(input("Input the name of the " + foo + ": "))
        if validateName(name, foo):
            return name    

def getLastArtist():
    with open("artist.file", "r") as file:
        return file.read()

def writeFile(artist):
    with open("artist.file", "w") as file:
        file.write(artist)

def defineArgs(parser):
    parser.add_argument("-a", help = "set the artist as the last artist entered",
                        action = "store_true")
    parser.add_argument("-s", help = "set the album name as the name of the artist",
                        action = "store_true")
    return parser

def initArgs():
    parser = defineArgs(argparse.ArgumentParser())
    args = parser.parse_args()
    return args

def fetchAlbumArt(artist, album, path):
    url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?term=" + album + " " + artist + "&entity=album"
    try:
        response = requests.get(url)
        data = response.json()
        artUrl = data["results"][0]["artworkUrl100"]
        hiResUrl = artUrl.replace("100x100bb", "100000x100000-999")
        img = urllib.request.urlopen(hiResUrl)
        saveImage(img, path)
    except e:
        print("didn't work: " + e)

def saveImage(img, path):
    with open(path + "cover.jpg", "wb") as file:
        file.write(img.read())
                   
if __name__ == "__main__":
    args = initArgs()
    artistName = getArtist(args)
    albumName = getAlbum(args, artistName)
    w = "H://Music/Music/{0}/{1}/".format(artistName, albumName)
    x = "H://Music/Album Art/{0}/{1}/".format(artistName, albumName)
    dirList = [w, x]
    for foo in dirList:
        if os.path.exists(foo) is False:
            os.makedirs(foo)
        os.startfile(foo)
    fetchAlbumArt(artistName, albumName, x)
