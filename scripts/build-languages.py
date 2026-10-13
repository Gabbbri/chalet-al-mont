from pathlib import Path
from html.parser import HTMLParser
from html import escape
import json,re
root=Path(__file__).resolve().parents[1];page=root/'docs/index.html'
base=page.read_text()
if 'class="language-switch"' not in base:
 switch='''<details class="language-switch"><summary aria-label="Scegli la lingua"><span>IT</span><span aria-hidden="true">⌄</span></summary><div class="language-list"><a href="/" lang="it" hreflang="it" data-language="it" aria-current="page">Italiano</a><a href="/en/" lang="en" hreflang="en" data-language="en">English</a><a href="/de/" lang="de" hreflang="de" data-language="de">Deutsch</a></div></details>'''
 old='<a class="top-cta" href="#contatti">DISPONIBILITÀ <span>↗</span></a>'
 assert old in base
 base=base.replace(old,'<div class="header-actions">'+old+switch+'</div>')
 base=base.replace('<script src="/gallery.js"></script>','<script src="/language-menu.js"></script>\n  <script src="/gallery.js"></script>')
 base=base.replace('</head>','<link rel="alternate" hreflang="it" href="https://gabbbri.github.io/chalet-al-mont/"><link rel="alternate" hreflang="en" href="https://gabbbri.github.io/chalet-al-mont/en/"><link rel="alternate" hreflang="de" href="https://gabbbri.github.io/chalet-al-mont/de/"></head>')
 page.write_text(base)
