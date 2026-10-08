# Daily Practice editorial V2
Reference-led typography and original neural diagrams, preserving the original continuous voice and all 122 words.

## Complete editable project
Download `renders/daily-practice-v2-editable.zip` from the repository and unzip it. The ZIP includes `source.mp4`; the GitHub source folder omits that footage file.

Run `python render.py` inside the unzipped directory. Requires Python 3, Node/npm, FFmpeg and Chromium. Set `HYPERFRAMES_BROWSER_PATH` to the Chromium executable when needed. The script renders graphics in HyperFrames 0.8.141, then composites every phrase with FFmpeg. Output: `output.mp4`, 1216×2160, 24000/1001 fps, original voice plus four quiet graphic accents.

## What to edit
- `index.html`: graphic layouts, original SVG drawings and deterministic GSAP animation. Its untimed caption elements provide an editable preview.
- `captions.json`: exact phrase and word timings, text and highlight choices.
- `build-captions.py`: subtitle appearance and timing; generates ASS and SRT.
- `render.py`: repeatable two-stage export, with an explicit ASS subtitle layer.
- `DESIGN.md` and `AGENTS.md`: reference-based visual direction and face/gesture protection rules.
- `assets/`: local fonts, GSAP and quiet sound accents.

Run the full framework check with `npx hyperframes@0.8.141 check .`. View the composition with HyperFrames preview; use `python render.py` for final delivery.

## Skills used
```sh
npx skills add heygen-com/hyperframes --full-depth --agent codex --skill hyperframes talking-head-recut hyperframes-animation hyperframes-core media-use --yes
```
`--full-depth` searches nested skill directories. It is a discovery option. The visual improvement comes from the reference study, custom layout, original diagrams and animation timing. No reference footage, logos or promotional copy is incorporated.
