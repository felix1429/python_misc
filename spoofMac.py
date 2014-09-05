import winreg, random, sys, os, subprocess, multiprocessing, time, ipaddress, uuid, sys

results = [True]
toggleList = ["disable","enable"]
#wiredList = ["0c54a528785e","0c54a5791b29","0c54a53a5d63","0c54a5580c0c","0c54a5387803","0c54a5284279","0c54a52b3900","0c54a51c2925","0c54a5441e67","0c54a524117e","0c54a5765e36","0c54a564543b"]
#listList = [wiredList, wirelessList]
macList = ["02db3064780b","02db30356416","02db300e1773","02db30640e5f","02db30681a3b","02db302d174c","02db30570a0f","02db3028761a","02db30763301","02db30593f24","02db300f6f3e","02db30452657"]



def writeReg(mac, reg):
    try:
        aReg = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        keyVal = winreg.OpenKey(aReg, r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\000" + reg, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(keyVal,"NetworkAddress",0,winreg.REG_SZ,mac)
        print("Registry write completed successfully")
        return True
    except WindowsError:
        print("Registry write failed")
        sys.exit()


def getCurrentMac():
    output = subprocess.Popen("getmac", stdout=subprocess.PIPE)
    tmp = output.stdout.read().decode("utf-8")
    lineArray = tmp.split("\r\n")
    for line in lineArray:
        if "Device" in line:
            mac = line.split(' ')[0].strip().replace('-','').lower()
            break
    return mac


def generateMac():
    address = [0x0c, 0x54, 0xa5,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f)]
    return "".join(map(lambda x: '%02x' %x, address))


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
            endStr = "\n"
        print(x,end = endStr)
        sys.stdout.flush()
        time.sleep(1)


def initialize(fd):
    sys.stdin = os.fdopen(fd)


def getResults(boolean):
    results[0] = boolean


def toggleNetworkCard(toggleList, reg):
    for toggle in toggleList:
        subprocess.call("wmic path win32_networkadapter where index="
                                + reg + " call " + toggle)
        time.sleep(1)
    

if __name__ == "__main__":
	
    currentAddress = getCurrentMac()

    if currentAddress.startswith("0c"):
        reg = "0"
        address = generateMac()
    elif currentAddress.startswith("02"):
        reg = "2"
        macLength = len(macList)
        if currentAddress in macList:
            currentIndex = macList.index(currentAddress)
        else:
            for value in listList:
                if value != macList:
                    currentIndex = value.index(currentAddress)

        if(currentIndex != (macLength - 1)):
            address = macList[currentIndex + 1]
        else:
            address = macList[0]
    
    print("MAC address will be changed to " + address)    
    writeReg(address, reg)

    fn = [sys.stdin.fileno()] 
    p = multiprocessing.Pool(initializer = initialize, initargs = fn)
    q = multiprocessing.Pool()
    
    go = True
    while(go):
        p.apply_async(userInput, callback = getResults)
        q.apply(countdown)
        if(results[0]):
            toggleNetworkCard(toggleList, reg)
            go = False
        else:
            print("Postponing for 15 minutes")
            results[0] = True
            time.sleep(900)
            