rows=[
('LO CHALET','THE CHALET','DAS CHALET'),('IL LUOGO','THE SETTING','DIE UMGEBUNG'),('CONTATTI','CONTACT','KONTAKT'),('DISPONIBILITÀ','AVAILABILITY','VERFÜGBARKEIT'),
('01 — LO CHALET','01 — THE CHALET','01 — DAS CHALET'),('02 — IL LUOGO','02 — THE SETTING','02 — DIE UMGEBUNG'),('03 — GLI AMBIENTI','03 — THE SPACES','03 — DIE RÄUME'),('04 — COME RAGGIUNGERCI','04 — GETTING HERE','04 — ANREISE'),('05 — CONTATTI','05 — CONTACT','05 — KONTAKT'),
('Il calore','The warmth','Gemütlichkeit'),('dello chalet','of the chalet','im Chalet'),('La libertà','The freedom','Zeit'),('di rallentare','to slow down','zum Durchatmen'),('Lo chalet,','The chalet,','Das Chalet'),('da vicino','up close','im Detail'),('Come','Getting','Dein Weg'),('raggiungerci','here','zum Chalet'),('Contatti','Contact','Kontakt'),
('Esplora gli ambienti','Explore the spaces','Die Räume ansehen'),('01 / PIANO TERRA','01 / GROUND FLOOR','01 / ERDGESCHOSS'),('02 / PIANO SUPERIORE','02 / UPPER FLOOR','02 / OBERGESCHOSS'),('03 / ALL’APERTO','03 / OUTDOORS','03 / DRAUSSEN'),('Cucina e zona giorno','Kitchen and living area','Küche und Wohnbereich'),('Camera da letto','Bedroom','Schlafzimmer'),('Solarium ed esterni','Sun terrace and outdoor spaces','Sonnenterrasse und Außenbereich'),
('Apri le indicazioni','Get directions','Route öffnen'),('IL TUO SOGGIORNO','YOUR STAY','DEIN AUFENTHALT'),('Scegli le tue date','Choose your dates','Reisedaten wählen'),('Arrivo','Arrival','Anreise'),('Partenza','Departure','Abreise'),('Nome','Name','Name'),('Email','Email','E-Mail'),('Ospiti','Guests','Gäste'),('Messaggio','Message','Nachricht'),('Richieste o informazioni sul soggiorno','Questions or requests for your stay','Fragen oder Wünsche zu deinem Aufenthalt'),('Seleziona le date per preparare la richiesta.','Choose your dates to prepare your enquiry.','Wähle die Reisedaten für deine Anfrage.'),('Invia richiesta su WhatsApp ↗','Send enquiry on WhatsApp ↗','Anfrage per WhatsApp senden ↗'),('Lo chalet resta chiuso nei mesi invernali.','The chalet is closed during the winter months.','Das Chalet ist in den Wintermonaten geschlossen.'),('↑ Torna su','↑ Back to top','↑ Nach oben'),
('Chalet al Mont — Una casa sul Monte Peller','Chalet al Mont — A mountain chalet on Monte Peller','Chalet al Mont — Eine Hütte am Monte Peller'),('Chalet al Mont, torna all\'inizio','Chalet al Mont, back to top','Chalet al Mont, zum Seitenanfang'),('Menu principale','Main menu','Hauptmenü'),('Scendi alla descrizione','Scroll to the chalet','Zum Chalet scrollen'),('Scegli la lingua','Choose language','Sprache wählen'),('Logo originale di Chalet al Mont','Chalet al Mont logo','Logo von Chalet al Mont'),
('Fotografie dello chalet, esterni e interni','Chalet photographs, indoors and outdoors','Fotos des Chalets, innen und außen'),('Fotografie: piano terra','Ground floor photographs','Fotos vom Erdgeschoss'),('Fotografie: piano superiore','Upper floor photographs','Fotos vom Obergeschoss'),('Fotografie: all’aperto','Outdoor photographs','Fotos vom Außenbereich'),('Scegli una foto','Choose a photograph','Foto auswählen'),('Foto precedente','Previous photo','Vorheriges Foto'),('Foto successiva','Next photo','Nächstes Foto'),('Galleria fotografica dello chalet','Chalet photo gallery','Fotogalerie des Chalets'),('Chiudi la galleria','Close gallery','Galerie schließen'),('Mese precedente','Previous month','Vorheriger Monat'),('Mese successivo','Next month','Nächster Monat'),('Calendario per scegliere le date','Calendar for choosing dates','Kalender zur Auswahl der Reisedaten'),('Mappa di Chalet al Mont sul Monte Peller','Map of Chalet al Mont on Monte Peller','Karte von Chalet al Mont am Monte Peller'),('Contatti della famiglia','Family contact numbers','Telefonnummern der Familie'),
('Apri la foto della facciata','Open the chalet exterior photo','Foto der Chaletfassade öffnen'),('Apri la foto della terrazza','Open the terrace photo','Foto der Terrasse öffnen'),('Apri la foto della cucina','Open the kitchen photo','Foto der Küche öffnen'),('Apri la foto della camera','Open the bedroom photo','Foto des Schlafzimmers öffnen'),
('Chalet al Mont sul prato del Monte Peller','Chalet al Mont in the meadows of Monte Peller','Chalet al Mont auf den Wiesen des Monte Peller'),('La baita e le sedute sul prato','The chalet and the outdoor seating','Das Chalet und die Sitzplätze im Freien'),('Terrazza con tavolo e sdraio','Terrace with a table and sun loungers','Terrasse mit Tisch und Sonnenliegen'),('Cucina in legno e focolare, sotto la scala','Wooden kitchen and stove beneath the stairs','Holzküche und Herd unter der Treppe'),('I letti nella camera al piano superiore','Beds in the upstairs bedroom','Betten im Schlafzimmer im Obergeschoss'),('La baita nella radura tra il prato e il bosco','The chalet in a clearing between meadow and forest','Das Chalet auf einer Lichtung zwischen Wiese und Wald'),('La baita vista dal prato','The chalet seen from the meadow','Das Chalet von der Wiese aus gesehen'),('La cucina e la scala che porta al piano superiore','The kitchen and the stairs to the upper floor','Die Küche und die Treppe zum Obergeschoss'),('Il tavolo della zona giorno, davanti alle due finestre','The dining table beside the two windows','Der Esstisch vor den beiden Fenstern'),('Il focolare a legna al piano terra','The wood-burning stove on the ground floor','Der Holzherd im Erdgeschoss'),('Il divano nella zona giorno','The sofa in the living area','Das Sofa im Wohnbereich'),('Il bagno al piano terra, con lavabo e doccia','Ground floor bathroom with basin and shower','Das Bad im Erdgeschoss mit Waschbecken und Dusche'),('Letto matrimoniale e letto singolo nella camera al piano superiore','Double and single beds in the upstairs bedroom','Doppelbett und Einzelbett im Schlafzimmer im Obergeschoss'),('I letti singoli sotto il soffitto in legno','Single beds beneath the wooden ceiling','Einzelbetten unter der Holzdecke'),('Il letto matrimoniale visto dalla finestra','The double bed seen from the window','Das Doppelbett vom Fenster aus gesehen'),('La terrazza con tavolo e sdraio','The terrace with table and sun loungers','Die Terrasse mit Tisch und Sonnenliegen'),('Il prato e il bosco visti dalla terrazza','The meadow and forest seen from the terrace','Wiese und Wald von der Terrasse aus gesehen'),('La terrazza vista dal prato, con accesso al piano superiore','Terrace seen from the meadow, with access to the upper floor','Die Terrasse von der Wiese aus, mit Zugang zum Obergeschoss'),('Il tavolo sulla terrazza e il percorso di accesso alla baita','The terrace table and the path to the chalet','Der Tisch auf der Terrasse und der Zugang zum Chalet'),('La panca in legno accanto alla facciata','The wooden bench beside the chalet','Die Holzbank an der Chaletfassade'),('La famiglia Dallago, che accoglie gli ospiti di Chalet al Mont','The Dallago family, your hosts at Chalet al Mont','Die Familie Dallago, die Gastgeber von Chalet al Mont')]
copy=json.loads((root/'scripts/approved-copy.json').read_text())
copy['3'][0]=copy['3'][0].replace('per cominciare a sentirsi a casa.','per cominciare già a sentirti a casa.')
copy['4'][0]=copy['4'][0].replace('Dal paese di Tuenno, in Val di Non,','Dal paese di Tuenno, al centro della Val di Non,').replace('Spegni il motore, sei in vacanza.','Spegni il motore, sei in vacanza!')
translations={
'1':[
('The chalet is for your exclusive use and sleeps up to five guests. Downstairs, the wooden kitchen and large dining table are where everyone comes together — over a good meal, an unhurried conversation and the crackle of the wood-burning stove.','Das Chalet wird als Ganzes vermietet und bietet Platz für bis zu fünf Gäste. Im Erdgeschoss bilden die Holzküche und der große Esstisch den Mittelpunkt des Hauses. Hier kommt man bei einem guten Essen zusammen, lässt Gespräche ihren Lauf nehmen und hört dabei das Holz im Herd knistern.'),
('Upstairs, the bedroom overlooks the meadows of Monte Peller. Wake up to the view, take your time and let the pace of the mountains make room for a proper break.','Vom Schlafzimmer im Obergeschoss geht der Blick auf die Wiesen des Monte Peller. Die Aussicht lädt dazu ein, den Tag in Ruhe zu beginnen, im Rhythmus der Berge abzuschalten und wieder richtig Urlaub zu machen.')],
'2':[("At the chalet, nature sets the pace and the rush of everyday life feels a long way off. Head out through woods and open mountain scenery, stopping at an alpine hut for local specialities. Or stay a little longer over lunch, let the conversation wander and spend the afternoon on the grass with a good book. There’s no need to keep an eye on the time.",'Auf der Hütte ist die Natur ganz nah, der Alltag weit weg. Von hier aus kannst du durch Wälder wandern, weite Ausblicke genießen und auf einer Alm regionale Spezialitäten probieren. Oder du bleibst einfach hier, sitzt noch etwas länger beim Mittagessen und verbringst den Nachmittag mit einem guten Buch auf der Wiese. Ganz ohne auf die Uhr zu schauen.')],
'3':[("From the kitchen table to the sun loungers on the terrace, every space has its place in the day. Take a closer look at the rooms and details, and start picturing yourself at home here.",'Vom Küchentisch bis zu den Sonnenliegen auf der Terrasse: Jeder Platz hat seine Zeit im Tagesablauf. Ein Blick in die Räume und auf die Details — damit du dich schon jetzt ein wenig zu Hause fühlst.')],
'4':[("From Tuenno, in the central part of Val di Non, follow the mountain road for around 8 km towards Monte Peller. The road has asphalt and concrete sections. Parking is right beside the chalet, so you can unload your bags and settle in without rushing. Switch off the engine. Your holiday starts here!",'Von Tuenno, zentral im Val di Non gelegen, geht es rund 8 km hinauf Richtung Monte Peller. Die Bergstraße ist teils asphaltiert, teils betoniert. Du parkst direkt neben dem Chalet und kannst in Ruhe das Gepäck ausladen und ankommen. Motor aus — der Urlaub beginnt!')],
'5':[("You’ve seen the chalet. Now meet the family behind it: we’re the Dallagos. We like to think that your next holiday could begin right here, in a place that means so much to us.",'Das Chalet kennst du jetzt. Nun möchten wir uns vorstellen: Wir sind die Familie Dallago. Es ist ein schöner Gedanke, dass dein nächster Urlaub genau hier beginnen könnte — an einem Ort, der uns sehr am Herzen liegt.'),('For availability, information or a quote, get in touch directly or fill in the form below.','Für freie Termine, Fragen oder ein Angebot erreichst du uns direkt oder über das Formular unten.')]
}
for key,paragraphs in copy.items():
 for original,(en,de) in zip(paragraphs,translations[key]):rows.append((original,en,de))
