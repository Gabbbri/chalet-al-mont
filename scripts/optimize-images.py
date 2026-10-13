"""Encode responsive WebP assets; preserve high-resolution sources outside dist."""
from pathlib import Path
from PIL import Image, ImageOps
import re,json,shutil
root=Path(__file__).resolve().parents[1]
page=root/'docs/index.html'
html=page.read_text()
files=sorted(set(re.findall(r'(?:src|href)="/assets/([^"<>]+\.(?:png|jpg|jpeg))"',html)))
if not any(file!='logo-originale.png' for file in files):
 print('Images already encoded; no source references to replace.')
 raise SystemExit(0)
variants={}; before=0; after=0
source=root/'source-assets';source.mkdir(exist_ok=True)
for file in files:
 if file=='logo-originale.png':continue
 old=root/'docs/assets'/file
 backup=source/file
 if old.exists():shutil.copyfile(old,backup)
 with Image.open(backup) as raw:
  im=ImageOps.exif_transpose(raw).convert('RGB')
  width,height=im.size;before+=backup.stat().st_size
  sizes=sorted(set(min(width,w) for w in [240,480,960,1600]+([1920] if file=='chalet.jpg.png' else [])))
  entries=[]
  for w in sizes:
   h=round(height*w/width)
   dest=root/'docs/assets'/f'{Path(file).stem}-{w}.webp'
   im.resize((w,h),Image.Resampling.LANCZOS).save(dest,'WEBP',quality=82 if w>=480 else 76,method=6)
   entries.append({'src':'/assets/'+dest.name,'width':w,'height':h,'bytes':dest.stat().st_size})
   after+=dest.stat().st_size
  variants[file]=entries
# Replace image tags according to the actual rendered context.
for file,entries in variants.items():
 full=entries[-1]['src']
 html=html.replace(f'href="/assets/{file}"',f'href="{full}"')
 pattern=r'<img\b[^>]*src="/assets/'+re.escape(file)+r'"[^>]*>'
 def tag(match):
  original=match[0]
  pos=match.start()
  is_thumb=html.rfind('<button',0,pos)>html.rfind('</button>',0,pos)
  is_logo=False
  if is_thumb:
   entry=entries[0];replacement=f'src="{entry["src"]}" width="{entry["width"]}" height="{entry["height"]}" decoding="async"'
  else:
   choices=[e for e in entries if e['width']>=min(480,entries[-1]['width'])]
   default=min(choices,key=lambda e:abs(e['width']-960))
   hero='class="hero-img"' in original
   if hero:default=choices[-1]
   host=file=='famiglia-originale.jpg'
   sizes='100vw' if hero else '(max-width: 650px) 90vw, 300px' if host else '(max-width: 650px) 90vw, (max-width: 950px) 30vw, 30vw'
   if file=='radura.png':sizes='(max-width: 950px) 90vw, 46vw'
   srcset=', '.join(f'{e["src"]} {e["width"]}w' for e in choices)
   replacement=f'src="{default["src"]}" srcset="{srcset}" sizes="{sizes}" width="{default["width"]}" height="{default["height"]}" decoding="async"'
  return original.replace(f'src="/assets/{file}"',replacement)
 html=re.sub(pattern,tag,html)
# Put hidden slides behind explicit deferred sources rather than requesting full photos.
html=re.sub(r'(<a\b[^>]*class="room-photo"[^>]* hidden[^>]*>)(<img[^>]+>)',lambda m:m[1]+m[2].replace('src="','data-src="').replace('srcset="','data-srcset="'),html)
page.write_text(html)
# Keep originals in source control for future edits; ship only encoded assets and the small logo.
for old in (root/'docs/assets').iterdir():
 if old.suffix.lower() in ['.png','.jpg','.jpeg'] and old.name!='logo-originale.png':
  if not (source/old.name).exists():shutil.copyfile(old,source/old.name)
  old.unlink()
(root/'scripts/image-manifest.json').write_text(json.dumps(variants,indent=2))
print(f'Referenced source photos: {before/1024/1024:.1f} MB; all responsive sizes combined: {after/1024/1024:.1f} MB')
print(f'Hero: {variants["chalet.jpg.png"][-1]["bytes"]/1024:.0f} KB; all thumbnail files: {sum(v[0]["bytes"] for v in variants.values())/1024:.0f} KB')
