"""Repeatable HyperFrames graphics render with reliable ASS captions."""
from pathlib import Path
import os
import shutil
import subprocess

project = Path(__file__).resolve().parent
os.chdir(project)
os.environ['XDG_CACHE_HOME'] = str(project / '.cache')
os.environ.setdefault('npm_config_cache', '/workspace/.npm-cache')
os.environ.setdefault('HYPERFRAMES_BROWSER_PATH', '/usr/bin/chromium')
Path(os.environ['XDG_CACHE_HOME']).mkdir(exist_ok=True)
subprocess.run(['python', 'build-captions.py'], check=True)
subprocess.run(['python', 'make-accents.py'], check=True)
stage = project / '.render-stage'
stage.mkdir(exist_ok=True)
shutil.copytree(project / 'assets', stage / 'assets', dirs_exist_ok=True)
for name in ['cut.mp4', 'captions.js']:
    target = stage / name
    target.unlink(missing_ok=True)
    try:
        os.link(project / name, target)
    except OSError:
        shutil.copyfile(project / name, target)
(stage / 'index.html').write_text((project / 'index.html').read_text().replace('</style>', '.caption{opacity:0!important}</style>'))
subprocess.run(['npx', '--yes', 'hyperframes@0.8.141', 'render', str(stage), '--fps', '24000/1001',
                '--workers', '2', '--quality', 'high', '--output', str(stage / 'graphics.mp4')], check=True)
subprocess.run(['ffmpeg', '-y', '-i', str(stage / 'graphics.mp4'), '-vf', 'ass=captions.ass:fontsdir=assets',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-threads', '4', '-pix_fmt', 'yuv420p',
                '-c:a', 'copy', '-movflags', '+faststart', str(project / 'output.mp4')], check=True)
print('Finished', project / 'output.mp4')
