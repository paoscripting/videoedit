from pathlib import Path
import math
import struct
import wave

path = Path(__file__).resolve().parent / 'assets' / 'accents.wav'
rate = 48000
length = 32.741
samples = [0.0] * round(length * rate)
# Four cues are actually timed in the brief. Keep them barely audible under speech.
for when, frequency, duration, gain in [(8.11, 810, .055, .014), (16.34, 310, .18, .009),
                                       (20.68, 620, .06, .012), (27.90, 180, .13, .012)]:
    base = round(when * rate)
    for n in range(round(duration * rate)):
        t = n / rate
        attack = min(1.0, t / .004)
        envelope = attack * (1 - t / duration) ** 2
        samples[base + n] += math.sin(2 * math.pi * frequency * t) * gain * envelope
with wave.open(str(path), 'wb') as out:
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(rate)
    out.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, value)) * 32767)) for value in samples))
print(path)
