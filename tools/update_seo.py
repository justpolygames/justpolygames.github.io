"""Regenerate static metadata and sitemap: python3 tools/update_seo.py."""
from pathlib import Path
import html,json,re,struct,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE='https://justpolygames.github.io/'
CSS_VERSION=hashlib.sha256((ROOT/'style.css').read_bytes()).hexdigest()[:12]
JS_VERSION=hashlib.sha256((ROOT/'site.js').read_bytes()).hexdigest()[:12]
PAGES={
 'index.html':('Just Poly Games - Indie Game Developer','Meet Anthony, a Filipino indie game developer, designer, and Product Manager. Explore Project Pencil and QUINTARC, with mechanics, controls, and game guides.','assets/just-poly-icon.png','Just Poly Games cyan, blue, and violet JP icon',1280,1280),
 'games/project-pencil/index.html':('Project Pencil — Drawing Adventure & Game Guide | Just Poly Games','Discover Project Pencil, a first-person drawing adventure. Learn how to draw tools and weapons, explore the story, and find game modes, controls, and tips.','assets/project-pencil.png','Project Pencil — Draw your way through',630,500),
 'games/quintarc/index.html':('QUINTARC — Elemental Magic & 126-Spell Guide | Just Poly Games','Explore QUINTARC: combine five elements into 126 spells. Browse the searchable spellbook, campaign, arenas, multiplayer modes, mechanics, and PC controls.','assets/quintarc-cover-0.1.7.png','QUINTARC grimoire and five elemental seals',1260,1000),
 'credits/index.html':('Game Credits, Creators & Asset Licenses | Just Poly Games','Explore Project Pencil and QUINTARC credits: asset creators, character models, spell icons, sound, fonts, technology, and original license notices.','assets/just-poly-icon.png','Just Poly Games JP icon',1280,1280)
}
org={'@type':'Organization','@id':BASE+'#studio','name':'Just Poly Games','url':BASE,'logo':BASE+'assets/just-poly-icon.png','sameAs':['https://github.com/justpolygames','https://justpolygames.itch.io/']}
person={'@type':'Person','@id':BASE+'#anthony','name':'Anthony','url':BASE+'#about','jobTitle':['Indie Game Developer','Product Manager'],'description':'An indie game developer from the Philippines with experience in Web Design and UI/UX Design.','homeLocation':{'@type':'Country','name':'Philippines'}}
site={'@type':'WebSite','@id':BASE+'#website','name':'Just Poly Games','url':BASE,'publisher':{'@id':BASE+'#studio'},'inLanguage':'en'}
urls=[]
for path,(title,description,img,alt,width,height) in PAGES.items():
 width,height=struct.unpack('>II',(ROOT/img).read_bytes()[16:24])
 url=BASE+('' if path=='index.html' else path.removesuffix('index.html'));urls.append(url)
 prefix='/'
 page={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,'isPartOf':{'@id':BASE+'#website'},'inLanguage':'en','primaryImageOfPage':{'@type':'ImageObject','url':BASE+img}}
 graph=[org,site,page]
 if path=='index.html':
  graph.append(person);page['about']={'@id':BASE+'#anthony'}
 elif path.startswith('games/'):
  name='QUINTARC' if 'quintarc' in path else 'Project Pencil'
  game={'@type':'VideoGame','@id':url+'#game','name':name,'url':url,'description':description,'image':BASE+img,'author':{'@id':BASE+'#studio'},'gamePlatform':'PC','genre':'Elemental spellcasting' if name=='QUINTARC' else 'First-person drawing adventure','inLanguage':'en'}
  page['about']={'@id':url+'#game'}
  breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':1,'name':'Just Poly Games','item':BASE},{'@type':'ListItem','position':2,'name':name,'item':url}]}
  page['breadcrumb']={'@id':url+'#breadcrumbs'};graph.extend([game,breadcrumb])
 def esc(v):return html.escape(str(v),quote=True)
 head=['<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">',f'<title>{esc(title)}</title>',f'<meta name="description" content="{esc(description)}">','<meta name="author" content="Anthony, Just Poly Games">','<meta name="robots" content="index, follow, max-image-preview:large">','<meta name="theme-color" content="#0b1020">',f'<link rel="canonical" href="{url}">']
 for prop,val in {'og:type':'website','og:site_name':'Just Poly Games','og:locale':'en_PH','og:title':title,'og:description':description,'og:url':url,'og:image':BASE+img,'og:image:alt':alt,'og:image:type':'image/png','og:image:width':width,'og:image:height':height}.items():head.append(f'<meta property="{prop}" content="{esc(val)}">')
 for prop,val in {'twitter:card':'summary','twitter:title':title,'twitter:description':description,'twitter:image':BASE+img,'twitter:image:alt':alt}.items():head.append(f'<meta name="{prop}" content="{esc(val)}">')
 head.extend([f'<link rel="icon" href="{prefix}assets/just-poly-icon.png" type="image/png">',f'<link rel="stylesheet" href="{prefix}style.css?v={CSS_VERSION}">',f'<script src="{prefix}site.js?v={JS_VERSION}" defer></script>','<script type="application/ld+json">\n'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2)+'\n</script>'])
 p=ROOT/path;text=p.read_text();
 if 'quintarc' in path: head=[line.replace('/assets/just-poly-icon.png', '/assets/quintarc-app.png') if 'rel="icon"' in line else line for line in head]
 text=re.sub(r'<head>.*?</head>','<head>\n'+'\n'.join(head)+'\n</head>',text,count=1,flags=re.S);p.write_text(text)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Updated metadata, structured data, robots.txt, and four canonical sitemap URLs.')
