from pathlib import Path
import json,re
p=Path(__file__).resolve().parent;cs=json.loads((p/'captions.json').read_text())
def tc(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
def srt(t):
 c=round(t*1000);return f'{c//3600000:02}:{c//60000%60:02}:{c//1000%60:02},{c%1000:03}'
header='''[Script Info]
Title: Daily Practice Editorial V2
ScriptType: v4.00+
PlayResX: 1216
PlayResY: 2160
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,OpenAI Sans,86,&H00ECF7FF,&H00ECF7FF,&HBB191717,&HDD191717,-1,0,0,0,100,100,0,0,1,2,0,5,80,160,0,1
Style: Backing,OpenAI Sans,20,&H00191717,&H00191717,&H00191717,&H00191717,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
lines=[]
for i,c in enumerate(cs):
 st=c['start'];end=c['end'];stack=st<5.95 or 11.94<=st<13.7 or 16.3<=st<22.6 or 26.44<=st<31.88
 y=1880 if stack else c['y'];size=86 if len(c['text'])<=25 else 76
 serif=c['text'] in ['neurons that fire together','wire together','it actually gets stronger','That wiring gets stronger','putting the time in']
 if serif:size=106 if len(c['text'])<=25 else 94
 prefix=r'\fnInstrument Serif\b0\i1' if serif else r'\fnOpenAI Sans\b1\i0'
 parts=[];hits=[j for j,w in enumerate(c['words']) if c['accent'] and w['text'].lower()==c['accent'].lower()];chosen=hits[-1] if hits else -1
 for j,w in enumerate(c['words']):
  text=w['text']
  if j==chosen:
   delay=max(0,round((w['start']-st)*1000));text=f'{{\\t({delay},{delay+1},\\1c&H6AF2E6&)}}'+text+'{\\1c&HECF7FF&}'
  parts.append(text)
 event=f'{{\\an5{prefix}\\fs{size}\\move(578,{y+22},578,{y},0,170)\\fad(90,40)}}'+' '.join(parts)
 width=min(1040,max(320,len(c['text'])*size*(.4 if serif else .51)+65));height=130 if serif else 122;x=578-width/2
 back=f'{{\\an7\\pos({x:.0f},{y-height/2:.0f})\\1c&H191717&\\alpha&H88&\\p1\\fad(90,40)}}m 0 0 l {width:.0f} 0 {width:.0f} {height} 0 {height}'
 lines.extend([f'Dialogue: 0,{tc(st)},{tc(end)},Backing,,0,0,0,,{back}',f'Dialogue: 1,{tc(st)},{tc(end)},Caption,,0,0,0,,{event}'])
(p/'captions.ass').write_text(header+'\n'.join(lines)+'\n');(p/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{srt(c['start'])} --> {srt(c['end'])}\n{c['text']}" for i,c in enumerate(cs))+'\n')
print('Built 36 reliably composited caption phrases')
