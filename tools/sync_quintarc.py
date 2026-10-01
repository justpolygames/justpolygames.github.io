"""Sync QUINTARC's player guide from a verified local game source tree."""
import argparse,hashlib,html,json,re,shutil,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
site=Path(__file__).resolve().parents[1];root=a.source.resolve()
data=json.loads((root/'data/spell_recipes.json').read_text())
icons=json.loads((root/'data/spell_icons.json').read_text())
descriptions=json.loads((root/'data/spell_descriptions.json').read_text())
summaries=json.loads((root/'data/spell_summaries.json').read_text())
with tempfile.TemporaryDirectory(prefix='quintarc-guide-') as temporary:
 output=Path(temporary)/'details.json'
 subprocess.run(['godot','--headless','--log-file',str(Path(temporary)/'export.log'),'--path',str(root),'--script',str(site/'tools/export_quintarc_details.gd'),'--',str(output)],check=True)
 details=json.loads(output.read_text())
assert set(data['recipes'])==set(icons)==set(descriptions)==set(summaries)==set(details)
assert len(details)==126
cards=[]
for key,r in data['recipes'].items():
 runtime=data['profiles'][r['profile']]|r['overrides']
 recipe=' · '.join(f'{e} ×{int(n)}' for n,e in zip(key,data['element_order']) if n!='0')
 keys=' '.join(str(i+1) for i,n in enumerate(key) for _ in range(int(n)))
 icon=root/icons[key].removeprefix('res://');shutil.copy2(icon,site/'assets/skill-icons'/icon.name)
 description=summaries[key];name=r['name'];search=html.escape(f'{name} {recipe} {descriptions[key]} {description} {" ".join(details[key])}'.lower(),quote=True)
 rows=(len(details[key])+1)//2
 columns=[]
 for start in (0,rows):
  entries=[]
  for detail in details[key][start:start+rows]:
   label,value=detail.split(': ',1)
   entries.append(f'<div><dt>{html.escape(label)}:</dt> <dd>{html.escape(value)}</dd></div>')
  columns.append('<dl>'+''.join(entries)+'</dl>')
 stats='<div class="spell-details">'+''.join(columns)+'</div>'
 cards.append(f'<article class="spell-card" data-search="{search}"><div class="spell-heading"><img src="/assets/skill-icons/{icon.name}" width="56" height="56" loading="lazy" decoding="async" alt=""><h3>{html.escape(name)}</h3></div><p class="recipe">{html.escape(recipe)}</p><p class="spell-description">{html.escape(description)}</p>{stats}<div class="spell-stats"><span>Keys: <kbd>{keys}</kbd> → <kbd>Q</kbd></span></div></article>')
page=site/'games/quintarc/index.html';text=page.read_text()
text,n=re.subn(r'<div class="spell-list">.*?</div></section>','<div class="spell-list">'+''.join(cards)+'</div></section>',text,flags=re.S);assert n==1
shutil.copy2(root/'assets/quintarc-app.png',site/'assets/quintarc-app.png')
version=hashlib.sha256((site/'assets/quintarc-app.png').read_bytes()).hexdigest()[:12]
text=re.sub(r'<link rel="icon"[^>]*>',f'<link rel="icon" href="/assets/quintarc-app.png?v={version}" type="image/png">',text)
blurb='<p class="spell-roles">Spells have specific targeting, timing, movement, resource, and terrain interactions. Mire Guardian holds a fixed area; Magma Eruption opens a narrow ground fissure. The cards below describe each spell’s current behavior. Encapsulate enemies in ice with Flash Freeze and Blizzard. Matching Earth, Fire, electrical, and Arcane skills apply Poison, Burn, Shock, and Mana Drain. Shock prevents new invocations while leaving stored spells available. Shields block incoming debuffs; cleanse skills remove active effects.</p>'
text=re.sub(r'<p class="spell-roles">.*?</p>','',text)
needle='<section class="wiki-section" id="overview">';start=text.index(needle);end=text.index('</section>',start);text=text[:end]+blurb+text[end:]
page.write_text(text)
shutil.copy2(root/'assets/licenses/QUINTARC-Wave-Icon.txt',site/'assets/licenses/QUINTARC-Wave-Icon.txt')
attrs=site/'assets/ATTRIBUTION.md';note='\n## Leviathan Surge water-wave icon\n\nBig wave by Lorc, https://game-icons.net/1x1/lorc/big-wave.html, CC BY 3.0.\nRecolored cyan/white and rasterized. See licenses/QUINTARC-Wave-Icon.txt.\n'
if '## Leviathan Surge water-wave icon' not in attrs.read_text():attrs.write_text(attrs.read_text()+note)
shutil.copy2(root/'data/spell_icon_provenance.json',site/'assets/quintarc-skill-icon-provenance.json')
shutil.copy2(root/'assets/licenses/QUINTARC-Skill-Identity-Icons.txt',site/'assets/licenses/QUINTARC-Skill-Identity-Icons.txt')
print('Synced 126 current spells, matching icons, electrical/ice overview, game favicon and wave attribution.')
