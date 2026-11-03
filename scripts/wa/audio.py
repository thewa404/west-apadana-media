"""Synthesize an original ambient/cinematic score with numpy (no samples, no licensing issues)."""
import wave

import numpy as np

SR = 44100


def _lowpass(x, k):
    kernel = np.ones(k) / k
    return np.convolve(x, kernel, mode="same")


def synth(duration, out_wav, root_hz=73.42, bpm=56, seed=0, hit_at=None):
    """Drone + slow pad + soft pulse + riser into a final low hit.

    root_hz   : fundamental (73.42 = D2, 65.41 = C2, 82.41 = E2 ...). Vary per batch.
    bpm       : pulse rate. hit_at: second of the final hit (default duration - 1.6).
    """
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    t = np.arange(n) / SR
    hit_at = duration - 1.6 if hit_at is None else hit_at

    drone = (0.55 * np.sin(2 * np.pi * root_hz * t)
             + 0.28 * np.sin(2 * np.pi * root_hz * 1.5 * t + 0.4)
             + 0.17 * np.sin(2 * np.pi * root_hz * 2 * t + 1.1))
    drone *= 0.65 + 0.35 * np.sin(2 * np.pi * 0.06 * t)

    pad = np.zeros(n)
    for ratio in (2.0, 2.378, 3.0, 3.564):  # root, minor third, fifth, minor seventh (equal temperament)
        for det in (-0.7, 0.7):
            pad += np.sin(2 * np.pi * (root_hz * ratio + det) * t + rng.uniform(0, 6.28))
    pad *= 0.045 * (1 - np.exp(-t / 3.0))

    pulse = np.zeros(n)
    beat = 60.0 / bpm
    for bt in np.arange(0.6, max(hit_at - 0.5, 0.7), beat):
        i = int(bt * SR)
        length = min(int(0.4 * SR), n - i)
        if length <= 0:
            break
        tt = np.arange(length) / SR
        freq = 46 + 70 * np.exp(-tt * 28)
        pulse[i:i + length] += 0.55 * np.exp(-tt * 8) * np.sin(2 * np.pi * np.cumsum(freq) / SR)

    riser = np.zeros(n)
    r0, r1 = max(0, int((hit_at - 2.6) * SR)), int(hit_at * SR)
    if r1 > r0:
        seg = _lowpass(rng.normal(0, 1, r1 - r0), 12)
        ramp = np.linspace(0, 1, r1 - r0) ** 2.2
        riser[r0:r1] = 0.22 * seg * ramp

    boom = np.zeros(n)
    b0 = int(hit_at * SR)
    if b0 < n:
        length = n - b0
        tt = np.arange(length) / SR
        freq = 38 + 120 * np.exp(-tt * 14)
        boom[b0:] = (0.9 * np.exp(-tt * 2.4) * np.sin(2 * np.pi * np.cumsum(freq) / SR)
                     + 0.15 * np.exp(-tt * 5) * _lowpass(rng.normal(0, 1, length), 6))

    mono = 0.55 * drone + pad + 0.6 * pulse + riser + boom
    fade_in = np.clip(t / 1.2, 0, 1)
    fade_out = np.clip((duration - t) / 0.9, 0, 1)
    mono *= fade_in * fade_out
    delay = int(0.012 * SR)
    left = mono
    right = np.concatenate([np.zeros(delay), mono[:-delay]])
    stereo = np.stack([left, right], axis=1)
    stereo = stereo / max(1e-9, np.abs(stereo).max()) * 0.85
    pcm = (stereo * 32767).astype("<i2")
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    return str(out_wav)
