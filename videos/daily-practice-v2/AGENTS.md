# Editing this film
Read DESIGN.md and captions.json before changing index.html.
The supplied references define typography and editorial pacing, not the subject matter. Never insert their promotional words, logos, or footage into this film.

Preserve the source voice, every spoken word, the source aspect ratio and the original camera cuts. Phrase captions contain 2–5 words, without punctuation. Supporting diagram text must be justified by the transcript. Emphasis words should reveal at their own word timestamps.

Reserve strong visual treatments for the hook, the fire/wire explanation, and the strengthening takeaway. Use two font families and one acid-yellow accent. Alternate these designed stages with quieter speaker sections. Avoid using the same small caption bar as the entire edit.

Protect padded head bounds across all shots and gestures. Keep diagram stages outside the displayed source frame. On full-bleed footage keep captions at the recorded shot-specific positions. Inspect transitions as well as settled frames.

Use one seekable paused GSAP timeline. Set initial opacity explicitly for later elements; never let an unrevealed future word appear through its CSS default. Animate signal dots along the drawn curve, rather than across a straight line beneath it.

Run the full HyperFrames check. Review actual output at phone size throughout the clip, verify all words and audio continuity, and check the opening, both original cuts, graphic entrances and final frame. Render with the original 24000/1001 frame rate. Deliver the MP4 and editable source, retaining the earlier version.

Delivery uses the two-stage render.py pipeline: HyperFrames graphics, then FFmpeg ASS captions. Keep HTML preview captions as ordinary GSAP layers; use the ASS layer for delivery. Regenerate captions.ass and captions.srt from captions.json after changes. Check all 36 phrases in the actual encoded output: framework checks do not guarantee that captions are visible.

Keep hook, quote, network, strength and caption layers as direct children of the composition root. Validate that structure in a browser after markup edits. Avoid unscoped string replacements of closing tags.
