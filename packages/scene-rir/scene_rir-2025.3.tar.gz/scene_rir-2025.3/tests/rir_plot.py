# -*- coding: utf-8 -*-
# tests\rir_plot.py

"""
    rir_plot.py: Provides plotting functions for the tests.

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

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from scene_rir.rir import ImpulseResponseSignal


def _set_ax_semilog_limits(ax: Axes, vec: np.ndarray) -> None:
    """Set the x-axis and y-axis limits for a axis plot."""

    lvlmax = np.max(vec)
    ax.set_xlim(left=10, right=100000)
    ax.set_ylim(lvlmax - 90, lvlmax + 10)


def plot_irs(signal: ImpulseResponseSignal) -> None:
    """Plot IR signals for testing."""

    fig, ax = plt.subplots(nrows=3, ncols=2)
    sglvec = signal._refsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[0, 0].plot(tmevec, sglvec)
    ax[0, 0].set_xlim(left=0, right=sgldur)

    sglvec = signal._recsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[1, 0].plot(tmevec, sglvec)
    ax[1, 0].set_xlim(left=0, right=sgldur)

    sglvec = signal.irssglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[2, 0].plot(tmevec, sglvec)
    ax[2, 0].set_xlim(left=0, right=sgldur)
    ax[2, 0].set_ylim(bottom=-1, top=1)

    sglspc = np.abs(signal._refspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[0, 1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[0, 1], sgllvlspc)

    sglspc = np.abs(signal._recspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1, 1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[1, 1], sgllvlspc)

    sglspc = np.abs(signal._irsspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[2, 1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[2, 1], sgllvlspc)

    plt.show()


def plot_irs_deconvolution(signal: ImpulseResponseSignal) -> None:
    """Plot IR signals for testing."""
    fig, ax = plt.subplots(nrows=1, ncols=2)
    sglvec = signal._refsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(left=0, right=sgldur)
    sglspc = np.abs(signal._refspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[1], sgllvlspc)

    fig, ax = plt.subplots(nrows=1, ncols=2)
    sglvec = signal._invrefvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(left=0, right=sgldur)

    sglspc = np.abs(signal._invrefspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[1], sgllvlspc)

    fig, ax = plt.subplots(nrows=1, ncols=2)
    sglvec = signal.irssglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(start=0, stop=sgldur, num=sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(left=0, right=sgldur)
    ax[0].set_ylim(bottom=-1, top=1)

    sglspc = np.abs(signal._irsspc)
    frqvec = np.linspace(start=1, stop=signal.smprte, num=sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    _set_ax_semilog_limits(ax[1], sgllvlspc)

    plt.show()
