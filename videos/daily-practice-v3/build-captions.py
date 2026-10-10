from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
brief = (ROOT / 'brief.md').read_text()
section = brief.split('Use the exact subtitle text below', 1)[1].split('Keep dialogue clear', 1)[0]
rows = []
for line in section.splitlines():
    m = re.match(r'^\|\s*([\d.]+)–([\d.]+)\s*\|\s*([\d.]+)–([\d.]+)\s*\|\s*([^|]+?)\s*\|$', line)
    if m:
        source_start, source_end, start, end = map(float, m.group(1, 2, 3, 4))
        rows.append(dict(source_start=source_start, source_end=source_end, start=start, end=end, text=m.group(5).strip()))
assert len(rows) == 35, len(rows)
# The source audio says "new habit formation"; retain the spoken word.
for row in rows:
    if row['text'] == 'to habit formation':
        row['text'] = 'to new habit formation'

(ROOT / 'captions.json').write_text(json.dumps(rows, indent=2) + '\n')
(ROOT / 'captions.js').write_text('window.CAPTIONS = ' + json.dumps(rows) + ';\n')

def ass_time(value):
    centis = round(value * 100)
    return f'{centis // 360000}:{centis // 6000 % 60:02}:{centis // 100 % 60:02}.{centis % 100:02}'

def srt_time(value):
    millis = round(value * 1000)
    return f'{millis // 3600000:02}:{millis // 60000 % 60:02}:{millis // 1000 % 60:02},{millis % 1000:03}'

head = '''[Script Info]
Title: Daily Practice Editorial V3
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,OpenAI Sans,64,&H00E8F0F4,&H00E8F0F4,&H771C1716,&HAA1C1716,0,0,0,0,100,100,-1,0,1,2,1,5,90,130,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
lines = []
for i, row in enumerate(rows):
    text = row['text']
    start, end = row['start'], row['end']
    y = 1100 if i in (0, 34) else 1390
    x = 480
    size = 56 if len(text) > 22 else 64
    fade = 70 if end - start < .6 else 120
    parts = []
    emphasis = {'hardwired': 8.11, 'fire': 11.38, 'wire': 12.12,
                'hell': 12.93, 'mean': 13.45, 'stronger': 27.90,
                'time': 32.18}
    for word in text.split():
        if word in emphasis and start <= emphasis[word] < end:
            delay = round((emphasis[word] - start) * 1000)
            parts.append(r'{\t(' + str(delay) + ',' + str(delay + 100) + r',\1c&H8AEBDD&)}' +
                         (r'{\fnInstrument Serif\fs80}' if word in ('hardwired', 'stronger', 'time') else '') +
                         word + r'{\fnOpenAI Sans\fs' + str(size) + r'\1c&HE8F0F4&}')
        else:
            parts.append(word)
    if i == 0:
        # Hero words form one phrase; the numeral lands at its spoken cue.
        caption = r'these {\fnInstrument Serif\fs140\t(150,240,\1c&H8AEBDD&)}30{\fnOpenAI Sans\fs64\1c&HE8F0F4&} minutes'
    elif i == 34:
        caption = r'putting the {\fnInstrument Serif\t(360,470,\fs96\1c&H8AEBDD&)}time in'
    else:
        caption = ' '.join(parts)
    event = r'{\an5\fs' + str(size) + rf'\move({x},{y + 14},{x},{y},0,140)\fad({fade},40)' + r'}' + caption
    lines.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Caption,,0,0,0,,{event}')
(ROOT / 'captions.ass').write_text(head + '\n'.join(lines) + '\n')
(ROOT / 'captions.srt').write_text('\n\n'.join(
    f"{i + 1}\n{srt_time(r['start'])} --> {srt_time(r['end'])}\n{r['text']}" for i, r in enumerate(rows)) + '\n')
print(f'Built {len(rows)} phrases')
