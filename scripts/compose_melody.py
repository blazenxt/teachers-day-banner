#!/usr/bin/env python3
"""
Original Teacher's Day celebration melody — composed for this project.
Warm, respectful, uplifting. NOT based on any existing copyrighted song.
Synthesized with additive 'piano-ish' tones + soft pad + gentle percussion.
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

import numpy as np

SR = 44100
MASTER = 0.72

# Equal temperament, A4 = 440
NOTE = {
    "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.00, "A3": 220.00, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00,
    "REST": 0.0,
}

# Original theme in C major — gentle, grateful, ceremonial (not any known song)
# Format: (note_name, beats)
# 4/4, tempo ~76 BPM — slow ceremonial feel
BPM = 76.0
BEAT = 60.0 / BPM

# Main melody — original phrase A
MELODY_A = [
    ("E4", 1.0), ("G4", 1.0), ("A4", 1.5), ("G4", 0.5),
    ("E4", 1.0), ("D4", 1.0), ("C4", 2.0),
    ("D4", 1.0), ("E4", 1.0), ("G4", 1.5), ("A4", 0.5),
    ("G4", 1.0), ("E4", 1.0), ("D4", 2.0),
]

# Phrase B — lift
MELODY_B = [
    ("A4", 1.0), ("C5", 1.0), ("B4", 1.0), ("A4", 1.0),
    ("G4", 1.0), ("E4", 1.0), ("G4", 2.0),
    ("A4", 1.0), ("G4", 0.5), ("E4", 0.5), ("D4", 1.0), ("C4", 1.0),
    ("D4", 1.0), ("E4", 1.0), ("C4", 2.0),
]

# Soft closing / resolve
MELODY_C = [
    ("E4", 1.0), ("G4", 1.0), ("A4", 2.0),
    ("G4", 1.0), ("E4", 1.0), ("D4", 1.0), ("C4", 1.0),
    ("D4", 2.0), ("E4", 2.0),
    ("C4", 4.0),
]

# Simple chord pads under melody (root, third, fifth) as note names lasting full bars
# Each entry: list of notes, duration in beats
PADS = [
    (["C3", "E3", "G3", "C4"], 4.0),
    (["A3", "C4", "E4"], 4.0),
    (["F3", "A3", "C4"], 4.0),
    (["G3", "B3", "D4"], 4.0),
    (["C3", "E3", "G3", "C4"], 4.0),
    (["A3", "C4", "E4"], 4.0),
    (["F3", "A3", "C4"], 4.0),
    (["G3", "B3", "D4", "G4"], 4.0),
    (["C3", "E3", "G3"], 4.0),
    (["F3", "A3", "C4"], 4.0),
    (["G3", "B3", "D4"], 4.0),
    (["C3", "E3", "G3", "C4"], 4.0),
]


def env_adsr(n: int, sr: int, a=0.02, d=0.12, s=0.65, r=0.35, peak=1.0) -> np.ndarray:
    """ADSR envelope, durations in seconds."""
    ea, ed, er = int(a * sr), int(d * sr), int(r * sr)
    es = max(0, n - ea - ed - er)
    parts = []
    if ea > 0:
        parts.append(np.linspace(0.0, peak, ea, endpoint=False))
    if ed > 0:
        parts.append(np.linspace(peak, peak * s, ed, endpoint=False))
    if es > 0:
        parts.append(np.full(es, peak * s))
    if er > 0:
        last = parts[-1][-1] if parts else peak * s
        parts.append(np.linspace(last, 0.0, er, endpoint=True))
    env = np.concatenate(parts) if parts else np.zeros(n)
    if len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    return env[:n]


def tone_piano(freq: float, dur: float, sr: int = SR, vel: float = 0.85) -> np.ndarray:
    """Additive partials approximating a soft upright piano."""
    n = int(dur * sr)
    if freq <= 0 or n <= 0:
        return np.zeros(max(n, 1), dtype=np.float64)
    t = np.arange(n) / sr
    # Inharmonic-ish partials with decaying weights
    partials = [
        (1.0, 1.00, 0.02, 0.18, 0.55, 0.55),
        (2.0, 0.42, 0.01, 0.12, 0.40, 0.45),
        (3.0, 0.18, 0.01, 0.10, 0.30, 0.40),
        (4.0, 0.10, 0.01, 0.08, 0.22, 0.35),
        (5.0, 0.05, 0.01, 0.06, 0.15, 0.30),
        (6.0, 0.03, 0.01, 0.05, 0.10, 0.25),
    ]
    sig = np.zeros(n, dtype=np.float64)
    for mul, amp, a, d, s, r in partials:
        f = freq * mul
        # slight stretch
        if mul > 1:
            f *= 1.0 + 0.0006 * (mul - 1)
        wave_ = np.sin(2 * math.pi * f * t)
        # soft detune twin for warmth
        wave_ += 0.22 * np.sin(2 * math.pi * (f * 1.002) * t + 0.3)
        e = env_adsr(n, sr, a=a, d=d, s=s, r=min(r, dur * 0.45), peak=amp * vel)
        sig += wave_ * e
    # gentle low-pass-ish by mixing previous sample
    out = np.zeros_like(sig)
    prev = 0.0
    for i, x in enumerate(sig):
        prev = 0.72 * prev + 0.28 * x
        out[i] = prev
    return out


def tone_pad(freq: float, dur: float, sr: int = SR, vel: float = 0.25) -> np.ndarray:
    n = int(dur * sr)
    if freq <= 0 or n <= 0:
        return np.zeros(max(n, 1), dtype=np.float64)
    t = np.arange(n) / sr
    sig = (
        0.55 * np.sin(2 * math.pi * freq * t)
        + 0.28 * np.sin(2 * math.pi * freq * 2.0 * t)
        + 0.12 * np.sin(2 * math.pi * freq * 3.0 * t + 0.4)
        + 0.08 * np.sin(2 * math.pi * freq * 0.5 * t)
    )
    # slow tremolo
    trem = 1.0 + 0.04 * np.sin(2 * math.pi * 2.2 * t)
    e = env_adsr(n, sr, a=0.45, d=0.3, s=0.75, r=min(1.2, dur * 0.35), peak=vel)
    return sig * trem * e


def soft_chime(freq: float, dur: float = 1.2, sr: int = SR) -> np.ndarray:
    n = int(dur * sr)
    t = np.arange(n) / sr
    sig = (
        np.sin(2 * math.pi * freq * t)
        + 0.35 * np.sin(2 * math.pi * freq * 2.76 * t)
        + 0.15 * np.sin(2 * math.pi * freq * 5.4 * t)
    )
    e = np.exp(-2.8 * t) * env_adsr(n, sr, a=0.005, d=0.05, s=0.4, r=0.9, peak=0.35)
    return sig * e


def place(buf: np.ndarray, sig: np.ndarray, start: int) -> None:
    end = min(len(buf), start + len(sig))
    if start >= len(buf) or end <= start:
        return
    buf[start:end] += sig[: end - start]


def render_melody(events, start_beat: float = 0.0) -> tuple[np.ndarray, float]:
    total_beats = start_beat + sum(b for _, b in events)
    # tail for release
    total_sec = total_beats * BEAT + 2.5
    buf = np.zeros(int(total_sec * SR), dtype=np.float64)
    t_beat = start_beat
    for name, beats in events:
        freq = NOTE[name]
        dur = beats * BEAT * 0.96  # slight gap for articulation
        vel = 0.78 if beats >= 1.0 else 0.68
        if name != "REST":
            sig = tone_piano(freq, max(dur, 0.08), vel=vel)
            place(buf, sig, int(t_beat * BEAT * SR))
        t_beat += beats
    return buf, total_beats


def render_pads(pads, start_beat: float = 0.0) -> np.ndarray:
    total_beats = start_beat + sum(d for _, d in pads)
    total_sec = total_beats * BEAT + 3.0
    buf = np.zeros(int(total_sec * SR), dtype=np.float64)
    t_beat = start_beat
    for notes, beats in pads:
        dur = beats * BEAT
        chord = np.zeros(int(dur * SR) + int(1.5 * SR), dtype=np.float64)
        for nm in notes:
            place(chord, tone_pad(NOTE[nm], dur + 1.2, vel=0.16 / max(1, len(notes) - 1)), 0)
        place(buf, chord, int(t_beat * BEAT * SR))
        t_beat += beats
    return buf


def soft_noise_whoosh(dur: float = 0.35) -> np.ndarray:
    n = int(dur * SR)
    noise = np.random.randn(n) * 0.04
    e = env_adsr(n, SR, a=0.05, d=0.1, s=0.3, r=0.2, peak=1.0)
    # simple lowpass
    out = np.zeros(n)
    prev = 0.0
    for i, x in enumerate(noise * e):
        prev = 0.9 * prev + 0.1 * x
        out[i] = prev
    return out


def compose() -> np.ndarray:
    # Structure: intro chime → A → B → A → C → outro
    # Build melody timeline
    events = []
    events += [("REST", 2.0)]  # breath in
    events += MELODY_A
    events += MELODY_B
    events += MELODY_A
    events += MELODY_C
    events += [("REST", 1.0)]

    mel, total_beats = render_melody(events, 0.0)

    # Pads aligned to 4-beat bars covering the piece
    pad_buf = render_pads(PADS, 2.0)  # start after intro rest

    n = max(len(mel), len(pad_buf)) + int(2.0 * SR)
    mix = np.zeros(n, dtype=np.float64)
    place(mix, pad_buf * 0.85, 0)
    place(mix, mel * 1.0, 0)

    # Opening + closing chimes (original motif: C5-E5-G5)
    place(mix, soft_chime(NOTE["C5"], 1.6) * 0.55, int(0.15 * SR))
    place(mix, soft_chime(NOTE["E5"], 1.6) * 0.45, int(0.45 * SR))
    place(mix, soft_chime(NOTE["G5"], 2.0) * 0.40, int(0.75 * SR))

    # Soft whoosh at start
    place(mix, soft_noise_whoosh(0.5), int(0.05 * SR))

    # Gentle pulse every bar (very soft low heartbeat-like piano thump on C2-ish)
    bars = int(total_beats // 4) + 1
    for b in range(bars):
        t0 = (2.0 + b * 4.0) * BEAT  # after intro
        if t0 * SR >= len(mix):
            break
        thump = tone_piano(NOTE["C3"], 0.35, vel=0.25)
        place(mix, thump * 0.22, int(t0 * SR))

    # Ending chime resolve
    end_t = (total_beats - 3.0) * BEAT
    place(mix, soft_chime(NOTE["C5"], 2.5) * 0.5, int(end_t * SR))
    place(mix, soft_chime(NOTE["G4"], 2.8) * 0.35, int((end_t + 0.25) * SR))
    place(mix, soft_chime(NOTE["E4"], 3.0) * 0.30, int((end_t + 0.5) * SR))
    place(mix, soft_chime(NOTE["C4"], 3.5) * 0.40, int((end_t + 0.85) * SR))

    # Fade in / out
    fade_in = int(1.2 * SR)
    fade_out = int(3.5 * SR)
    if fade_in > 0:
        mix[:fade_in] *= np.linspace(0, 1, fade_in)
    if fade_out > 0 and fade_out < len(mix):
        mix[-fade_out:] *= np.linspace(1, 0, fade_out)

    # Soft limiter / normalize
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * MASTER

    # Light stereo-ish widening later: mono for max compatibility
    return mix


def write_wav(path: Path, mono: np.ndarray, sr: int = SR) -> None:
    # Convert to 16-bit stereo (duplicate channels)
    mono = np.clip(mono, -1.0, 1.0)
    pcm = (mono * 32767.0).astype(np.int16)
    stereo = np.empty(pcm.size * 2, dtype=np.int16)
    stereo[0::2] = pcm
    stereo[1::2] = pcm
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(stereo.tobytes())


def wav_to_mp3_ffmpeg(wav_path: Path, mp3_path: Path) -> bool:
    import shutil
    import subprocess
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False
    r = subprocess.run(
        [ffmpeg, "-y", "-i", str(wav_path), "-codec:a", "libmp3lame", "-qscale:a", "3", str(mp3_path)],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0 and mp3_path.exists()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    audio_dir = root / "assets" / "audio"
    wav_path = audio_dir / "teachers-day-song.wav"
    mp3_path = audio_dir / "teachers-day-song.mp3"

    print("Composing original Teacher's Day melody…")
    audio = compose()
    dur = len(audio) / SR
    print(f"Duration: {dur:.1f}s")
    write_wav(wav_path, audio)
    print(f"Wrote {wav_path}")

    if wav_to_mp3_ffmpeg(wav_path, mp3_path):
        print(f"Wrote {mp3_path}")
        # keep wav as fallback too; html can prefer mp3
    else:
        # Fallback: ship wav and also try lame-less re-encode via pure python? keep wav
        # Replace mp3 reference by writing a small note — we'll point html to wav if needed
        print("ffmpeg not found — keeping WAV. Will update HTML to use wav if mp3 missing.")
        if mp3_path.exists():
            mp3_path.unlink()


if __name__ == "__main__":
    main()
