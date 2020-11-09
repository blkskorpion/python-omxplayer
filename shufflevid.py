
import os
import random
import signal
import subprocess
import re
import time

from decimal import Decimal

## Code original found here:
## http://www.baconisafruit.com/2014/07/raspberry-pi-random-videos-at-boot.html
 
## Mods:
## Play window projection videos for halloween. Provide your own videos
## Calculate all video duration
## Smooth transition among videos by forcing font color to black
## Shuffle videos, play all before shuffling again
## Turn raspeberry off when done
## Modify rc.local to start running on powerup:
## sudo python /home/pi/shufflevid.py


## Place mp4 videos (H264 encoding) on /home/pi/
## Declare omxplayer video cli

vid0="/usr/bin/omxplayer -b -o hdmi --win -200,-100,1500,1000 /home/pi/spider.mp4"
vid1="/usr/bin/omxplayer -b -o hdmi --orientation 90 /home/pi/girl.mp4"
vid2="/usr/bin/omxplayer -b -o hdmi /home/pi/bride1.mp4"
vid3="/usr/bin/omxplayer -b -o hdmi /home/pi/bride2.mp4"
vid4="/usr/bin/omxplayer -b -o hdmi /home/pi/bride3.mp4"
vid5="/usr/bin/omxplayer -b -o hdmi /home/pi/bride4.mp4"
vid6="/usr/bin/omxplayer -b -o hdmi --win -1200,-500,2600,2800 /home/pi/orb1.mp4"

vid10="/usr/bin/omxplayer -b -o hdmi --win -1200,-600,2300,1800 /home/pi/ghost1.mp4"
vid11="/usr/bin/omxplayer -b -o hdmi --win -1200,0,2300,1800 /home/pi/ghost2.mp4"
vid12="/usr/bin/omxplayer -b -o hdmi --win -1200,-200,2300,1800 /home/pi/ghost3.mp4"
vid13="/usr/bin/omxplayer -b -o hdmi --win -1250,-150,2300,1800 /home/pi/ghost4.mp4"
vid14="/usr/bin/omxplayer -b -o hdmi --win -1200,-300,2300,1800 /home/pi/ghost5.mp4"
vid15="/usr/bin/omxplayer -b -o hdmi --win -1200,-300,2300,1800 /home/pi/ghost6.mp4"
vid16="/usr/bin/omxplayer -b -o hdmi --win -1200,0,2300,1800 /home/pi/ghost7.mp4"
vid17="/usr/bin/omxplayer -b -o hdmi --win -1200,-200,2300,1800 /home/pi/ghost8.mp4"
vid18="/usr/bin/omxplayer -b -o hdmi --win -1200,0,2300,1800 /home/pi/ghost9.mp4"


## Create list of videos
vidlist = []
vidlist.append (vid0)
vidlist.append (vid1)
vidlist.append (vid2)
vidlist.append (vid3)
vidlist.append (vid4)
vidlist.append (vid5)
vidlist.append (vid6)

vidlist.append (vid10)
vidlist.append (vid11)
vidlist.append (vid12)
vidlist.append (vid13)
vidlist.append (vid14)
vidlist.append (vid15)
vidlist.append (vid16)
vidlist.append (vid17)
vidlist.append (vid18)



def get_video_length(path):  
    # determines the video duration in seconds  

    process = subprocess.Popen(['/usr/bin/omxplayer', '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    stdout, stderr = process.communicate()  

    #print stdout
    # Regex borrowed from http://www.codingwithcody.com/2012/04/get-video-duration-with-ffmpeg-and-python/. Luckily omxplayer has the same output as ffmpeg.  
    matches = re.search(r'Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),', stdout, re.DOTALL).groupdict()  

    hours = Decimal(matches['hours'])  
    minutes = Decimal(matches['minutes'])  
    seconds = Decimal(matches['seconds'])  

    total = 0  
    total += 60 * 60 * hours  
    total += 60 * minutes  
    total += seconds  

    return int(total)  

def play_video(duration,vidstr):
    # Plays a video 

    os.system ('echo -e "Default \e[30mBlack"')
    process = subprocess.Popen(vidstr)

    os.system("clear")
    time.sleep(duration+3)  
    subprocess.Popen('killall omxplayer.bin', shell=True)  
    os.system("clear")
    return  

def mymain(flag,playtime):

    totalduration=0
    end = time.time() + playtime

    selectedlist = vidlist[:]
    random.shuffle (selectedlist)
    vidcount  = len (selectedlist)

    while( time.time()  < end):

        count = len ( selectedlist )

        if ( count==0 ):
            selectedlist = vidlist[:]
            random.shuffle (selectedlist)
            if  flag==0:
                break


        vid = selectedlist.pop(0)
        selectedvid = vid.split()

        fullpath = selectedvid[-1]
        #print fullpath
        #print  selectedvid


        duration = get_video_length(fullpath)
        #print fullpath, duration
        totalduration = totalduration + duration
        if flag==0:
            #print fullpath, duration
            pass
        else:
            play_video(duration,selectedvid)

    return totalduration,vidcount



## Calculate play duration within 25 seconds
total,vidcount = mymain(0,25)


## Calculate loop for 4hours
loopcount = (4*3600)/(total+3)
mymain(1, (total+3)*loopcount )


## Change font color
os.system('echo -e "Default \e[97White"')


## Turn off raspberry pi
os.system("sudo poweroff")



