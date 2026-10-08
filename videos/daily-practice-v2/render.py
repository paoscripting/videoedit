"""Render graphics in HyperFrames and composite every subtitle reliably in FFmpeg."""
from pathlib import Path
import subprocess,shutil,os
p=Path(__file__).resolve().parent;os.chdir(p)
os.environ.setdefault('XDG_CACHE_HOME',str(p/'.cache'))
Path(os.environ['XDG_CACHE_HOME']).mkdir(parents=True,exist_ok=True)
subprocess.run(['python','build-captions.py'],check=True)
stage=p/'.render-stage';stage.mkdir(exist_ok=True)
shutil.copytree(p/'assets',stage/'assets',dirs_exist_ok=True)
source=stage/'source.mp4'
if not source.exists():
 try:os.link(p/'source.mp4',source)
 except OSError:shutil.copyfile(p/'source.mp4',source)
# Keep the editable preview complete; export captions through the ASS compositor.
html=(p/'index.html').read_text().replace('</head>','<style>.caption{opacity:0!important}</style></head>')
(stage/'index.html').write_text(html)
subprocess.run(['npx','--yes','hyperframes@0.8.141','render',str(stage),'--fps','24000/1001','--workers','2','--quality','high','--output',str(stage/'graphics.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-i',str(stage/'graphics.mp4'),'-vf','ass=captions.ass:fontsdir=assets','-c:v','libx264','-preset','medium','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(p/'output.mp4')],check=True)
print('Finished',p/'output.mp4')
