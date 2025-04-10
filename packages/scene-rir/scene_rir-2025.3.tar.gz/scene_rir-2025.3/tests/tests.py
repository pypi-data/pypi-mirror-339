# -*- coding: utf-8 -*-
# tests\test.py

"""
    tests.py: Script for the testing of the scene_rir package.

    Copyright (C) 2025 Christos Sevastiadis

    License: GNU GPL v3.0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

import shutil
import numpy as np
import rir_plot
import scene_rir
import scipy as sp
from matplotlib import pyplot as plt
from scene_rir import rir

_AXIS_LEVEL_BOTTOM = -100  # decibell
_AXIS_LEVEL_TOP = 0  # decibell
_TIME_VECTOR_START = 0  # second

#######################################################################

help(scene_rir)

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
tmevec = np.linspace(_TIME_VECTOR_START, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(_AXIS_LEVEL_BOTTOM, _AXIS_LEVEL_TOP)
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
tmevec = np.linspace(_TIME_VECTOR_START, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(_AXIS_LEVEL_BOTTOM, _AXIS_LEVEL_TOP)
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
tmevec = np.linspace(_TIME_VECTOR_START, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(_AXIS_LEVEL_BOTTOM, _AXIS_LEVEL_TOP)
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
tmevec = np.linspace(_TIME_VECTOR_START, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(_AXIS_LEVEL_BOTTOM, _AXIS_LEVEL_TOP)
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
    "ss_rtetyp": "lin",
}
signal = rir.SweptSineSignal(params)
signal.save("output/ss-signal-04.wav")

(smprte, sglvec) = sp.io.wavfile.read("output/ss-signal-04.wav")
slcvec = np.zeros(int(DELAY_DURATION * smprte))
sglvec = np.concatenate((slcvec, sglvec))
sp.io.wavfile.write("input/rec-signal-04.wav", smprte, sglvec)
shutil.copy("output/ss-signal-04.wav", "input/ref-signal-04.wav")

params = {
    "rec_path": "input/rec-signal-04.wav",
    "ref_path": "input/ref-signal-04.wav",
    "ss_rtetyp": "lin",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-04.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

irssglvec = irs_signal.irssglvec
irssglvec[irssglvec == 0] = 10**-10
irssgllvlvec = 10 * np.log10(irssglvec**2)
sgldur = irssglvec.size / irs_signal.smprte
tmevec = np.linspace(_TIME_VECTOR_START, sgldur, irssglvec.size)
fix, ax = plt.subplots()
ax.set_ylim(_AXIS_LEVEL_BOTTOM, _AXIS_LEVEL_TOP)
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
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": "input/GrCLab1SSRPos2.wav",
    "ref_path": "input/Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab1SSRPos2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": r"input\GrCLab2SSRPos1Src1.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src1.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": r"input\GrCLab2SSRPos1Src2.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################
