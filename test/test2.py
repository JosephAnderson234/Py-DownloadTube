from pytube import YouTube

YouTube("https://youtu.be/96L5sV7rqX0").streams.first().download()
