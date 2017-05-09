import time
from subprocess import call

def live_stream(width,height):
    try:
        call(["uv4l","--driver","raspicam","--auto-video_nr","--encoding","h264","--width",width,"--height",height,"--enable-server","on"])
        time.sleep(0.05)
    except:
        pass
        
def kill_stream():
    call(["pkill","uv4l"])
    time.sleep(0.05)

def main():
    t = input("enter amount of time to watch stream:")
    print ("Streaming for {} seconds".format(t))

    width ='1080'
    height = '720'

    live_stream(width,height)
    time.sleep(0.05)
    time.sleep(t)
    kill_stream()
    time.sleep(0.05)
    print ("Stream Ends")

try:
    pass
    #main()
    #time.sleep(1)
except KeyboardInterrupt:
    kill_stream()
    time.sleep(0.05)
    exit()
