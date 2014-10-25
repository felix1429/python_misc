#! c:/python34/scripts python
#creates an album and an artist folder in music and album art directory of both
#internal and external hdd

import os

def getArtist():
    while True:
        artist_name = str(input("Input the name of the artist: "))      
        try:
            if "/" in artist_name:
                raise OSError()
            os.makedirs("C://{0}".format(artist_name))
            os.removedirs("C://{0}".format(artist_name))
            return artist_name
        except OSError:
            print("Invalid character for file name, please "
                  + "input a different artist name")


def getAlbum():
    while True:
        album_name = str(input("Input the name of the album: "))
        try:
            if "/" in album_name:
                raise OSError()
            os.makedirs("C://{0}".format(album_name))
            os.removedirs("C://{0}".format(album_name))
            return album_name
        except OSError:
            print("Invalid character for file name, please "
                  + "input a different album name")

if __name__ == "__main__":
    artist_name = getArtist()
    album_name = getAlbum()
    w = "H://Music/Music/{0}/{1}".format(artist_name, album_name)
    x = "H://Music/Album Art/{0}/{1}".format(artist_name, album_name)
    dir_list = [w, x]
    for foo in dir_list:
        if os.path.exists(foo) is False:
            os.makedirs(foo)
        os.startfile(foo)
