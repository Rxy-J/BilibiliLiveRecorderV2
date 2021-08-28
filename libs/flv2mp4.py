import os

TRANSFORM = "{0} -y -i {1} -c copy {2}"

def flv2mp4(ffmpeg, flv, mp4):
    command = TRANSFORM.format(ffmpeg, "\""+flv+"\"", "\""+mp4+"\"")
    os.system(command)
