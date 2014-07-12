import winreg, random, sys, os, subprocess, multiprocessing, time

results = [True]
def writeReg(mac):
    try:
        aReg = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        keyVal = winreg.OpenKey(aReg, r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0002", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(keyVal,"NetworkAddress",0,winreg.REG_SZ,mac)
        print("Registry write completed successfully")
        return True
    except WindowsError:
        print("Registry write failed")
        return False

def generateMac():
    address = [0x02, 0xDB, 0x30,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f)]
    return "".join(map(lambda x: '%02x' %x, address))

def userInput():
    var = str(input("Would you like to continue and reset the network? (y/n) "))
    sys.stdout.flush()
    if(var == "y" or var == "Y"):
        return True
    else:
        return False

def countdown():
    for x in range(15,0,-1):
        if(x != 1):
            endStr = ", "
        else:
            endStr = ""
        print(x,end = endStr)
        sys.stdout.flush()
        time.sleep(1)

def initialize(fd):
    sys.stdin = os.fdopen(fd)

def getResults(boolean):
    results[0] = boolean
    
if __name__ == "__main__":
    writeReg(generateMac())

    fn = [sys.stdin.fileno()] 
    p = multiprocessing.Pool(initializer = initialize, initargs = fn)
    q = multiprocessing.Pool()
    
    go = True
    while(go):
        p.apply_async(userInput, callback = getResults)
        q.apply(countdown)
        if(results[0]):
            subprocess.call("wmic path win32_networkadapter where index=2 call disable")
            subprocess.call("wmic path win32_networkadapter where index=2 call enable")
            go = False
        else:
            print("Postponing for 15 minutes")
            results[0] = True
            time.sleep(900)
            
