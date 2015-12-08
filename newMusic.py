#! c:/python34/scripts python
#creates an album and an artist folder in music and album art directory of both

import os, argparse

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
                   
if __name__ == "__main__":
    args = initArgs()
    artist_name = getArtist(args)
    album_name = getAlbum(args, artist_name)
    w = "H://Music/Music/{0}/{1}".format(artist_name, album_name)
    x = "H://Music/Album Art/{0}/{1}".format(artist_name, album_name)
    dir_list = [w, x]
    for foo in dir_list:
        if os.path.exists(foo) is False:
            os.makedirs(foo)
        os.startfile(foo)
