# -*- coding: utf-8 -*-
# src\scene_rir\__init__.py

"""
    Room Impulse Response extraction package.

    The purpose of the package is to extract the room impulse response (RIR) from the
    recorded response signal of a proper excitation signal. It is part of the Audio
    Simulation Module of the Horizon project SCENE.

    Modules:
    - rir: Provides the classes implementing swept-sine excitation signal creation and
        room impulse response extraction from a recorded response.

    Example:
    >>>from scene_rir import rir
    >>>
    >>>signal = rir.SweptSineSignal()
    >>>signal.save("output/ss-signal.wav")
    >>>
    >>>params = {
    >>>    "rec_path": "input/rec-signal.wav",
    >>>    "ref_path": "input/ref-signal.wav",
    >>>}
    >>>irs_signal = rir.ImpulseResponseSignal(params)
    >>>irs_signal.save("output/irs-signal.wav")

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

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # for Python<3.8

__version__ = version(__name__)
