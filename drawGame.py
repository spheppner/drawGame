# from https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
import pyaudio
import numpy as np
import PIL

maxValue = 2**16
bars = 35
CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=44100,
              input=True, frames_per_buffer=1024)
while True:
    data2 = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data2 = data2 * np.hanning(len(data2)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data2).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    #print("peak frequency: %d Hz"%freqPeak)
    ##
    data = np.fromstring(stream.read(1024),dtype=np.int16)
    dataL = data[0::2]
    dataR = data[1::2]
    peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
    peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
    lString = "#"*int(peakL*bars)#+"-"*int(bars-peak*bars)
    rString = "#"*int(peakR*bars)
    print("[%s"%(lString)+"][%s"%(rString)+"]")
    print("Hz: ["+"+"*int(freqPeak / 100)+"]")
    


