# -*- coding: utf-8 -*-
# examples\scene-signals.py

"""
    scene-signals.py: Creates and tests three typical swept-sine excitation signals.

    Creates the needed excitation signal `.wav' files for the Audio Simulation Module,
    of the Horizon project SCENE. The produced signals have durations of 743 ms, 2972
    ms, and 11889 ms, corresponding to typical small, medium and large rooms. All the
    files are stored in a `output` directory, in the execution path. The produced
    signals are tested by themselfs, as recorded and reference signal. The extracted
    impulse responses should be Kronecker delta functions signals, stored in the
    `output` directory.

    Usage:
    >python.exe scene-signals.py

    or

    >python3 scene-signals.py

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
from pathlib import Path
from scene_rir import rir

# Swept-sine excitation signals creation

# Short duration time signal, for small rooms
ss_params_1 = {
    "sglszeidx": 1,
}
ss_signal_1 = rir.SweptSineSignal(ss_params_1)
ss_signal_1.save("output/ss-signal-44100_kHz-743_ms.wav")

# Medium duration time signal, for medium rooms
ss_params_2 = {
    "sglszeidx": 3,
}
ss_signal_2 = rir.SweptSineSignal(ss_params_2)
ss_signal_2.save("output/ss-signal-44100_kHz-2972_ms.wav")

# Long duration time signal, for large rooms
ss_params_3 = {
    "sglszeidx": 5,
}
ss_signal_3 = rir.SweptSineSignal(ss_params_3)
ss_signal_3.save("output/ss-signal-44100_kHz-11889_ms.wav")

# Produced swept-sine excitation signals testing

# Copy the produced signals to an input directory
p = Path("input")
if not p.exists():
    p.mkdir(parents=True)
shutil.copy(
    "output/ss-signal-44100_kHz-743_ms.wav", "input/ss-signal-44100_kHz-743_ms.wav"
)
shutil.copy(
    "output/ss-signal-44100_kHz-2972_ms.wav", "input/ss-signal-44100_kHz-2972_ms.wav"
)
shutil.copy(
    "output/ss-signal-44100_kHz-11889_ms.wav", "input/ss-signal-44100_kHz-11889_ms.wav"
)

# Test the short duration time signal
irs_params_1 = {
    "rec_path": "input/ss-signal-44100_kHz-743_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-743_ms.wav",
}
irs_signal_1 = rir.ImpulseResponseSignal(irs_params_1)
irs_signal_1.save("output/irs-signal-44100_kHz-743_ms.wav")

# Test the medium duration time signal
irs_params_2 = {
    "rec_path": "input/ss-signal-44100_kHz-2972_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-2972_ms.wav",
}
irs_signal_2 = rir.ImpulseResponseSignal(irs_params_2)
irs_signal_2.save("output/irs-signal-44100_kHz-2972_ms.wav")

# Test the long duration time signal
irs_params_3 = {
    "rec_path": "input/ss-signal-44100_kHz-11889_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-11889_ms.wav",
}
irs_signal_3 = rir.ImpulseResponseSignal(irs_params_3)
irs_signal_3.save("output/irs-signal-44100_kHz-11889_ms.wav")
