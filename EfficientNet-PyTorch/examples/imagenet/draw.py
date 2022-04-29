import numpy as np
import seaborn as sns
import librosa
import librosa.display
import warnings
from PIL import Image

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use("ggplot")


def create_mel_spectrogram(audio_file, endtime, **spec_params):
    sr, hop_length, n_fft, n_mels, fmin, fmax = [
        spec_params[k] for k in ["sr", "hop_length", "n_fft", "n_mels", "fmin", "fmax"]
    ]
    audio, _ = librosa.core.load(audio_file, sr=sr, mono=True)

    buffer = 5 * _
    _end = endtime * _
    block = audio[_end-buffer:_end]

    melspec = librosa.feature.melspectrogram(
        block,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        fmin=fmin,
        fmax=fmax,
        power=1,
    )
    return melspec


def pcen_bird(melspec, **spec_params):
    """
    parameters are taken from [1]:
        - [1] Lostanlen, et. al. Per-Channel Energy Normalization: Why and How. IEEE Signal Processing Letters, 26(1), 39-43.
    """
    sr, hop_length = [spec_params[k] for k in ["sr", "hop_length"]]
    return librosa.pcen(
        melspec * (2 ** 31),
        time_constant=0.06,
        eps=1e-6,
        gain=0.8,
        power=0.25,
        bias=10,
        sr=sr,
        hop_length=hop_length,
    )


def mel2audio(melspec, **spec_params):
    n_fft, sr, hop_length = [spec_params[k] for k in ["n_fft", "sr", "hop_length"]]
    return librosa.feature.inverse.mel_to_audio(
        melspec, sr=sr, n_fft=n_fft, hop_length=hop_length, power=1
    )


def plot_spectrograms(
    audio_file,
    endtime,
    spec_params=dict(sr=32_000, hop_length=320, n_fft=800, n_mels=128, fmin=950, fmax=12_000)
    ):

    sr, hop_length, fmin, fmax, n_mels = [
        spec_params[k] for k in ["sr", "hop_length", "fmin", "fmax", "n_mels"]
    ]

    melspec = create_mel_spectrogram(audio_file, endtime, **spec_params)
    pcen_melspec = pcen_bird(melspec, **spec_params)

    img_pcen = librosa.display.specshow(
        pcen_melspec,
        sr=sr,
        hop_length=hop_length,
        fmin=fmin,
        fmax=fmax
    )

    img_pcen = img_pcen.get_array()

    img_pcen = img_pcen.reshape((n_mels, -1))
    corr_pcen = np.corrcoef(img_pcen)
    assert corr_pcen.shape == (n_mels, n_mels)

    # plot
    fig = plt.figure(figsize=(3, 3))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    sns.heatmap(corr_pcen, ax=ax, xticklabels=False, yticklabels=False, cbar=False)

    # plt.savefig(path)
    img = fig2img(fig)
    fig.clf()
    plt.clf()
    plt.close('all')

    return img


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    return img