for i in range(1,6):rows.append((f'{i} '+('ospite' if i==1 else 'ospiti'),f'{i} '+('guest' if i==1 else 'guests'),f'{i} '+('Gast' if i==1 else 'Gäste')))
meta='Chalet al Mont: una baita indipendente per cinque ospiti sul Monte Peller, tra prato e bosco. Esplora gli spazi e scrivi per la disponibilità.'
rows.append((meta,'Chalet al Mont: a private chalet for up to five guests on Monte Peller, between meadows and forest. Explore the spaces and ask about availability.','Chalet al Mont: eine Hütte für bis zu fünf Gäste am Monte Peller, zwischen Wiesen und Wald. Entdecke die Räume und frage nach freien Terminen.'))
tables={lang:{row[0]:row[i] for row in rows} for lang,i in [('en',1),('de',2)]}
(root/'scripts/translations.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2))
unknown=set()
def translate(text,lang):
 if text in tables[lang]:return tables[lang][text]
 for prefix,en,de in [('Ingrandisci: ','Enlarge: ','Vergrößern: '),('Mostra: ','Show: ','Anzeigen: ')]:
  if text.startswith(prefix):return (en if lang=='en' else de)+translate(text[len(prefix):],lang)
 if re.search(r'[A-Za-zÀ-ÿ]',text) and text not in ['IT','×','CHALET','AL MONT','MONTE PELLER · VAL DI NON','Monte Peller · Val di Non','Leonardo','Talita','Viridiana','Leonardo · +39 335 605 5109','chaletalmont2k16@gmail.com','Italiano','English','Deutsch','L','M','G','V','S','D','CIN IT022249C2B84GAFRP · CIPAT 022249-AT-070354']:unknown.add(text)
 return text
class Renderer(HTMLParser):
 def __init__(self,lang):super().__init__(convert_charrefs=True);self.lang=lang;self.out=[]
 def handle_decl(self,d):self.out.append('<!'+d+'>')
 def handle_starttag(self,t,attrs):
  d=dict(attrs);new=[]
  for k,v in attrs:
   if t=='html' and k=='lang':v=self.lang
   if k in ['src','href','data-src'] and v and not v.startswith(('https:','http:','mailto:','tel:','#','//')):
    if d.get('data-language'):
     selected=d['data-language'];v='./' if selected==self.lang else '../' if selected=='it' else '../'+selected+'/'
    else:v='../'+v.lstrip('/')
   if k in ['srcset','data-srcset'] and v:
    v=', '.join('../'+part.strip().lstrip('/') for part in v.split(','))
   if t=='iframe' and k=='src' and v and 'google.com/maps' in v:v+='&hl='+self.lang
   if v is not None and k in ['alt','aria-label','title','placeholder']:v=translate(v,self.lang)
   if t=='meta' and d.get('name')=='description' and k=='content':v=translate(v,self.lang)
   if k=='aria-current' and d.get('data-language'):continue
   new.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
  if d.get('data-language')==self.lang:new.append('aria-current="page"')
  self.out.append('<'+t+(' '+' '.join(new) if new else '')+'>')
 def handle_endtag(self,t):self.out.append('</'+t+'>')
 def handle_data(self,data):
  text=data.strip();translated=translate(text,self.lang) if text else text
  self.out.append(escape(data.replace(text,translated,1) if text else data,quote=False))
 def handle_comment(self,data):self.out.append('<!--'+data+'-->')
for lang in ['en','de']:
 renderer=Renderer(lang);renderer.feed(base);output=''.join(renderer.out)
 output=output.replace('<span>IT</span><span aria-hidden="true">⌄</span>','<span>'+lang.upper()+'</span><span aria-hidden="true">⌄</span>')
 old='<div class="calendar-week" aria-hidden="true"><span>L</span><span>M</span><span>M</span><span>G</span><span>V</span><span>S</span><span>D</span></div>'
 days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] if lang=='en' else ['Mo','Di','Mi','Do','Fr','Sa','So']
 assert old in output
 output=output.replace(old,'<div class="calendar-week" aria-hidden="true">'+''.join('<span>'+x+'</span>' for x in days)+'</div>')
 dest=root/'docs'/lang;dest.mkdir(exist_ok=True);(dest/'index.html').write_text(output)
assert not unknown,sorted(unknown)
print('English and German pages generated; all visible text and accessible labels covered')
