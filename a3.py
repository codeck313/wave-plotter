import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import wave
import os

fileNames = os.listdir('./data')
if not os.path.exists('output'):
    os.makedirs('output')

for _file in fileNames:
    print(_file)
    s_wave = wave.open('data/'+_file, 'r')
    signalToPlot = np.frombuffer(s_wave.readframes(-1), dtype=np.int16)
    deinterleaved = [signalToPlot[idx::s_wave.getnchannels()]
                     for idx in range(s_wave.getnchannels())]

    mpl.style.use('seaborn')
    plt.figure(1)
    bitRate = s_wave.getframerate()
    time = np.linspace(0, len(signalToPlot)/s_wave.getnchannels() /
                       bitRate, num=int(len(signalToPlot)/s_wave.getnchannels()))
    plot_t = plt.subplot(211)
    plot_f = plt.subplot(212)
    plt.suptitle(_file)
    plot_t.set_ylabel('Signal')
    plot_t.set_xlabel('Time \n')
    plot_f.set_ylabel('Signal')
    plot_f.set_xlabel('Frequency')
    for channel in deinterleaved:
        plot_t.plot(time, channel, linewidth=.125)
        plot_f.specgram(channel, NFFT=1024, Fs=bitRate,
                        noverlap=900, cmap='plasma')
    plt.tight_layout()
    plt.savefig('output/'+_file+'.png', dpi=512)
    plt.close()
print("---DONE---")
