from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from subprocess import call
import subprocess
import os
import signal
import socket
import time

def handleTimeOut():
    print 'Alarm Timeout Exception'
    raise TimeoutException()


def getFirefoxPort(firfoxport):
    cmnd = subprocess.Popen(["netstat","-nlpt"],stdout=subprocess.PIPE)
    (out , err) = cmnd.communicate()
    procs = out.split("\n")
    for i in range(2,len(procs)-1):
        splittedProc = procs[i].split(" ")
        proc = filter(lambda a: a!="",splittedProc)
        prog = proc[len(proc)-1].split("/")[1]
        if prog == 'firefox':
            firfoxport.append(proc[3].split(":")[1])
    return firfoxport

def myrefresh(site, n,port,ffports):
    count = 0
    call(["mkdir", "-p", "/mnt/dataset/uproxy/dump/%s" % (site)])
    for i in range(n, 50):
        try:
            try:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('localhost',port))
            except:
                count += 1
                print 'not connected'
                time.sleep(120)
                fireFoxPorts = getFirefoxPort(ffports)
                port = fireFoxPorts[count+1]
            if count== 5:
                exit(0)
            print i
            os.system("/usr/sbin/tcpdump -i eth1 -w /mnt/dataset/uproxy/dump/%s/%d.pcap &" % (site, i))
            driver.get(site)
            signal.alarm(300)
            WebDriverWait(driver, 5).until(EC.title_is('hkylgkhkk,bnkb'))
            print 'hello'
            signal.alarm(0)
        except Exception as e:
            print e
            pass
        finally:
            call(["killall", "tcpdump"])



profile = webdriver.FirefoxProfile()
path = '/home/shahrzad/.mozilla/firefox/t95q3p0x.default/extensions//jid1-uTe1Bgrsb76jSA@jetpack.xpi'
profile.add_extension(path)
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
profile.set_preference("network.http.max-connections", 1)
profile.set_preference("network.http.max-persistent-connections-per-proxy", 1)
profile.set_preference("network.http.max-persistent-connections-per-server", 1)
profile.set_preference("network.http.max-connections-per-server", 1)

driver = webdriver.Firefox(profile)
port = raw_input()
ffports = []
ffports = getFirefoxPort(ffports)
print ffports

driver.set_page_load_timeout(90)

f = open('websites1.txt', 'r')
for line in f:
    print line
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    directory = "/mnt/dataset/uproxy/dump/%s" % (line)
    if os.path.isdir(directory):
        pcaps = os.listdir(directory)
        number = 0
        for pcap in pcaps:
            number = max(number, int(pcap.split('.')[0]))
        print number
        myrefresh(line, number + 1,int(port),ffports)

    else:
        myrefresh(line, 0,int(port),ffports)
