import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import wave
import os
from scipy.io import wavfile
import scipy.signal as sps

fileNames = os.listdir('./data')
if not os.path.exists('output'):
    os.makedirs('output')
nBitRate = 36
for _file in fileNames:
    print(_file)
    s_wave = wave.open('data/'+_file, 'r')
    _file = _file.split('.')[0]
    bitRate = s_wave.getframerate()
    signalToPlot = np.frombuffer(s_wave.readframes(-1), dtype=np.int16)
    deinterleaved = [signalToPlot[idx::s_wave.getnchannels()]
                     for idx in range(s_wave.getnchannels())]

    mpl.style.use('seaborn')
    # plt.figure(figsize=(17.0, 10.0))
    time = np.linspace(0, len(signalToPlot)/s_wave.getnchannels() /
                       bitRate, num=int(len(signalToPlot)/s_wave.getnchannels()))
    plot_t = plt.subplot(211)
    plot_f = plt.subplot(212)
    plt.suptitle(_file)
    plot_t.set_ylabel('Signal')
    plot_t.set_xlabel('Time \n')
    plot_f.set_ylabel('Frequency')
    plot_f.set_xlabel('Time')
    for channel in deinterleaved:
        plot_t.plot(time, channel, linewidth=.2)
        plot_f.specgram(channel, NFFT=1024, Fs=bitRate,
                        noverlap=900, cmap='plasma')
    plt.tight_layout()
    # plt.show()
    plt.savefig('output/'+_file+'.png', dpi=512)
    plt.close()

    # RESAMPLE
    plt.figure(figsize=(17.0, 5.0))
    number_of_samples = round(
        len(signalToPlot) * float(nBitRate) / bitRate)
    signalToPlot = sps.resample(signalToPlot, number_of_samples)
    deinterleaved = [signalToPlot[idx::s_wave.getnchannels()]
                     for idx in range(s_wave.getnchannels())]
    mpl.style.use('seaborn')
    time = np.linspace(0, len(signalToPlot)/s_wave.getnchannels() /
                       nBitRate, num=int(len(signalToPlot)/s_wave.getnchannels()))
    plt.suptitle(_file+'-Discrete', fontsize=25)
    plt.ylabel('Signal')
    plt.xlabel('Time \n')
    for channel in deinterleaved:
        plt.stem(time, channel)
    plt.tight_layout()
    # plt.show()
    plt.savefig('output/'+_file+'-Discrete.png', dpi=200)
    plt.close()

print("---DONE---")
