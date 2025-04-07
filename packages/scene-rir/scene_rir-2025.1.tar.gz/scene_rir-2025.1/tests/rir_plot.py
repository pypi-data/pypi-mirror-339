import numpy as np
from matplotlib import pyplot as plt


def set_ax_semilog_limits(ax, vec):
    """Set the x-axis and y-axis limits for a axis plot."""

    lvlmax = np.max(vec)
    ax.set_xlim(10, 100000)
    ax.set_ylim(lvlmax - 90, lvlmax + 10)


def plot_irs(signal):
    """Plot IR signals for testing."""

    fig, ax = plt.subplots(3, 2)

    sglvec = signal._refsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[0, 0].plot(tmevec, sglvec)
    ax[0, 0].set_xlim(0, sgldur)
    # ax[0, 0].set_ylim(-1, 1)

    sglvec = signal._recsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[1, 0].plot(tmevec, sglvec)
    ax[1, 0].set_xlim(0, sgldur)
    # ax[1, 0].set_ylim(-1, 1)

    sglvec = signal.irssglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[2, 0].plot(tmevec, sglvec)
    ax[2, 0].set_xlim(0, sgldur)
    ax[2, 0].set_ylim(-1, 1)

    sglspc = np.abs(signal._refspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[0, 1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[0, 1], sgllvlspc)

    sglspc = np.abs(signal._recspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1, 1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[1, 1], sgllvlspc)

    sglspc = np.abs(signal._irsspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[2, 1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[2, 1], sgllvlspc)

    plt.show()


def plot_irs_deconvolution(signal):
    """Plot IR signals for testing."""
    fig, ax = plt.subplots(1, 2)
    sglvec = signal._refsglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(0, sgldur)
    # ax[0].set_ylim(-1, 1)
    sglspc = np.abs(signal._refspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[1], sgllvlspc)

    fig, ax = plt.subplots(1, 2)
    sglvec = signal._invrefvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(0, sgldur)

    sglspc = np.abs(signal._invrefspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[1], sgllvlspc)

    fig, ax = plt.subplots(1, 2)
    sglvec = signal.irssglvec
    sglsze = sglvec.size
    sgldur = sglsze / signal.smprte
    tmevec = np.linspace(0, sgldur, sglsze)
    ax[0].plot(tmevec, sglvec)
    ax[0].set_xlim(0, sgldur)
    ax[0].set_ylim(-1, 1)

    sglspc = np.abs(signal._irsspc)
    frqvec = np.linspace(1, signal.smprte, sglspc.size)
    frqvec = frqvec[: int(frqvec.size / 2)]
    sgllvlspc = 10 * np.log10(sglspc[: int(sglspc.size / 2)] ** 2)
    ax[1].semilogx(frqvec, sgllvlspc)
    set_ax_semilog_limits(ax[1], sgllvlspc)

    plt.show()
