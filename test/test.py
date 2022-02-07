from email.mime import audio
from moviepy.editor import *

video = VideoFileClip("Cant Hold Us (feat Ray Dalton).mp4")
audio = video.audio
audio.write_audiofile("Cant Hold Us (feat Ray Dalton).mp3")