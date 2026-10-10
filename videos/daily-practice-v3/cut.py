"""Rebuild the exact 785-frame speech recut from source.mp4."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
fps = 24000 / 1001
blocks = [(4, 142), (149, 186), (193, 277), (284, 810)]
parts = []
for i, (first, last) in enumerate(blocks):
    parts.extend([
        f'[0:v]trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS[v{i}]',
        f'[0:a]atrim=start={first / fps:.6f}:end={last / fps:.6f},asetpts=PTS-STARTPTS[a{i}]',
    ])
inputs = ''.join(f'[v{i}][a{i}]' for i in range(len(blocks)))
parts.append(f'{inputs}concat=n=4:v=1:a=1[v][a]')
parts.append('[v]scale=1080:1920:flags=lanczos,crop=1080:1920[vout]')
subprocess.run([
    'ffmpeg', '-y', '-i', str(root / 'source.mp4'), '-filter_complex', ';'.join(parts),
    '-map', '[vout]', '-map', '[a]', '-r', '24000/1001', '-frames:v', '785',
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-g', '48', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(root / 'cut.mp4')
], check=True)
