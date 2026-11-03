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


# ---------------------------------------------------------------------------------------------------------------------
# Event-driven score: dry percussive hits locked to on-screen strikes, a low drone that is cut dead, silence, one soft bell.
# Used by art-directed reels whose picture is a pure function of the same event list (see build_samples.py).
# ---------------------------------------------------------------------------------------------------------------------
def _reverb_ir(rng, length_s, decay_s):
    n = int(length_s * SR)
    tt = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-tt / decay_s)
    ir[0] = 0
    return ir / np.abs(ir).max()


def _sweep_noise(rng, n, a0, a1):
    """White noise through a one-pole low-pass whose coefficient glides a0 -> a1 (a 'swoosh' that brightens)."""
    x = rng.normal(0, 1, n)
    y = np.empty(n)
    acc = 0.0
    alphas = np.linspace(a0, a1, n)
    for i in range(n):
        acc += alphas[i] * (x[i] - acc)
        y[i] = acc
    return y - _lowpass(y, 400)  # drop the rumble


def strike_score(duration, out_wav, hits, swooshes=(), drone=None, bell=None, blow=None, seed=0):
    """hits: [{'t', 'amp', 'f0'}] seconds / 0-1 / Hz. swooshes: [(t0, t1)] noise sweeps that end on a hit.
    drone: {'hz', 'until'} low sine that stops abruptly at 'until'. bell: {'t', 'hz', 'amp'}. blow: (t0, t1) air burst."""
    from scipy.signal import fftconvolve
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    dry = np.zeros(n)
    wet = np.zeros(n)

    def add(buf, i, seg):
        j = min(n, i + len(seg))
        if j > i:
            buf[i:j] += seg[: j - i]

    for k, h in enumerate(hits):
        i = int(h["t"] * SR)
        L = int(0.32 * SR)
        tt = np.arange(L) / SR
        f0 = h.get("f0", 110.0)
        freq = f0 * 0.5 + f0 * 1.6 * np.exp(-tt * 38)
        body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt * 20)
        click = rng.normal(0, 1, L) * np.exp(-tt * 1100)
        slap = _lowpass(rng.normal(0, 1, L), 3) * np.exp(-tt * 70)
        slap = slap - _lowpass(slap, 40)
        seg = h["amp"] * (0.95 * body + 0.38 * click + 0.55 * slap)
        add(dry, i, seg)
        add(wet, i, seg * 0.8)
    for (t0, t1) in swooshes:
        i0, i1 = int(t0 * SR), int(t1 * SR)
        m = i1 - i0
        s = _sweep_noise(rng, m, 0.03, 0.55)
        env = np.linspace(0, 1, m) ** 1.8
        seg = 0.20 * s * env / max(1e-9, np.abs(s).max())
        add(dry, i0, seg)
    if blow:
        i0, i1 = int(blow[0] * SR), int(blow[1] * SR)
        m = i1 - i0
        s = _sweep_noise(rng, m, 0.5, 0.02)
        env = np.sin(np.linspace(0, np.pi, m)) ** 1.5
        add(dry, i0, 0.30 * s * env / max(1e-9, np.abs(s).max()))
    if drone:
        t = np.arange(n) / SR
        until = drone["until"]
        hz = drone["hz"] * (1 + 0.06 * np.clip(t / until, 0, 1))
        ph = 2 * np.pi * np.cumsum(hz) / SR
        d = 0.6 * np.sin(ph) + 0.25 * np.sin(2 * ph + 0.3) + 0.12 * np.sin(3 * ph + 1.1)
        env = np.clip(t / 0.6, 0, 1) * (0.35 + 0.65 * np.clip(t / until, 0, 1))
        cut = np.clip((until - t) / 0.02, 0, 1)  # dead stop, 20 ms
        add(dry, 0, 0.30 * d * env * cut)
    if bell:
        i = int(bell["t"] * SR)
        L = int(4.0 * SR)
        tt = np.arange(L) / SR
        seg = np.zeros(L)
        for ratio, amp, dec in ((1, 1.0, 2.8), (2.01, 0.42, 2.2), (2.76, 0.28, 1.6), (4.07, 0.14, 1.0), (5.4, 0.09, 0.6)):
            seg += amp * np.sin(2 * np.pi * bell["hz"] * ratio * tt) * np.exp(-tt / dec)
        seg += 0.4 * np.sin(2 * np.pi * bell["hz"] / 2 * tt) * np.exp(-tt / 3.0)
        seg *= np.clip(tt / 0.004, 0, 1) * bell.get("amp", 0.35)
        add(dry, i, seg)
        add(wet, i, seg * 0.6)
    ir = _reverb_ir(rng, 1.4, 0.35)
    tail = fftconvolve(wet, ir)[:n]
    mono = dry + 0.16 * tail
    left = mono.copy()
    right = np.concatenate([np.zeros(int(0.009 * SR)), mono[:-int(0.009 * SR)]])
    stereo = np.stack([left, right], axis=1)
    fade_out = np.clip((duration - np.arange(n) / SR) / 0.25, 0, 1)
    stereo *= fade_out[:, None]
    stereo = stereo / max(1e-9, np.abs(stereo).max()) * 0.9
    pcm = (stereo * 32767).astype("<i2")
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    return str(out_wav)
