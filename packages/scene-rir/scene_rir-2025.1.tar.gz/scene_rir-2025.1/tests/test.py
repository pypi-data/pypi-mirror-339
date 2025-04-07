# -*- coding: utf-8 -*-
# tests\test.py

import scene_rir.rir as rir
import rir_plot
from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
import shutil

#######################################################################

help(rir)

#######################################################################

DELAY_DURATION = 0
SIGNAL_LEVEL = -3

signal = rir.SweptSineSignal()
signal.save("output/ss-signal-00.wav")

shutil.copy("output/ss-signal-00.wav", "input/rec-signal-00.wav")
shutil.copy("output/ss-signal-00.wav", "input/ref-signal-00.wav")

params = {
    "rec_path": "input/rec-signal-00.wav",
    "ref_path": "input/ref-signal-00.wav",
    "sgllvl": SIGNAL_LEVEL,
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-00.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

irssglvec = irs_signal.irssglvec
irssglvec[irssglvec == 0] = 10**-10
irssgllvlvec = 10 * np.log10(irssglvec**2)
sgldur = irssglvec.size / irs_signal.smprte
tmevec = np.linspace(0, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(-100, 0)
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(SIGNAL_LEVEL, color="yellow")
ax.plot(tmevec, irssgllvlvec)
fix, ax = plt.subplots()
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(10 ** (SIGNAL_LEVEL / 20), color="yellow")
ax.plot(tmevec, irssglvec)
plt.show()

sp.io.wavfile.write("input/inv-signal-00.wav", irs_signal.smprte, irs_signal._invrefvec)

#######################################################################

DELAY_DURATION = 0.5
SIGNAL_LEVEL = -3

signal = rir.SweptSineSignal()
signal.save("output/ss-signal-01.wav")

(smprte, sglvec) = sp.io.wavfile.read("output/ss-signal-01.wav")
slcvec = np.zeros(int(DELAY_DURATION * smprte))
sglvec = np.concatenate((slcvec, sglvec))
sp.io.wavfile.write("input/rec-signal-01.wav", smprte, sglvec)
shutil.copy("output/ss-signal-01.wav", "input/ref-signal-01.wav")


params = {
    "rec_path": "input/rec-signal-01.wav",
    "ref_path": "input/ref-signal-01.wav",
    "sgllvl": SIGNAL_LEVEL,
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-01.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

irssglvec = irs_signal.irssglvec
irssglvec[irssglvec == 0] = 10**-10
irssgllvlvec = 10 * np.log10(irssglvec**2)
sgldur = irssglvec.size / irs_signal.smprte
tmevec = np.linspace(0, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(-100, 0)
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(SIGNAL_LEVEL, color="yellow")
ax.plot(tmevec, irssgllvlvec)
fix, ax = plt.subplots()
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(10 ** (SIGNAL_LEVEL / 20), color="yellow")
ax.plot(tmevec, irssglvec)
plt.show()

#######################################################################

DELAY_DURATION = 0
SIGNAL_LEVEL = -3

params = {
    "antslcdur": 0.3,
    "pstslcdur": 0.3,
}
signal = rir.SweptSineSignal(params)
signal.save("output/ss-signal-02.wav")

shutil.copy("output/ss-signal-02.wav", "input/rec-signal-02.wav")
shutil.copy("output/ss-signal-02.wav", "input/ref-signal-02.wav")

params = {
    "rec_path": "input/rec-signal-02.wav",
    "ref_path": "input/ref-signal-02.wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-02.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

irssglvec = irs_signal.irssglvec
irssglvec[irssglvec == 0] = 10**-10
irssgllvlvec = 10 * np.log10(irssglvec**2)
sgldur = irssglvec.size / irs_signal.smprte
tmevec = np.linspace(0, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(-100, 0)
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(SIGNAL_LEVEL, color="yellow")
ax.plot(tmevec, irssgllvlvec)
fix, ax = plt.subplots()
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(10 ** (SIGNAL_LEVEL / 20), color="yellow")
ax.plot(tmevec, irssglvec)
plt.show()

#######################################################################

DELAY_DURATION = 0.5
SIGNAL_LEVEL = -3

params = {
    "antslcdur": 0.3,
    "pstslcdur": 0.3,
}
signal = rir.SweptSineSignal(params)
signal.save("output/ss-signal-03.wav")

(smprte, sglvec) = sp.io.wavfile.read("output/ss-signal-03.wav")
slcvec = np.zeros(int(DELAY_DURATION * smprte))
sglvec = np.concatenate((slcvec, sglvec))
sp.io.wavfile.write("input/rec-signal-03.wav", smprte, sglvec)
shutil.copy("output/ss-signal-03.wav", "input/ref-signal-03.wav")


params = {
    "rec_path": "input/rec-signal-03.wav",
    "ref_path": "input/ref-signal-03.wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-03.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

irssglvec = irs_signal.irssglvec
irssglvec[irssglvec == 0] = 10**-10
irssgllvlvec = 10 * np.log10(irssglvec**2)
sgldur = irssglvec.size / irs_signal.smprte
tmevec = np.linspace(0, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(-100, 0)
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(SIGNAL_LEVEL, color="yellow")
ax.plot(tmevec, irssgllvlvec)
fix, ax = plt.subplots()
ax.set_xlim(-0.1, sgldur)
ax.axvline(DELAY_DURATION, color="red")
ax.axhline(10 ** (SIGNAL_LEVEL / 20), color="yellow")
ax.plot(tmevec, irssglvec)
plt.show()

#######################################################################

params = {
    "rec_path": "input/GrCLab1SSRPos2.wav",
    "ref_path": "input/Sweep(10-22000Hz,10s-0.2s).wav",
    "frqstt": 10,
    "frqstp": 22000,
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab1SSRPos2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "rec_path": r"input\GrCLab2SSRPos1Src1.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
    "frqstt": 10,
    "frqstp": 22000,
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src1.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "rec_path": r"input\GrCLab2SSRPos1Src2.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
    "frqstt": 10,
    "frqstp": 22000,
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################
