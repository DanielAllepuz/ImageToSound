import numpy as np
from scipy.io.wavfile import write
from PIL import Image
import sys

if __name__ == "__main__":
    imagename = sys.argv[1] #Filename from command args
    maxfreq = 2800 #Freq corresponding to right edge
    minfreq = 100 #Freq corresponding to left edge

    #The image is loaded, converted to grayscale and transposed
    image = np.array(Image.open(imagename).convert("L").transpose(Image.ROTATE_180))

    rate = int(48000/4) #frames/s (values per second)
    T = 40/1000 #s duration of each row of the image
    t = np.linspace(0,T,int(T*rate)) #s times of each row

    waveblank = np.zeros(int(T*rate)) #an array filled with zeros
    width = len(image[0]) -1 #maximum column

    t0 = 0 #time, this is used to ensure continuity between rows

    waveform = [] #this is the final audio

    for r,row in enumerate(image):
        print(r/len(image)) #A way to know the progress
        wave = np.array(waveblank) #Audio for this column
        for c,value in enumerate(row):
            freq = minfreq*(maxfreq/minfreq)**(c/width)
            A = value/255.0
            wave += A*np.sin(2*np.pi*freq*(t + t0))
        t0 = t[-1] + t0
        waveform = waveform + list(wave)


    waveform = 32767*np.array(waveform)/max(np.abs(waveform))
    waveform = np.array(waveform, dtype = 'int16')
    write(imagename.split(".")[0] + ".wav", rate, waveform)
