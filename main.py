import sys
import numpy as np
import sounddevice as sd
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

#Audio Settings
CHUNK = 1024
RATE = 44100

#Circular Waveform Buffer
buffer = np.zeros(CHUNK * 10)

app = QApplication(sys.argv)

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("Live Microphone Oscilloscope")

plot = win.addPlot()
plot.setYRange(-1, 1)

curve = plot.plot()

def audio_callback(indata, frames, time, status):
    global buffer

    samples = indata[:, 0]

    buffer = np.roll(buffer, -len(samples))
    buffer[-len(samples):] = samples

stream = sd.InputStream(
    channels=1,
    samplerate=RATE,
    blocksize=CHUNK,
    callback=audio_callback
)

stream.start()

timer = pg.QtCore.QTimer()

def update():
    curve.setData(buffer)

timer.timeout.connect(update)
timer.start(20)

sys.exit(app.exec_())
