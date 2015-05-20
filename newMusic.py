#! c:/python34/scripts python
#creates an album and an artist folder in music and album art directory of both
#internal and external hdd

import os, argparse

def getArtist(args):
    if args.a:
        return getLastArtist()
    while True:
        artistName = str(input("Input the name of the artist: "))      
        try:
            if "/" in artistName:
                raise OSError()
            os.makedirs("C://{0}".format(artistName))
            os.removedirs("C://{0}".format(artistName))
            writeFile(artistName)
            return artistName
        except OSError:
            print("Invalid character for file name, please "
                  + "input a different artist name")

def getAlbum():
    while True:
        albumName = str(input("Input the name of the album: "))
        try:
            if "/" in albumName:
                raise OSError()
            os.makedirs("C://{0}".format(albumName))
            os.removedirs("C://{0}".format(albumName))
            return albumName
        except OSError:
            print("Invalid character for file name, please "
                  + "input a different album name")

def getLastArtist():
    with open("artist.file", "r") as file:
        return file.read()

def writeFile(artist):
    with open("artist.file", "w") as file:
        file.write(artist)
                   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help = "set the artist as the last artist entered",
                        action = "store_true")
    args = parser.parse_args() 
    artist_name = getArtist(args)
    album_name = getAlbum()
    w = "H://Music/Music/{0}/{1}".format(artist_name, album_name)
    x = "H://Music/Album Art/{0}/{1}".format(artist_name, album_name)
    dir_list = [w, x]
    for foo in dir_list:
        if os.path.exists(foo) is False:
            os.makedirs(foo)
        os.startfile(foo)
