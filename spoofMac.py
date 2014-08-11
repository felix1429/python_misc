import winreg, random, sys, os, subprocess, multiprocessing, time, pyperclip, ipaddress, uuid

results = [True]
toggleList = ["disable","enable"]
macList = ["02db304a241f","02db30677369"]


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


def getCurrentMac():
    return (''.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]))

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


def copyToClipboard(macString):
    pyperclip.copy(macString)


def toggleNetworkCard(toggleList):
    for toggle in toggleList:
        subprocess.call("wmic path win32_networkadapter where index=2 "
                                + "call " + toggle)
        time.sleep(1)

    
def setIP():
    subprocess.call("netsh interface ip set address name=Wi-Fi "
                + "source=static addr=192.168.2.3 "
                + "mask=255.255.255.0 gateway=192.168.2.1 1")
    print("IP set")


def setDNS():
    subprocess.call("netsh interface ip set dns name=Wi-Fi "
                    + "source=static addr=8.8.8.8")
    time.sleep(1)
    subprocess.call("netsh interface ip add dns name=Wi-Fi "
                    + "addr=8.8.4.4 index=2")
    print("DNS set")
    
    
if __name__ == "__main__":
    currentAddress = getCurrentMac()
    
    for macAddress in macList:
        if(macAddress != currentAddress):
            address = macAddress
            break
        
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

    copyToClipboard(address)
    setIP()    
    setDNS()

