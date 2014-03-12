# random file generator
import random
import string
import os
count=0
numoffiles=int(input("Input the number of files to be created: "))
yorn=input("Would you like to specify the length of the files? (y/n): ")
if yorn=="y":
    lengthoffiles=int(input("Input a length (in number of characters) for each file: "))
else:
    lengthoffiles=3000
if os.path.exists("c://randfiles"): #checks for directory
    dirpath="c://randfiles/"
    filelist=os.listdir(dirpath)
    for filename in filelist:
        os.remove(dirpath+filename) #removes files already in directory
else:
    os.makedirs("c://randfiles") #creates directory if it doesn't exist
with open("c://randfiles/text.txt", "w") as a_file: 
        for x in range(lengthoffiles):
            a_file.write("random")
count=1        
while True:
    with open("c://randfiles/text{0}.txt" .format(count), "w") as a_file: #creates file
        for x in range(lengthoffiles):
            a_file.write("random")
        if count==(numoffiles):
            os.startfile("c://randfiles") #opens the directory the files are in
            raise SystemExit("{0} files have been created in the direcory c://randfiles" .format(count))
    count += 1
