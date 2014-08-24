import winreg, random, sys, os, subprocess, multiprocessing, time, ipaddress, uuid, sys

results = [True]
toggleList = ["disable","enable"]
macList = ["02db304a241f","02db30677369","02db302e0e75"]
macLength = len(macList)


def writeReg(mac):
    try:
        aReg = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        keyVal = winreg.OpenKey(aReg, r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0002", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(keyVal,"NetworkAddress",0,winreg.REG_SZ,mac)
        print("Registry write completed successfully")
        return True
    except WindowsError:
        print("Registry write failed")
        sys.exit()


def getCurrentMac():
    output = subprocess.Popen("getmac", stdout=subprocess.PIPE)
    tmp = output.stdout.read().decode("utf-8")
    lineArray = tmp.split("\n")
    for line in lineArray:
        if line.lstrip().startswith("02"):
            mac = line.split(' ')[0].strip().replace('-','').lower()
            print(mac)
            break
    return mac


def userInput():
    var = str(input("Would you like to continue and reset the network? (n to postpone\n) "))
    sys.stdout.flush()
    if(var == "n" or var == "N"):
        return False
    else:
        return True


def countdown():
    for x in range(10,0,-1):
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


def toggleNetworkCard(toggleList):
    for toggle in toggleList:
        subprocess.call("wmic path win32_networkadapter where index=2 "
                                + "call " + toggle)
        time.sleep(1)
    

if __name__ == "__main__":
	
    currentAddress = getCurrentMac()
    currentIndex = macList.index(currentAddress)

    if(currentIndex != (macLength - 1)):
        address = macList[currentIndex + 1]
    else:
        address = macList[0]
        
    print("MAC address will be changed to " + address)    
    writeReg(address)

    fn = [sys.stdin.fileno()] 
    p = multiprocessing.Pool(initializer = initialize, initargs = fn)
    q = multiprocessing.Pool()
    
    go = True
    while(go):
        p.apply_async(userInput, callback = getResults)
        q.apply(countdown)
        if(results[0]):
            toggleNetworkCard(toggleList)
            go = False
        else:
            print("Postponing for 15 minutes")
            results[0] = True
            time.sleep(900)

	
