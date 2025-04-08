# -*- coding: utf-8 -*-
# examples\scene-signals.py

import scene_rir.rir as rir
import shutil
import os

# Swetp-sine excitation signals production
# The produced signals are stored to the output folder, and they are copied to the input folder, to be used as reference signals, in the impulse response extraction from a recorder signal response.

ss_params_1 = {
    "sglszeidx": 1,
}
ss_signal_1 = rir.SweptSineSignal(ss_params_1)
ss_signal_1.save("output/ss-signal-44100_kHz-743_ms.wav")
if not os.path.exists("input"):
    os.makedirs("input")
shutil.copy("output/ss-signal-44100_kHz-743_ms.wav", "input/ss-signal-44100_kHz-743_ms.wav")

ss_params_2 = {
    "sglszeidx": 3,
}
ss_signal_2 = rir.SweptSineSignal(ss_params_2)
ss_signal_2.save("output/ss-signal-44100_kHz-2972_ms.wav")
if not os.path.exists("input"):
    os.makedirs("input")
shutil.copy(     "output/ss-signal-44100_kHz-2972_ms.wav", "input/ss-signal-44100_kHz-2972_ms.wav")

ss_params_3 = {
    "sglszeidx": 5,
}
ss_signal_3 = rir.SweptSineSignal(ss_params_3)
ss_signal_3.save("output/ss-signal-44100_kHz-11889_ms.wav")
if not os.path.exists("input"):
    os.makedirs("input")
shutil.copy(     "output/ss-signal-44100_kHz-11889_ms.wav", "input/ss-signal-44100_kHz-11889_ms.wav")


# The produced signals are tested by themselfs, and almost Kronecker delta functions signal should be extracted.

irs_params_1 = {
    "rec_path": "input/ss-signal-44100_kHz-743_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-743_ms.wav",
}
irs_signal_1 = rir.ImpulseResponseSignal(irs_params_1)
irs_signal_1.save("output/irs-signal-44100_kHz-743_ms.wav")

irs_params_2 = {
    "rec_path": "input/ss-signal-44100_kHz-2972_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-2972_ms.wav",
}
irs_signal_2 = rir.ImpulseResponseSignal(irs_params_2)
irs_signal_2.save("output/irs-signal-44100_kHz-2972_ms.wav")

irs_params_3 = {
    "rec_path": "input/ss-signal-44100_kHz-11889_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-11889_ms.wav",
}
irs_signal_3 = rir.ImpulseResponseSignal(irs_params_3)
irs_signal_3.save("output/irs-signal-44100_kHz-11889_ms.wav")
