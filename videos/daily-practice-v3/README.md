# Daily Practice editorial V3

This version follows `brief.md`: four retained source blocks, 785 frames at 24000/1001 fps, 1080 × 1920, 35 short subtitle phrases, restrained punch ins, and a recurring two-neuron connection graphic. The speaker's original voice and camera angles remain.

## Editable project

The editable ZIP includes `source.mp4`. Run `python cut.py` to create `cut.mp4` from the source, then run `python render.py` to rebuild graphics and the captioned MP4. The render requires Python 3, FFmpeg, Node, Chromium, and `hyperframes@0.8.141` (fetched automatically through npx). `render.py` sets writable cache paths and uses `/usr/bin/chromium` by default.

Edit `index.html` for graphics, layout and animation; `brief.md` for the supplied direction; `build-captions.py` and `captions.json` for captions; `make-accents.py` for four quiet sound cues; and `cut.py` for source in and out points. `captions.ass` is used for final export; `captions.srt` is supplied separately.

The source transcript includes “new” in “to new habit formation”; the supplied brief omits it. The subtitle keeps the spoken word. The brief mentions five sound effects, while its schedule places four. This project uses the four scheduled cues.
