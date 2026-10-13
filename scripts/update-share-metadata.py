from pathlib import Path
from html import escape
import re

root = Path(__file__).resolve().parents[1]
origin = 'https://gabbbri.github.io/chalet-al-mont/'
title = 'Chalet al Mont · Monte Peller, Val di Non'
locales = {'it':'it_IT','en':'en_GB','de':'de_DE'}
alts = {'it':'Chalet al Mont tra i prati e i boschi del Monte Peller', 'en':'Chalet al Mont among the meadows and woodland of Monte Peller', 'de':'Chalet al Mont zwischen Wiesen und Wäldern am Monte Peller'}
for lang in ['it','en','de']:
    page = root / 'docs' / ('' if lang=='it' else lang) / 'index.html'
    html = page.read_text()
    description = re.search(r'<meta name="description" content="([^"]*)">', html).group(1)
    html = re.sub(r'<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>\s*', '', html)
    url = origin + ('' if lang=='it' else lang+'/')
    image = origin + 'assets/chalet-al-mont-social.jpg'
    values = [('og:type','website'),('og:site_name','Chalet al Mont'),('og:title',title),('og:description',description),('og:url',url),('og:locale',locales[lang]),('og:image',image),('og:image:secure_url',image),('og:image:type','image/jpeg'),('og:image:width','1200'),('og:image:height','630'),('og:image:alt',alts[lang])]
    tags = '\n'.join('<meta property="'+key+'" content="'+escape(value,quote=True)+'">' for key,value in values)
    tags += '\n'+ '\n'.join('<meta name="'+key+'" content="'+escape(value,quote=True)+'">' for key,value in [('twitter:card','summary_large_image'),('twitter:title',title),('twitter:description',description),('twitter:image',image),('twitter:image:alt',alts[lang])])
    html = html.replace('</head>', tags+'\n</head>')
    page.write_text(html)
print('Share metadata updated for IT, EN and DE')
